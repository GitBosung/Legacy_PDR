import numpy as np
import pandas as pd
from src.data_loader import load_and_preprocess_csv
from src.detect_steps import detect_steps_peak
from src.getHeading import calculate_bearing
from src.plot_PDR_path import calculate_positions, plot_paths

def main():
    # 1. 데이터 로드 및 전처리
    file_path = "data/sensor_data_2.csv"
    try:
        df = load_and_preprocess_csv(file_path)
        print("✅ Data loaded and preprocessed.")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return

    # 2. 가속도 norm 계산
    acc_norm = np.sqrt(df['Accelerometer x']**2 + df['Accelerometer y']**2 + df['Accelerometer z']**2)
    print("✅ Accelerometer norm calculated.")

    # 3. 걸음 검출
    step_count, step_points = detect_steps_peak(df, acc_norm, peak_threshold=12, min_peak_distance=5, sampling_frequency=50)
    print(f"✅ Detected steps: {step_count}")

    # 4. 이동 방향 계산
    api_pitch = -df['Oriention y']  # Pitch 값
    api_roll = -df['Oriention z']   # Roll 값
    df = calculate_bearing(df, api_pitch, api_roll)
    print("✅ Heading calculated.")

    # 5. 이동 경로 계산
    stride_length = 0.62  # 보폭 (단위: 미터)
    initial_position = (0, 0)  # 초기 위치
    x_positions, y_positions = calculate_positions(step_points, df, stride_length, initial_position)
    print("✅ Predicted path calculated.")

    # 6. 실제 이동 경로 (예제)
    true_x_positions = [-10.5, 10, 10, -10.5, -10.5]
    true_y_positions = [0, 0, 14, 14, 0]

    # 7. 경로 시각화
    try:
        plot_paths(x_positions, y_positions, true_x_positions, true_y_positions)
        print("✅ Paths plotted.")
    except Exception as e:
        print(f"❌ Error plotting paths: {e}")

if __name__ == "__main__":
    main()
