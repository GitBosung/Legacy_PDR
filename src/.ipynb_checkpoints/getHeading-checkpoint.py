import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def rotation_matrix_x(theta):
    """
    Generate a rotation matrix for rotation around the x-axis.

    Parameters:
        theta (float): Angle in radians.

    Returns:
        np.array: 3x3 rotation matrix.
    """
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]])

def rotation_matrix_y(theta):
    """
    Generate a rotation matrix for rotation around the y-axis.

    Parameters:
        theta (float): Angle in radians.

    Returns:
        np.array: 3x3 rotation matrix.
    """
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                     [0, 1, 0],
                     [-np.sin(theta), 0, np.cos(theta)]])

def apply_rotation_matrices(rot_matrices, gyro_data):
    """
    Apply rotation matrices to gyroscope data.

    Parameters:
        rot_matrices (list of np.array): List of 3x3 rotation matrices.
        gyro_data (np.array): Nx3 array of gyroscope data.

    Returns:
        np.array: Rotated gyroscope data.
    """
    rotated_data = []
    for rot_matrix, gyro_row in zip(rot_matrices, gyro_data):
        rotated_data.append(np.dot(rot_matrix, gyro_row))
    return np.array(rotated_data)

def calculate_bearing(df, api_pitch, api_roll, sampling_time=0.02):
    """
    Calculate the bearing (yaw) from gyroscope data after applying rotation matrices.

    Parameters:
        df (pd.DataFrame): DataFrame containing gyroscope data (Gyroscope x, y, z).
        api_pitch (list or np.array): List of pitch angles in degrees.
        api_roll (list or np.array): List of roll angles in degrees.
        sampling_time (float): Sampling time interval in seconds (default: 0.02).

    Returns:
        pd.DataFrame: DataFrame with updated columns for rotated gyroscope data and final bearing.
    """
    # Convert gyroscope data to numpy array
    gyro_data = np.vstack([df['Gyroscope x'], df['Gyroscope y'], df['Gyroscope z']]).T

    # Create rotation matrices
    rot_matrices_x = [rotation_matrix_x(theta) for theta in np.radians(api_pitch)]
    rot_matrices_y = [rotation_matrix_y(theta) for theta in np.radians(api_roll)]

    # Apply rotation matrices
    rotated_gyro_data = apply_rotation_matrices(rot_matrices_x, gyro_data)
    df['Rotated Gyroscope x'] = rotated_gyro_data[:, 0]
    df['Rotated Gyroscope y'] = rotated_gyro_data[:, 1]
    df['Rotated Gyroscope z'] = rotated_gyro_data[:, 2]

    rotated_gyro_data2 = apply_rotation_matrices(rot_matrices_y, rotated_gyro_data)
    df['Rotated2 Gyroscope x'] = rotated_gyro_data2[:, 0]
    df['Rotated2 Gyroscope y'] = rotated_gyro_data2[:, 1]
    df['Rotated2 Gyroscope z'] = rotated_gyro_data2[:, 2]

    # Calculate yaw angle
    corrected_yaw = np.cumsum(df['Rotated2 Gyroscope z'] * sampling_time)
    corrected_yaw = np.degrees(corrected_yaw)
    df['Final_Bearing'] = corrected_yaw

    return df

# Example Usage
# df = pd.DataFrame({...})  # Your DataFrame with gyroscope data
# api_pitch = [...]         # List of pitch angles
# api_roll = [...]          # List of roll angles
# updated_df = calculate_bearing(df, api_pitch, api_roll, sampling_time=0.02)

# 좌표 회전 함수 정의
def rotate_coordinates(x, y, theta):
    theta = np.radians(theta)
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    rotated_coords = np.dot(rotation_matrix, np.vstack([x, y]))
    return rotated_coords[0], rotated_coords[1]


def plot_paths(predicted_x, predicted_y, true_x, true_y, rotation_angle=90):
    """
    Plot the predicted path and the true path.

    Parameters:
        predicted_x (list): x-coordinates of the predicted path.
        predicted_y (list): y-coordinates of the predicted path.
        true_x (list): x-coordinates of the true path.
        true_y (list): y-coordinates of the true path.
        rotation_angle (float): Rotation angle for predicted path (default: 90).
    """
    rotated_x, rotated_y = rotate_coordinates(predicted_x, predicted_y, rotation_angle)

    plt.plot(-rotated_x, rotated_y, marker='o', linestyle='-', color='b', label='Predict Path')
    plt.plot(true_x, true_y, marker='x', linestyle='--', color='r', label='True Path')
    plt.plot(-rotated_x[0], rotated_y[0], marker='s', color='g', markersize=10, label='Start Position')
    plt.title('True And Predict Path')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend()
    plt.axis('equal')
    plt.grid(True)
    plt.show()

