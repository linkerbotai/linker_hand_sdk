from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QWidget
from PyQt5.QtCore import Qt
import rospy, rospkg, yaml
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import sys
import threading
global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_sdk = "linker_hand_sdk_ros"
sdk_path = rospack.get_path(package_sdk)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化 ROS 节点
        rospy.init_node('gui_control', anonymous=True)
        self.load_yaml()
        hand_joint = rospy.get_param('~hand_joint', default="L20")  # 默认获取全局参数
        hand_type = rospy.get_param('~hand_type', default="left")  # 默认获取全局参数
        self.hand_type = hand_type
        if hand_joint == "L25":
            # L25
            self.joint_name = ["拇指根部", "食指根部", "中指根部", "无名指根部","预留","拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","预留","拇指横摆","预留","预留","预留","预留","拇指中部","食指中部","中指中部","无名指中部","预留","拇指尖部","食指尖部","中指尖部","无名指尖部","预留"]
        elif hand_joint == "L20":
            # L20
            self.joint_name = ["拇指根部", "食指根部", "中指根部", "无名指根部","小指根部","拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","小指侧摆","拇指横摆","预留","预留","预留","预留","拇指尖部","食指末端","中指末端","无名指末端","小指末端"]
        elif hand_joint == "L10":
            # L10
            self.joint_name = ["拇指根部", "拇指侧摆","食指根部", "中指根部", "无名指根部","小指根部","食指侧摆","无名指侧摆","小指侧摆","拇指横摆"]

        self.setWindowTitle(f"hand:{self.hand_type} {hand_joint} joint Control - Qt5 with ROS")
        self.setGeometry(100, 100, 500, 800)
        if self.hand_type == "left":
            self.hand_pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)
        elif self.hand_type == "right":
            self.hand_pub = rospy.Publisher('/cb_right_hand_control_cmd', JointState, queue_size=10)
        self.rate = rospy.Rate(100)  # 100 Hz

        # 主窗口容器
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建垂直布局
        layout = QVBoxLayout(central_widget)

        # 存储滑动条和标签
        self.sliders = []
        self.labels = []

        # 创建25个滑动条
        for i in range(len(self.joint_name)):
            # 每个滑动条和标签的水平布局
            slider_layout = QHBoxLayout()

            # 标签显示滑动条的值
            label = QLabel(f"{self.joint_name[i]}: 255", self)
            self.labels.append(label)
            slider_layout.addWidget(label)

            # 滑动条
            slider = QSlider(Qt.Horizontal, self)
            slider.setRange(0, 255)
            slider.setValue(255)
            slider.setFixedHeight(15)  # 设置滑动条高度为15
            slider.valueChanged.connect(lambda value, index=i: self.update_label(index, value))
            self.sliders.append(slider)
            slider_layout.addWidget(slider)

            # 添加到主布局
            layout.addLayout(slider_layout)

        # 每秒发送 100 次
        self.running = True
        self.udp_thread = threading.Thread(target=self.send_ros_data)
        self.udp_thread.start()

    def send_ros_data(self):
        while self.running and not rospy.is_shutdown():
            slider_values = [slider.value() for slider in self.sliders]
            data = ",".join(map(str, slider_values))
            msg = self.joint_msg(data)
            print(msg.position)
            self.hand_pub.publish(msg)
            self.rate.sleep()

    def joint_msg(self, data):
        """创建 JointState 消息"""
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.name = []
        msg.position = [float(i) for i in data.split(",")]
        return msg

    def update_label(self, index, value):
        self.labels[index].setText(f"{self.joint_name[index]}: {value}")

    def closeEvent(self, event):
        """关闭窗口时停止线程并释放资源"""
        self.running = False
        self.udp_thread.join()  # 等待线程退出
        event.accept()


    def load_yaml(self):
        try:
            settings_yaml_path = sdk_path + "/config/setting.yaml"
            with open(settings_yaml_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                self.config = config
                self.sdk_version = config["VERSION"]
                self.left_hand_exists = config['LINKER_HAND']['LEFT_HAND']['EXISTS']
                self.left_hand_names = config['LINKER_HAND']['LEFT_HAND']['NAME']
                self.left_hand_joint = config['LINKER_HAND']['LEFT_HAND']['JOINT']
                self.left_hand_force = config['LINKER_HAND']['LEFT_HAND']['TOUCH']
                self.right_hand_exists = config['LINKER_HAND']['RIGHT_HAND']['EXISTS']
                self.right_hand_names = config['LINKER_HAND']['RIGHT_HAND']['NAME']
                self.right_hand_joint = config['LINKER_HAND']['RIGHT_HAND']['JOINT']
                self.right_hand_force = config['LINKER_HAND']['RIGHT_HAND']['TOUCH']
                self.password = config['PASSWORD']
        except Exception as e:
            rospy.logerr(f"Error reading setting.yaml: {e}")
# 主程序运行
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())