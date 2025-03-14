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
from utils.linker_hand_l25_can import LinkerHandL25Can
from utils.color_msg import ColorMsg
from utils.open_can import OpenCan
from utils.load_write_yaml import LoadWriteYaml
global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_name = "linker_hand_sdk_ros"
package_path = rospack.get_path(package_name)

'''
L25的灵巧手新增了失能/使能模式切换
失能模式: 在失能模式下，可以拖动手指，并且实时返回手指状态，目的用于进行同步遥操其他L25的灵巧手
'''
class LinkerHandL25:
    def __init__(self):
        
        self.left_hand = None
        self.right_hand = None
        self.motor_mode = rospy.get_param("~motor_mode", "enable") # 电机失能 | 使能模式参数
        self.thumb_pos,self.index_pos,self.middle_pos,self.ring_pos,self.little_pos = [0.0]*5,[0.0]*5,[0.0]*5,[0.0]*5,[0.0]*5
        #self.load_yaml()
        self.config = LoadWriteYaml().load_setting_yaml()
        self.left_hand_exists = self.config['LINKER_HAND']['LEFT_HAND']['EXISTS']
        self.left_hand_joint = self.config['LINKER_HAND']['LEFT_HAND']['JOINT']
        self.right_hand_exists = self.config['LINKER_HAND']['RIGHT_HAND']['EXISTS']
        self.right_hand_joint = self.config['LINKER_HAND']['RIGHT_HAND']['JOINT']
        self.sdk_version = self.config['VERSION']
        self.password = self.config['PASSWORD']
        time.sleep(0.1)
        ColorMsg(msg=f"SDK version:{self.sdk_version}", color="green")
        self.open_can0()
        time.sleep(0.01)
        self.is_can_up_sysfs()
        
        self.init_left_hand()
        
        self.init_right_hand()
        self.hand_setting_sub = rospy.Subscriber("/cb_hand_setting_cmd", String, self.hand_setting_cb) # 获取灵巧手设置命令
        self.stop_event = threading.Event()  # 创建一个事件对象
        self.hand_state_thread = threading.Thread(target=self.pub_hand_status)
        self.hand_state_thread.daemon = True
        self.hand_state_thread.start()
        self.hand_info_thread = threading.Thread(target=self.pub_hand_info)
        self.hand_info_thread.daemon = True
        self.hand_info_thread.start()
        #self.test_joint()
        # self.pub_hand_status()
        
        
    def test_joint(self):
        pos = [50]* 5
        pos2 = [250] * 5
        count = 0
        t = [250] * 5
        self.right_hand.set_torque(j=t)
        while True:
            fault = self.right_hand.get_fault()
            ColorMsg(msg=f"故障码:{fault}", color="yellow")
            tempe = self.right_hand.get_threshold()
            print("\n")
            ColorMsg(msg=f"温度阈值:{tempe}", color="yellow")
            if count % 2 == 0:
                self.right_hand.set_root1_positions(joint_ranges=pos)
            else:
                self.right_hand.set_root1_positions(joint_ranges=pos2)
            time.sleep(3)
            count = count + 1
        # self.right_hand.action_play()

    # 验证左手配置
    def init_left_hand(self):
        if self.left_hand_exists == True and self.left_hand_joint == "L25":
            self.left_hand=LinkerHandL25Can(config=self.config, can_channel="can0",baudrate=1000000,can_id=0x28)
            if self.motor_mode == "disability":
                # 设置为失能模式
                self.left_hand.set_disability_mode()
                # 失能模式下将手状态发布到控制话题，达到遥操控制其他L25手的效果
                self.left_hand_status_pub = rospy.Publisher("/cb_left_hand_control_cmd",JointState,queue_size=1)
            elif self.motor_mode == "enable":
                # 设置为使用模式
                self.left_hand.set_enable_mode()
                # 设置手指速度0~255
                self.left_hand.set_speed(speed=[100, 250, 250, 250, 250, 250])
                # 设置手掌张开
                self.left_hand.set_joint_positions_by_topic(joint_ranges=[232, 254, 255, 254, 252, 250, 61, 0.0, 10, 40, 189, 0.0, 0.0, 0.0, 0.0, 255, 252, 243, 240, 252, 229, 232, 247, 252, 247])
                self.left_hand_cmd_sub = rospy.Subscriber("/cb_left_hand_control_cmd", JointState,self.left_position_send,queue_size=1)
                self.left_hand_status_pub = rospy.Publisher("/cb_left_hand_state",JointState,queue_size=1)
            self.left_hand_info_pub = rospy.Publisher("/cb_left_hand_info", String, queue_size=10)
        else:
            ColorMsg(msg=f"当前配置left_hand_exists={self.left_hand_exists} left_hand_joint={self.left_hand_joint},不符合左手L25状态", color="red")
            self.left_hand_exists = False
    # 验证右手配置
    def init_right_hand(self):
        if self.right_hand_exists == True and self.right_hand_joint == "L25":
            self.right_hand=LinkerHandL25Can(config=self.config, can_channel="can0",baudrate=1000000,can_id=0x27)
            if self.motor_mode == "disability":
                # 设置为失能模式
                self.right_hand.set_disability_mode()
                # 失能模式下将手状态发布到控制话题，达到遥操控制其他L25手的效果
                self.right_hand_status_pub = rospy.Publisher("/cb_right_hand_control_cmd",JointState,queue_size=1)
            elif self.motor_mode == "enable":
                # 设置为使用模式
                self.right_hand.set_enable_mode()
                # 设置手指速度0~255
                self.right_hand.set_speed(speed=[100, 250, 250, 250, 250, 250])
                # 设置手掌张开
                self.right_hand.set_joint_positions_by_topic(joint_ranges=[232, 254, 255, 254, 252, 250, 61, 0.0, 10, 40, 189, 0.0, 0.0, 0.0, 0.0, 255, 252, 243, 240, 252, 229, 232, 247, 252, 247])
                self.right_hand_cmd_sub = rospy.Subscriber("/cb_right_hand_control_cmd", JointState,self.right_position_send,queue_size=1)
                self.right_hand_status_pub = rospy.Publisher("/cb_right_hand_state",JointState,queue_size=1)
            self.right_hand_info_pub = rospy.Publisher("/cb_right_hand_info", String, queue_size=10)
        else:
            ColorMsg(msg=f"当前配置right_hand_exists={self.right_hand_exists} right_hand_joint={self.right_hand_joint},不符合右手L25状态", color="red")
            self.right_hand_exists = False
        
    def left_position_send(self,msg):
        pos = msg.position
        #self.left_hand.set_joint_positions(joint_ranges=list(pos))
        self.left_hand.set_joint_positions_by_topic(joint_ranges=list(pos))
    def right_position_send(self,msg):
        pos = msg.position
        self.right_hand.set_joint_positions_by_topic(joint_ranges=list(pos))
    def pub_hand_status(self):
        while True:
            self.hand_status()
            #self.hand_info()
            time.sleep(0.015)
    def pub_hand_info(self):
        while True:
            self.hand_info()
            time.sleep(0.01)

    def hand_status(self):
        if self.left_hand != None:
            left_hand_state = self.left_hand.get_current_state_topic()
            if left_hand_state != None and len(left_hand_state) == 25:
                msg = self.create_joint_state_msg(position=left_hand_state)
                self.left_hand_status_pub.publish(msg)
        if self.right_hand != None:
            right_hand_state = self.right_hand.get_current_state_topic()
            if right_hand_state != None and len(right_hand_state) == 25:
                msg = self.create_joint_state_msg(position=right_hand_state)
                self.right_hand_status_pub.publish(msg)


    def hand_info(self):
        if self.left_hand_exists == True:
            data = {
                "left_hand":{
                    "version": self.left_hand.get_version(),
                    "hand_type": self.left_hand_joint,
                    "speed": self.left_hand.get_speed(),
                    #"current": self.left_hand.get_current(),
                    "fault": self.left_hand.get_fault(),
                    #"motor_temperature": self.left_hand.get_temperature()
                }
            }
            m = String()
            m.data = json.dumps(data)
            self.left_hand_info_pub.publish(m)
        if self.right_hand_exists == True:
            data = {
                "left_hand":{
                    "version": self.right_hand.get_version(),
                    "hand_type": self.right_hand_joint,
                    "speed": self.right_hand.get_speed(),
                    #"current": self.right_hand.get_current(),
                    "fault": self.right_hand.get_fault(),
                    #"motor_temperature": self.right_hand.get_temperature()
                }
            }
            m = String()
            m.data = json.dumps(data)
            self.right_hand_info_pub.publish(m)
            


    
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
        if data["setting_cmd"] == "set_speed": # 设置速度
            if isinstance(data["params"]["speed"], list) == True:
                speed = data["params"]["speed"]
            else:
                speed = [int(data["params"]["speed"])] * 5
            if hand_left == True:
                self.left_hand.set_speed(speed)
            if hand_right == True:
                self.right_hand.set_speed(speed)

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
        self.stop_event.set()
        # self.lh_l.close_can_interface()
        # self.lh_r.close_can_interface()
        # self.shutdown_flag.set()
        # self.can_left_thread.join()
        # self.can_right_thread.join()
    
def signal_handler(sig, frame):
    m = String()
    d = {
        "close_sdk":True
    }
    m.data = json.dumps(d)
    for i in range(2):
        pub.publish(m)
        time.sleep(0.01)
    """关闭 can0 接口"""
    can.close_can0()
    sys.exit(0)  # 正常退出程序
if __name__ == '__main__':
    rospy.init_node('linker_hand_sdk', anonymous=True)
    rospy.Rate(60)
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill 命令
    pub = rospy.Publisher('/close_sdk', String, queue_size=10)
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
        linker_hand = LinkerHandL25()
        rospy.spin()
    except rospy.ROSInterruptException:
        #linker_hand.shutdown()
        rospy.loginfo("Node shutdown complete.")
    