import sys,rospy,os
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QWidget, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.load_write_yaml import LoadWriteYaml
class RightView(QMainWindow):
    button_clicked = pyqtSignal(list)  # 定义一个信号
    def __init__(self,hand_joint="L20", hand_type="left"):
        super().__init__()
        self.hand_joint = hand_joint
        self.hand_type = hand_type
        self.buttons = []
        self.yaml = LoadWriteYaml() # 初始化配置文件
        self.all_action = self.yaml.load_action_yaml(hand_type=self.hand_type,hand_joint=self.hand_joint)
        self.setWindowTitle("按钮网格布局")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
        self.init_buttons()

    def init_ui(self):
        # 主窗口容器
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 主布局
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # 输入框和添加按钮
        self.input_field = QLineEdit()
        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(self.add_button_to_list)

        # 输入框和按钮布局
        self.top_layout = QVBoxLayout()
        self.top_layout.setSpacing(10)
        self.top_layout.addWidget(self.input_field)
        self.top_layout.addWidget(self.add_button)

        # 添加到主布局
        self.main_layout.addLayout(self.top_layout)

        # 创建一个滚动区域用于按钮列表
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # 左对齐和上对齐
        self.scroll_area.setWidget(self.scroll_widget)

        # 添加滚动区域到主布局
        self.main_layout.addWidget(self.scroll_area)

        # 网格布局参数
        self.row = 0  # 当前行
        self.column = 0  # 当前列
        self.BUTTONS_PER_ROW = 2  # 每行按钮数量限制
    def init_buttons(self):
        if self.all_action == None:
            return
        for item in self.all_action:
            button = QPushButton(item["ACTION_NAME"])
            button.setFixedWidth(100)  # 可根据需要设置按钮宽度
            button.setFixedHeight(30)  # 可根据需要设置按钮高度
            button.clicked.connect(lambda checked, action_pos=item["ACTION_POS"]: self.button_clicked.emit(action_pos))
            # 添加按钮到网格布局
            self.scroll_layout.addWidget(button, self.row, self.column, alignment=Qt.AlignLeft | Qt.AlignTop)

            # 更新行列位置
            self.column += 1
            if self.column >= self.BUTTONS_PER_ROW:  # 超过每行按钮数量时换行
                self.column = 0
                self.row += 1

    def add_button_to_list(self):
        text = self.input_field.text().strip()
        if text:
            if self.hand_type == "left":
                topic = "/cb_left_hand_control_cmd"
            else:
                topic = "/cb_right_hand_control_cmd"
            # 当前手数据
            current_hand_pos = rospy.wait_for_message(topic=topic, topic_type=JointState, timeout=0.3)
            button = QPushButton(text)
            button.setFixedWidth(100)  # 可根据需要设置按钮宽度
            button.setFixedHeight(30)  # 可根据需要设置按钮高度
            button.clicked.connect(lambda checked, action_pos=list(current_hand_pos.position): self.button_clicked.emit(action_pos))
            # 添加按钮到网格布局
            self.scroll_layout.addWidget(button, self.row, self.column, alignment=Qt.AlignLeft | Qt.AlignTop)

            # 更新行列位置
            self.column += 1
            if self.column >= self.BUTTONS_PER_ROW:  # 超过每行按钮数量时换行
                self.column = 0
                self.row += 1
            
            # 将输入框内容写入yaml文件
            self.yaml.write_to_yaml(text, current_hand_pos.position,hand_joint=self.hand_joint,hand_type=self.hand_type)
            self.input_field.clear()  # 清空输入框
            self.buttons.append(button)