#!/usr/bin/env python3
import rospy,rospkg
import signal
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import can
import json
import yaml
import time
import threading
import sys
import os
import subprocess
from std_msgs.msg import Header, Float32MultiArray
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.linker_hand_t24_can import LinkerHandT24Can
from utils.color_msg import ColorMsg
from utils.open_can import OpenCan
global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_name = "linker_hand_sdk_ros"
package_path = rospack.get_path(package_name)

'''
T24的灵巧手新增了失能/使能模式切换
失能模式: 在失能模式下，可以拖动手指，并且实时返回手指状态，目的用于进行同步遥操其他T24的灵巧手
'''
class LinkerHandT24:
    def __init__(self):
        self.left_hand = None
        self.right_hand = None
        self.motor_mode = rospy.get_param("~motor_mode", "enable") # 电机失能 | 使能模式参数
        self.thumb_pos,self.index_pos,self.middle_pos,self.ring_pos,self.little_pos = [0.0]*5,[0.0]*5,[0.0]*5,[0.0]*5,[0.0]*5
        self.load_yaml()
        time.sleep(0.1)
        ColorMsg(msg=f"SDK version:{self.sdk_version}", color="green")
        self.open_can0()
        time.sleep(0.01)
        self.is_can_up_sysfs()
        
        self.check_left_hand()
        self.init_right_hand()
        
        self.pub_hand_status()

    # 验证左手配置
    def check_left_hand(self):
        if self.left_hand_exists == True and self.left_hand_joint == "T24":
            self.left_hand=LinkerHandT24Can(config=self.config, can_channel="can0",baudrate=1000000,can_id=0x28)
            if self.motor_mode == "disability":
                # 设置为失能模式
                self.left_hand.set_disability_mode()
                # 失能模式下将手状态发布到控制话题，达到遥操控制其他T24手的效果
                self.left_hand_status_pub = rospy.Publisher("/cb_left_hand_control_cmd",JointState,queue_size=10)
            elif self.motor_mode == "enable":
                # 设置为使用模式
                self.left_hand.set_enable_mode()
                # 设置手指速度0~255
                self.left_hand.set_speed(speed=180)
                # 设置手掌张开
                self.left_hand.set_joint_positions(joint_ranges=[232, 254, 255, 254, 252, 250, 61, 0.0, 10, 40, 189, 0.0, 0.0, 0.0, 0.0, 255, 252, 243, 240, 252, 229, 232, 247, 252, 247])
                self.left_hand_cmd_sub = rospy.Subscriber("/cb_left_hand_control_cmd", JointState,self.left_position_send,queue_size=10)
                self.left_hand_status_pub = rospy.Publisher("/cb_left_hand_state",JointState,queue_size=10)
        else:
            ColorMsg(msg=f"当前配置left_hand_exists={self.left_hand_exists} left_hand_joint={self.left_hand_joint},不符合左手T24状态", color="red")
    # 验证右手配置
    def init_right_hand(self):
        if self.right_hand_exists == True and self.right_hand_joint == "T24":
            self.right_hand=LinkerHandT24Can(config=self.config, can_channel="can0",baudrate=1000000,can_id=0x27)
            if self.motor_mode == "disability":
                # 设置为失能模式
                self.right_hand.set_disability_mode()
                # 失能模式下将手状态发布到控制话题，达到遥操控制其他T24手的效果
                self.right_hand_status_pub = rospy.Publisher("/cb_right_hand_control_cmd",JointState,queue_size=10)
            elif self.motor_mode == "enable":
                # 设置为使用模式
                self.right_hand.set_enable_mode()
                # 设置手指速度0~255
                self.right_hand.set_speed(speed=180)
                # 设置手掌张开
                self.right_hand.set_joint_positions(joint_ranges=[232, 254, 255, 254, 252, 250, 61, 0.0, 10, 40, 189, 0.0, 0.0, 0.0, 0.0, 255, 252, 243, 240, 252, 229, 232, 247, 252, 247])
                self.right_hand_cmd_sub = rospy.Subscriber("/cb_right_hand_control_cmd", JointState,self.right_position_send,queue_size=10)
                self.right_hand_status_pub = rospy.Publisher("/cb_right_hand_state",JointState,queue_size=10)
        else:
            ColorMsg(msg=f"当前配置left_hand_exists={self.right_hand_exists} left_hand_joint={self.right_hand_joint},不符合右手T24状态", color="red")
            
            time.sleep(0.1)
        self.hand_setting_sub = rospy.Subscriber("/cb_hand_setting_cmd", String, self.hand_setting_cb) # 获取灵巧手设置命令
    def left_position_send(self,msg):
        pos = msg.position
        self.left_hand.set_joint_positions(joint_ranges=list(pos))
    def right_position_send(self,msg):
        pos = msg.position
        self.right_hand.set_joint_positions(joint_ranges=list(pos))
    def pub_hand_status(self):
        while True:
            self.get_hand_status()

    def get_hand_status(self):
        if self.left_hand != None:
            left_hand_state = self.left_hand.get_current_status()
            if left_hand_state != None and len(left_hand_state) == 25:
                msg = self.create_joint_state_msg(position=left_hand_state)
                self.left_hand_status_pub.publish(msg)
        if self.right_hand != None:
            right_hand_state = self.right_hand.get_current_status()
            if right_hand_state != None and len(right_hand_state) == 25:
                msg = self.create_joint_state_msg(position=right_hand_state)
                self.right_hand_status_pub.publish(msg)
    
    def create_joint_state_msg(self, position, names=[]):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.name = names
        msg.position = list(map(float, position))
        msg.velocity = [0.0] * len(position)
        msg.effort = [0.0] * len(position)
        return msg
    def hand_setting_cb(self, msg):
        hand_left, hand_right = False, False
        data = json.loads(msg.data)
        print(f"收到设置命令：{data}")
        if data["params"]["hand_type"] == "left" and self.left_hand_exists:
            hand_left = True
        elif data["params"]["hand_type"] == "right" and self.right_hand_exists:
            hand_right = True
        else:
            print("请指定要设定的手部位")
            return
        if data["setting_cmd"] == "set_disability": # 设置失能模式
            # rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_disability\",\"params\":{\"hand_type\":\"right\"}}"}'   参数说明：hand_type:left | right
            if hand_left == True:
                self.left_hand.set_disability_mode()
            if hand_right == True:
                self.right_hand.set_disability_mode()
        if data["setting_cmd"] == "set_enable": # 设置失能模式
            # rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_enable\",\"params\":{\"hand_type\":\"right\"}}"}'   参数说明：hand_type:left | right
            if hand_left == True:
                self.left_hand.set_enable_mode()
            if hand_right == True:
                self.right_hand.set_enable_mode()

    def load_yaml(self):
        try:
            settings_yaml_path = package_path + "/config/setting.yaml"
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
    def open_can0(self):
        try:
            # 检查 can0 接口是否已存在并处于 up 状态
            result = subprocess.run(
                ["ip", "link", "show", "can0"],
                check=True,
                text=True,
                capture_output=True
            )
            if "state UP" in result.stdout:
                rospy.loginfo("CAN接口已经是 UP 状态")
                return
            # 如果没有处于 UP 状态，则配置接口
            subprocess.run(
                ["sudo", "-S", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "1000000"],
                input=f"{self.password}\n",
                check=True,
                text=True,
                capture_output=True
            )
            rospy.loginfo("CAN接口设置成功")
        except subprocess.CalledProcessError as e:
            rospy.logerr(f"CAN接口设置失败: {e.stderr}")
        except Exception as e:
            rospy.logerr(f"发生错误: {str(e)}")

    def is_can_up_sysfs(self, interface="can0"):
    # 检查接口目录是否存在
        if not os.path.exists(f"/sys/class/net/{interface}"):
            return False
        # 读取接口状态
        try:
            with open(f"/sys/class/net/{interface}/operstate", "r") as f:
                state = f.read().strip()
            if state == "up":
                self.can_status = True
            return self.can_status
        except Exception as e:
            print(f"Error reading CAN interface state: {e}")
            return False
    def shutdown(self):
        # self.lh_l.close_can_interface()
        # self.lh_r.close_can_interface()
        # self.shutdown_flag.set()
        # self.can_left_thread.join()
        # self.can_right_thread.join()
        pass
    
def signal_handler(sig, frame):
    # rospy.loginfo("Shutting down ROS node...")
    # rospy.signal_shutdown("SIGINT received")
    # rospy.on_shutdown()
    sys.exit(0)  # 正常退出程序
if __name__ == '__main__':
    rospy.init_node('linker_hand_sdk', anonymous=True)
    rospy.Rate(60)
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill 命令
    
    try:
        # 检查can端口如果没有打开则等待重试，一般是usb转can设备没有插上
        while True:
            can = OpenCan()
            can.open_can0()
            time.sleep(0.001)
            o = can.is_can_up_sysfs()
            if o == False:
                ColorMsg(msg=f"can0端口打开失败，3秒后自动重试", color="red")
                time.sleep(3)
            else:
                break
        linker_hand = LinkerHandT24()
        rospy.spin()
    except rospy.ROSInterruptException:
        linker_hand.shutdown()
        rospy.loginfo("Node shutdown complete.")