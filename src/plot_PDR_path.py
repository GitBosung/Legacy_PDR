import matplotlib.pyplot as plt
import numpy as np

def calculate_positions(step_points, df, stride_length=0.62, initial_position=(0, 0)):
    """
    걸음 데이터를 기반으로 이동 경로 계산.

    Parameters:
        step_points (list): 걸음 발생 지점의 인덱스 리스트.
        df (pd.DataFrame): 데이터프레임 (베어링 포함).
        stride_length (float): 보폭 (기본값: 0.62m).
        initial_position (tuple): 초기 위치 (기본값: (0, 0)).

    Returns:
        tuple: x_positions, y_positions (각각의 이동 경로 좌표 리스트)
    """
    x_positions = [initial_position[0]]
    y_positions = [initial_position[1]]

    for i in range(1, len(step_points)):
        step_index = step_points[i]
        current_yaw = df['Final_Bearing'].iloc[step_index]
        new_x = x_positions[-1] + stride_length * np.sin(np.radians(current_yaw))
        new_y = y_positions[-1] + stride_length * np.cos(np.radians(current_yaw))
        x_positions.append(new_x)
        y_positions.append(new_y)

    return x_positions, y_positions

def plot_paths(predicted_x, predicted_y, true_x, true_y, rotation_angle=90):
    """
    예측 경로와 실제 경로를 시각화.

    Parameters:
        predicted_x (list): x-좌표 (예측 경로).
        predicted_y (list): y-좌표 (예측 경로).
        true_x (list): x-좌표 (실제 경로).
        true_y (list): y-좌표 (실제 경로).
        rotation_angle (float): 회전 각도 (기본값: 90도).
    """
    def rotate_coordinates(x, y, theta):
        theta = np.radians(theta)
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        rotated_coords = np.dot(rotation_matrix, np.vstack([x, y]))
        return rotated_coords[0], rotated_coords[1]

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
