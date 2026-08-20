"""
Signal smoothing algorithms (Exponential Moving Average & Moving Average).
"""
class ExponentialMovingAverage:
    """
    Exponential Moving Average (EMA) implementation for noise reduction in gesture signals.
    Formula: S_t = alpha * Y_t + (1 - alpha) * S_{t-1}
    """
    def __init__(self, alpha: float = 0.2, initial_value: float = None):
        self.alpha = max(0.01, min(1.0, alpha))
        self.value = initial_value

    def update(self, current_val: float) -> float:
        if self.value is None:
            self.value = float(current_val)
        else:
            self.value = self.alpha * current_val + (1.0 - self.alpha) * self.value
        return self.value

    def reset(self, new_value: float = None):
        self.value = new_value

    def set_alpha(self, alpha: float):
        self.alpha = max(0.01, min(1.0, alpha))
