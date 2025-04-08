from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import sys
import random
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class WaveformPlot(QWidget):
    def __init__(self, num_lines=3, labels=None, title="Waveform Plot"):
        super().__init__()
        self.num_lines = num_lines
        self.labels = labels if labels else [f"Line {i+1}" for i in range(num_lines)]
        self.data = [[] for _ in range(self.num_lines)]  # 初始化数据列表
        self.max_points = 100  # 最大显示点数
        self.setWindowTitle(title)
        # 设置布局
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 初始化 matplotlib 图形
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # 初始化绘图曲线
        self.lines = [self.ax.plot([], [], label=self.labels[i])[0] for i in range(self.num_lines)]
        self.ax.set_xlim(0, self.max_points)
        self.ax.set_ylim(0, 300)
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.legend(loc='upper left')  # 固定标签位置到左上角

    def update_data(self, new_data):
        for i in range(self.num_lines):
            self.data[i].append(new_data[i])
            if len(self.data[i]) > self.max_points:
                self.data[i].pop(0)
        self._update_plot()

    def _update_plot(self):
        """内部方法: 更新绘图"""
        for i, line in enumerate(self.lines):
            line.set_data(range(len(self.data[i])), self.data[i])

        self.ax.set_xlim(0, self.max_points)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 示例: 创建一个包含 3 条曲线的波形图
    waveform_plot = WaveformPlot(num_lines=3)
    waveform_plot.resize(800, 400)
    waveform_plot.show()

    # 模拟数据更新
    timer = QTimer()

    def update():
        import random
        values = [random.randint(0, 300) for _ in range(3)]  # 生成随机数据
        waveform_plot.update_data(values)

    timer.timeout.connect(update)
    timer.start(100)  # 每 100 毫秒更新一次

    sys.exit(app.exec_())
