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
global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_name = "linker_hand_sdk_ros"
package_path = rospack.get_path(package_name)

'''
注：L25双右手遥操模式为内部测试，尽量不要使用。
L25的灵巧手被操控模块。本模块切勿与linker_hand_sdk_ros在同一机器上使用。
ROS主启动linker_hand_sdk_ros和examples/L25目录下python set_remote_control.py --hand_type=right
ROS从机启动本ROS模块
rosrun be_manipulated be_manipulated.py
'''
class BeManipulated:
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
        self.manipulated_right()
    def manipulated_right(self):
        self.right_hand=LinkerHandL25Can(config=self.config, can_channel="can0",baudrate=1000000,can_id=0x27)
        self.right_hand.set_enable_mode()
        # 设置手指速度0~255
        self.right_hand.set_speed(speed=255)
        self.right_hand_cmd_sub = rospy.Subscriber("/cb_right_hand_control_cmd", JointState,self.right_position_send,queue_size=10)
    
        
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
        pass
    
def signal_handler(sig, frame):
    sys.exit(0)  # 正常退出程序
if __name__ == '__main__':
    rospy.init_node('be_manipulated', anonymous=True)
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
        linker_hand = BeManipulated()
        rospy.spin()
    except rospy.ROSInterruptException:
        linker_hand.shutdown()
        rospy.loginfo("Node shutdown complete.")