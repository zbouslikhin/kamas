import logging
import numpy as np


def sma(series: np.ndarray, window: int) -> np.ndarray:
    ret = np.convolve(series, np.ones(window) / window, mode="valid")
    # pad start to maintain same length
    pad = np.full(len(series) - len(ret), np.nan)
    return np.concatenate([pad, ret])


def ema(series: np.ndarray, span: int) -> np.ndarray:
    alpha = 2 / (span + 1)
    out = np.empty_like(series)
    out[0] = series[0]
    for i in range(1, len(series)):
        out[i] = alpha * series[i] + (1 - alpha) * out[i - 1]
    return out


def atr(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, window: int
) -> np.ndarray:
    if len(high) < window:
        raise ValueError(
            f"Requested ATR with window {window} while input data length is {len(high)} "
        )
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]

    tr = np.maximum.reduce(
        [high - low, np.abs(high - prev_close), np.abs(low - prev_close)]
    )

    atr = np.convolve(tr, np.ones(window) / window, mode="valid")
    pad = np.full(len(tr) - len(atr), np.nan)
    return np.concatenate([pad, atr])
