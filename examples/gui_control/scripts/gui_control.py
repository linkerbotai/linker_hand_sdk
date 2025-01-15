from PyQt5.QtWidgets import QMainWindow, QSplitter, QApplication,QMessageBox,QPushButton
from PyQt5.QtCore import Qt
import rospy, rospkg, yaml, os, sys,time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from views.left_view import LeftView
from views.right_view import RightView
from utils.load_write_yaml import LoadWriteYaml
from utils.ros_handler import RosHandler
from utils.wave_form import WaveformApp
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import threading

global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_sdk = "linker_hand_sdk_ros"
package_gui = "gui_control"
sdk_path = rospack.get_path(package_sdk)
gui_path = rospack.get_path(package_gui)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化 ROS 节点
        rospy.init_node('gui_control', anonymous=True)
        self.yaml = LoadWriteYaml() # 初始化配置文件
        # 读取配置文件
        self.setting = self.yaml.load_setting_yaml()
        # 判断左手是否配置
        self.left_hand = False
        self.right_hand = False
        if self.setting['LINKER_HAND']['LEFT_HAND']['EXISTS'] == True:
            self.left_hand = True
        elif self.setting['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            self.right_hand = True
        # gui控制只支持单手，这里进行左右手互斥
        if self.left_hand == True and self.right_hand == True:
            self.left_hand = True
            self.right_hand = False
        if self.left_hand == True:
            print("左手")
            self.hand_exists = True
            self.hand_joint = self.setting['LINKER_HAND']['LEFT_HAND']['JOINT']
            self.hand_type = "left"
        if self.right_hand == True:
            print("右手")
            self.hand_exists = True
            self.hand_joint = self.setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
            self.hand_type = "right"
        self.ros = RosHandler(hand_joint=self.hand_joint, hand_type=self.hand_type)
        # 读取动作文件
        self.action_pos = self.yaml.load_action_yaml(hand_joint=self.hand_joint,hand_type=self.hand_type)
        self.init_pos = [255] * 10
        if self.hand_joint == "L25":
            # L25
            self.init_pos = [255] * 25
            self.joint_name = ["拇指根部", "食指根部", "中指根部", "无名指根部","预留","拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","预留","拇指横摆","预留","预留","预留","预留","拇指中部","食指中部","中指中部","无名指中部","预留","拇指尖部","食指尖部","中指尖部","无名指尖部","预留"]
        elif self.hand_joint == "L20":
            self.init_pos = [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255]
            # L20
            self.joint_name = ["拇指根部", "食指根部", "中指根部", "无名指根部","小指根部","拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","小指侧摆","拇指横摆","预留","预留","预留","预留","拇指尖部","食指末端","中指末端","无名指末端","小指末端"]
        elif self.hand_joint == "L10":
            # L10
            self.init_pos = [255] * 10
            self.joint_name = ["拇指根部", "拇指侧摆","食指根部", "中指根部", "无名指根部","小指根部","食指侧摆","无名指侧摆","小指侧摆","拇指横摆"]
        self.init_gui_view()

    # 初始化窗口界面
    def init_gui_view(self):
        if self.hand_type == "left":
            self.setWindowTitle(f"Linker_Hand:左手- {self.hand_joint} Control - Qt5 with ROS")
        else:
            self.setWindowTitle(f"Linker_Hand:右手- {self.hand_joint} Control - Qt5 with ROS")
        self.setGeometry(100, 100, 600, 800)
        # 创建分割线
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                width:1px;
                background-color: lightgray;
                margin: 15px 20px;
            }
        """)
        # 左侧滑动条界面
        self.left_view = LeftView(joint_name=self.joint_name, init_pos=self.init_pos)
        splitter.addWidget(self.left_view)
        # 右侧记录动作界面
        self.right_view = RightView(hand_joint=self.hand_joint, hand_type=self.hand_type)
        splitter.addWidget(self.right_view)
        # 接收到信号槽事件，这里用于记录动作序列更新滑动条数据
        self.right_view.button_clicked.connect(self.handle_button_click)
        splitter.setSizes([600, 450])
        self.setCentralWidget(splitter)
        # 每秒发送 100 次
        self.running = True
        self.stop_event = threading.Event()  # 创建一个事件对象
        self.udp_thread = threading.Thread(target=self.send_ros_data)
        self.udp_thread.start()

    def handle_button_click(self,action_pos):
        print(action_pos)
        self.left_view.set_slider_values(values=action_pos)
    # 发送数据到ROS
    def send_ros_data(self):
        while self.running and not rospy.is_shutdown():
            if self.left_view.is_open == False:
                print("被关闭")
                continue
            slider_values = [slider.value() for slider in self.left_view.sliders]
            data = ",".join(map(str, slider_values))
            self.ros.pub_msg(pos=data)
    # 更新滑动条状态
    def update_label(self, index, value):
        self.left_view.labels[index].setText(f"{self.joint_name[index]}: {value}")
    # 关闭窗口结束程序
    def closeEvent(self, event):
        """关闭窗口时停止线程并释放资源"""
        self.stop_event.set()  # 设置事件，通知线程停止
        self.running = False
        self.udp_thread.join()  # 等待线程退出
        event.accept()

    

    

# 主程序运行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())