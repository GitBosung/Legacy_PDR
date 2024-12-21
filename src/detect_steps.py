from scipy.signal import find_peaks

def detect_steps_peak(df, acc_norm, peak_threshold=12, min_peak_distance=5, sampling_frequency=50):
    """
    걸음을 피크 탐지 기반으로 검출하는 함수.

    Parameters:
        df (DataFrame): 센서 데이터를 포함한 데이터프레임 (추가 정보를 저장할 경우 활용 가능).
        acc_norm (array-like): 가속도 크기(norm) 값 배열.
        peak_threshold (float): 피크를 검출하기 위한 가속도 크기의 최소값 (기본값: 12).
        min_peak_distance (float): 피크 간 최소 간격 (초 단위, 기본값: 5초).
        sampling_frequency (int): 데이터의 샘플링 주파수 (Hz, 기본값: 50Hz).

    Returns:
        tuple:
            - step_count (int): 검출된 걸음 수.
            - peaks (array): 검출된 피크의 인덱스 배열.
    
    Description:
        1. 가속도 크기 배열에서 `find_peaks` 함수를 사용하여 피크를 검출합니다.
        2. `peak_threshold` 이상의 값만 피크로 간주하며, 
           `min_peak_distance` 조건을 만족하도록 샘플 간 최소 거리를 설정합니다.
        3. 검출된 피크의 개수를 반환하며, 각 피크의 인덱스 정보를 함께 반환합니다.
    
    Example:
        ```python
        # 데이터프레임과 가속도 크기(norm) 배열 준비
        df = ...  # 센서 데이터프레임
        acc_norm = [9.8, 12.5, 13.1, 9.2, 14.0, 10.1, 12.7]

        # 함수 호출
        step_count, peaks = detect_steps_peak(df, acc_norm, peak_threshold=12, min_peak_distance=0.5, sampling_frequency=50)

        # 출력 결과
        print(f"걸음 수: {step_count}, 피크 위치: {peaks}")
        ```
    """
    # 최소 피크 간 거리 계산 (샘플 단위로 변환)
    min_distance_samples = int(sampling_frequency / min_peak_distance)
    # 피크 검출
    peaks, _ = find_peaks(acc_norm, height=peak_threshold, distance=min_distance_samples)
    # 걸음 수 계산 및 걸음 발생 시간 저장
    step_count = len(peaks)
    
    return step_count, peaks
