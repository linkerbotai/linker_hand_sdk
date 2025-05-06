'''
Author: HJX
Date: 2025-04-08 13:28:18
LastEditors: Please set LastEditors
LastEditTime: 2025-04-09 11:35:22
FilePath: /Linker_Hand_SDK_ROS/src/examples/set_linker_hand_speed/scripts/set_linker_hand_speed.py
Description: 
symbol_custom_string_obkorol_copyright: 
'''
#!/usr/bin/env python3
import rospy,rospkg
import sys
rospack = rospkg.RosPack()
ros_linker_hand_sdk_path = rospack.get_path('linker_hand_sdk_ros')
sys.path.append(ros_linker_hand_sdk_path + '/scripts')
from LinkerHand.core.linker_hand_l20_can import LinkerHandL20Can
from LinkerHand.core.linker_hand_l10_can import LinkerHandL10Can
from LinkerHand.core.linker_hand_l7_can import LinkerHandL7Can
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.color_msg import ColorMsg
class SetLinkerHandSpeed():
    def __init__(self,hand_type="left",speed=[255,255,255,255,255]):
        self.speed = speed
        self.hand_type = hand_type
        self.yaml = LoadWriteYaml()
        self.config = self.yaml.load_setting_yaml()
        if len(self.speed) >7 or len(self.speed) < 5:
            ColorMsg(msg=f"L7速度长度为7，其他速度长度为5的list  当前为{self.speed}", color="red")
            exit()
        self.set_hand_speed()
        
            
        
    def set_hand_speed(self):
        if self.hand_type == "left" and self.config['LINKER_HAND']['LEFT_HAND']['EXISTS']== True:
            # 设置左手速度
            if self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L20":
                self.left_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x28)
                # 设置手速
                self.left_hand_can.set_speed(self.speed)
                self.left_hand_speed = self.left_hand_can.get_speed()
                ColorMsg(msg=f"左手L20速度设置成功{self.left_hand_speed}", color="green")
            elif self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L10":
                self.left_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置手速
                self.left_hand_can.set_speed(self.speed)
                self.left_hand_speed = self.left_hand_can.get_speed()
                ColorMsg(msg=f"左手L10速度设置成功{self.left_hand_speed}", color="green")
            elif self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L7":
                self.left_hand_can = LinkerHandL7Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置手速
                self.left_hand_can.set_speed(self.speed)
                self.left_hand_speed = self.left_hand_can.get_speed()
                ColorMsg(msg=f"左手L10速度设置成功{self.left_hand_speed}", color="green")
            
        if self.hand_type == "right" and self.config['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            # 设置右手速度
            if self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L20":
                self.right_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置手速
                self.right_hand_can.set_speed(self.speed)
                self.right_hand_speed = self.right_hand_can.get_speed()
                ColorMsg(msg=f"右手L20速度设置成功{self.right_hand_speed}", color="green")
            elif self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L10":
                self.right_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置手速
                self.right_hand_can.set_speed(self.speed)
                self.right_hand_speed = self.right_hand_can.get_speed()
                ColorMsg(msg=f"右手L10速度设置成功{self.right_hand_speed}", color="green")
            elif self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L7":
                self.right_hand_can = LinkerHandL7Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置手速
                self.right_hand_can.set_speed(self.speed)
                self.right_hand_speed = self.right_hand_can.get_speed()
                ColorMsg(msg=f"右手L10速度设置成功{self.right_hand_speed}", color="green")
    
    


if __name__ == '__main__':
    '''
    L7:
    rosrun set_linker_hand_speed set_linker_hand_speed.py _hand_type:=right _speed:="[255,255,255,255,255,255,255]"

    other:
    rosrun set_linker_hand_speed set_linker_hand_speed.py _hand_type:=right _speed:="[255,255,255,255,255]"
    '''
    rospy.init_node('get_linker_hand_speed', anonymous=True)
    hand_type = rospy.get_param("~hand_type",default="left") # 设置哪只手的速度
    speed = rospy.get_param('~speed', default=[255,255,255,255,255])  # 默认获取全局参数

    gh = SetLinkerHandSpeed(hand_type=hand_type,speed=speed)
    