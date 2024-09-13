import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt


def preprocess(data,fs):
    # バンドパスフィルタを適用
    if True:
        # バンドパスフィルタの設定
        lowcut = 8  # バンドパスフィルタの下限周波数
        highcut = 30  # バンドパスフィルタの上限周波数
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(2, [low, high], btype='band')
        data = filtfilt(b, a, data)

    # データを標準化
    scaler = StandardScaler()
    data = scaler.fit_transform(data.T).T
    return np.array(data)