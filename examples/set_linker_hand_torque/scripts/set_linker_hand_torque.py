'''
Author: HJX
Date: 2025-04-08 13:28:18
LastEditors: Please set LastEditors
LastEditTime: 2025-04-09 11:41:59
FilePath: /Linker_Hand_SDK_ROS/src/examples/set_linker_hand_torque/scripts/set_linker_hand_torque.py
Description: 
symbol_custom_string_obkorol_copyright: 
'''
#!/usr/bin/env python3
import rospy,rospkg
import time,os,sys,json
from std_msgs.msg import String,Header, Float32MultiArray
from sensor_msgs.msg import JointState

rospack = rospkg.RosPack()
ros_linker_hand_sdk_path = rospack.get_path('linker_hand_sdk_ros')
sys.path.append(ros_linker_hand_sdk_path + '/scripts')
from LinkerHand.core.linker_hand_l20_can import LinkerHandL20Can
from LinkerHand.core.linker_hand_l10_can import LinkerHandL10Can
from LinkerHand.core.linker_hand_l7_can import LinkerHandL7Can
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.color_msg import ColorMsg
class SetLinkerHandTorque():
    def __init__(self,hand_type="left",torque=[180,180,180,180,180]):
        self.torque = torque
        self.hand_type = hand_type
        self.yaml = LoadWriteYaml()
        self.config = self.yaml.load_setting_yaml()
        if len(self.torque) != 5 and len(self.torque) != 7:
            ColorMsg(msg=f"扭矩必须是长度为5的list，例如:[255,255,255,255,255]     当前为{self.torque}", color="red")
            exit()
        self.set_hand_torque()
        
            
        
    def set_hand_torque(self):
        if self.hand_type == "left" and self.config['LINKER_HAND']['LEFT_HAND']['EXISTS']== True:
            # 设置左手扭矩
                
            if self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L10":
                self.left_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x28)
                # 设置扭矩
                self.left_hand_can.set_torque(self.torque)
                ColorMsg(msg=f"左手L10扭矩设置成功{self.torque}", color="green")
            elif self.config['LINKER_HAND']['LEFT_HAND']['JOINT'] == "L7":
                self.left_hand_can = LinkerHandL7Can(can_channel="can0", baudrate=1000000, can_id=0x28)
                # 设置扭矩
                self.left_hand_can.set_torque(self.torque)
                ColorMsg(msg=f"左手L7扭矩设置成功{self.torque}", color="green")
            
        if self.hand_type == "right" and self.config['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            # 设置右手扭矩
            if self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L10":
                self.right_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置扭矩
                self.right_hand_can.set_torque(self.torque)
                ColorMsg(msg=f"右手L10扭矩设置成功{self.torque}", color="green")
            elif self.config['LINKER_HAND']['RIGHT_HAND']['JOINT'] == "L7":
                self.right_hand_can = LinkerHandL7Can(can_channel="can0", baudrate=1000000, can_id=0x27)
                # 设置扭矩
                self.right_hand_can.set_torque(self.torque)
                ColorMsg(msg=f"右手L7扭矩设置成功{self.torque}", color="green")
    
    


if __name__ == '__main__':
    rospy.init_node('set_linker_hand_torque', anonymous=True)
    ColorMsg(msg="当前支持L7/L10")
    hand_type = rospy.get_param("~hand_type",default="left") # 设置哪只手的扭矩
    torque = rospy.get_param('~torque', default=[180,180,180,180,180])  # 默认获取全局参数

    gh = SetLinkerHandTorque(hand_type=hand_type,torque=torque)
    