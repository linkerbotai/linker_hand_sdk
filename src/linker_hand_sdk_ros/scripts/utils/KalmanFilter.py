class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        self.x_est = 0.0  # 初始状态
        self.P = 1.0      # 初始误差协方差
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance

    def predict(self):
        # 预测步骤
        self.P += self.process_variance

    def update(self, measurement):
        # 更新步骤
        K = self.P / (self.P + self.measurement_variance)  # 卡尔曼增益
        self.x_est += K * (measurement - self.x_est)      # 更新状态估计
        self.P *= (1 - K)                                 # 更新误差协方差
        return self.x_est