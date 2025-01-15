from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import numpy as np
import pyqtgraph as pg

class WaveformApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("波形图")
        self.setGeometry(700, 100, 700, 400)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        
        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setYRange(0, 255)
        self.layout.addWidget(self.plot_widget)

        self.plot_data_item = self.plot_widget.plot()

        self.x = np.linspace(0, 255, 1000)
        self.y = self.x  # 初始为线性上升
        self.plot_data_item.setData(self.x, self.y)

        # 设置标尺范围
        self.plot_widget.setXRange(0, 255)
        self.plot_widget.setYRange(0, 255)

    def setData(self, custom_phase=None):
        if custom_phase is not None:
            # 将 custom_phase 映射到 0 到 255 的范围
            self.y = np.linspace(0, custom_phase, 1000)
        else:
            self.y = self.x
        self.plot_data_item.setData(self.x, self.y)

if __name__ == "__main__":
    app = QApplication([])
    window = WaveformApp()
    window.show()
    app.exec_()