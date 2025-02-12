#!/usr/bin/env python3
import rospy,rospkg
import time,os,sys,json
from std_msgs.msg import String,Header, Float32MultiArray
from sensor_msgs.msg import JointState

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
'''
示例测试命令
rosrun set_linker_hand_current set_linker_hand_current.py _hand_type:=right _current:=80
'''
class SetLinkerHandCurrent():
    def __init__(self,hand_type="left",current=200):
        self.current = [current] * 5
        self.hand_type = hand_type
        self.yaml = LoadWriteYaml()
        self.config = self.yaml.load_setting_yaml()
        self.set_hand_current()

    def set_hand_current(self):
        if self.hand_type == "left" and self.config['LINKER_HAND']['LEFT_HAND']['EXISTS']== True:
            # 设置左手速度
            if self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L20":
                self.left_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x28, config=self.config)
                # 设置手速
                self.left_hand_can.set_electric_current(self.current)
                self.left_hand_current = self.left_hand_can.get_current()
                ColorMsg(msg=f"左手L20电流阈值设置成功{self.left_hand_current}", color="green")
            elif self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L10":
                ColorMsg(msg=f"L10暂时不能设置电流阈值", color="red")
            
        if self.hand_type == "right" and self.config['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            # 设置右手速度
            if self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L20":
                self.right_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x27, config=self.config)
                # 设置手速
                self.right_hand_can.set_electric_current(self.current)
                self.right_hand_current = self.right_hand_can.get_current()
                ColorMsg(msg=f"右手L20电流阈值设置成功{self.right_hand_current}", color="green")
            elif self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L10":
                ColorMsg(msg=f"L10暂时不能设置电流阈值", color="red")


if __name__ == '__main__':
    rospy.init_node('get_linker_hand_current', anonymous=True)
    ColorMsg(msg=f"请勿将电流阈值设置过大，避免损坏电机。默认值为:42", color="yellow")
    hand_type = rospy.get_param("~hand_type",default="left") # 设置哪只手的速度
    current = rospy.get_param('~current', default=42)  # 默认获取全局参数

    lhc = SetLinkerHandCurrent(hand_type=hand_type,current=current)