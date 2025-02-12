#!/usr/bin/env python3
import rospy,rospkg
import time,os,sys,json
from std_msgs.msg import String,Header, Float32MultiArray
from sensor_msgs.msg import JointState

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from utils.color_msg import ColorMsg

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 找到上上级目录
target_dir = os.path.abspath(os.path.join(current_dir, "../../.."))

# 添加到 sys.path
sys.path.append(target_dir)
from linker_hand_sdk_ros.scripts.utils.linker_hand_l20_can import LinkerHandL20Can
from linker_hand_sdk_ros.scripts.utils.linker_hand_l10_can import LinkerHandL10Can
from linker_hand_sdk_ros.scripts.utils.load_write_yaml import LoadWriteYaml
from linker_hand_sdk_ros.scripts.utils.color_msg import ColorMsg
class SetLinkerHandSpeed():
    def __init__(self,hand_type="left",speed=[255,255,255,255,255]):
        self.speed = speed
        self.hand_type = hand_type
        self.yaml = LoadWriteYaml()
        self.config = self.yaml.load_setting_yaml()
        if len(self.speed) != 5:
            ColorMsg(msg=f"速度必须是长度为5的list，例如:[255,255,255,255,255]     当前为{self.speed}", color="red")
            exit()
        self.set_hand_speed()
        
            
        
    def set_hand_speed(self):
        if self.hand_type == "left" and self.config['LINKER_HAND']['LEFT_HAND']['EXISTS']== True:
            # 设置左手速度
            if self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L20":
                self.left_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x28, config=self.config)
                # 设置手速
                self.left_hand_can.set_joint_speed(self.speed)
                self.left_hand_speed = self.left_hand_can.get_speed()
                ColorMsg(msg=f"左手L20速度设置成功{self.left_hand_speed}", color="green")
            elif self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L10":
                self.left_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x27, config=self.config)
                # 设置手速
                self.left_hand_can.set_joint_speed_l10(self.speed)
                self.left_hand_speed = self.left_hand_can.get_speed()
                ColorMsg(msg=f"左手L10速度设置成功{self.left_hand_speed}", color="green")
            
        if self.hand_type == "right" and self.config['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            # 设置右手速度
            if self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L20":
                self.right_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x27, config=self.config)
                # 设置手速
                self.right_hand_can.set_joint_speed(self.speed)
                self.right_hand_speed = self.right_hand_can.get_speed()
                ColorMsg(msg=f"右手L20速度设置成功{self.right_hand_speed}", color="green")
            elif self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L10":
                self.right_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x27, config=self.config)
                # 设置手速
                self.right_hand_can.set_joint_speed_l10(self.speed)
                self.right_hand_speed = self.right_hand_can.get_speed()
                ColorMsg(msg=f"右手L10速度设置成功{self.right_hand_speed}", color="green")
    
    


if __name__ == '__main__':
    rospy.init_node('get_linker_hand_speed', anonymous=True)
    hand_type = rospy.get_param("~hand_type",default="left") # 设置哪只手的速度
    speed = rospy.get_param('~speed', default=[255,255,255,255,255])  # 默认获取全局参数

    gh = SetLinkerHandSpeed(hand_type=hand_type,speed=speed)
    