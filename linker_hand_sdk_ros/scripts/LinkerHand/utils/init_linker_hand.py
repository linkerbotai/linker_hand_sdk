'''
Author: HJX
Date: 2025-04-01 14:09:21
LastEditors: Please set LastEditors
LastEditTime: 2025-04-08 11:18:23
FilePath: /Linker_Hand_SDK_ROS/src/linker_hand_sdk_ros/scripts/LinkerHand/utils/init_linker_hand.py
Description: 
symbol_custom_string_obkorol_copyright: 
'''
import yaml, os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from load_write_yaml import LoadWriteYaml

class InitLinkerHand():
    def __init__(self):
        self.yaml = LoadWriteYaml()
        self.setting = self.yaml.load_setting_yaml()

    def current_hand(self):
        '''
        初始化灵巧手
        return: hand_joint str L7/L10/L20/L21/L25, hand_type str left or right
        '''
        # 左手是否配置
        self.left_hand = None
        self.left_hand_joint = None
        self.left_hand_type = None
        self.left_hand_force = None
        self.left_hand_pose = None
        self.left_hand_torque = [200, 200, 200, 200, 200]
        self.left_hand_speed = [80, 200, 200, 200, 200]
        # 右手是否配置
        self.right_hand = None
        self.right_hand_joint = None
        self.right_hand_type = None
        self.right_hand_force = None
        self.right_hand_pose = None
        self.right_hand_torque = [200, 200, 200, 200, 200]
        self.right_hand_speed = [80, 200, 200, 200, 200]
        if self.setting['LINKER_HAND']['LEFT_HAND']['EXISTS'] == True:
            self.left_hand = True
            self.left_hand_joint = self.setting['LINKER_HAND']['LEFT_HAND']['JOINT']
            self.left_hand_type = "left"
            self.left_hand_force = self.setting['LINKER_HAND']['LEFT_HAND']['TOUCH']
            if self.left_hand_joint == "L7":
                # The data length of L7 is 7, reinitialize here
                self.left_hand_pose = [255, 200, 255, 255, 255, 255, 180]
                self.left_hand_torque = [250, 250, 250, 250, 250, 250, 250]
                self.left_hand_speed = [120, 180, 180, 180, 180, 180, 180]
            elif self.left_hand_joint == "L10":
                self.left_hand_pose = [255, 200, 255, 255, 255, 255, 180, 180, 180, 41]
            elif self.left_hand_joint == "L20":
                self.left_hand_pose = [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255]
            elif self.left_hand_joint == "L21":
                self.left_hand_pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
            elif self.left_hand_joint == "L25":
                self.left_hand_pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        # 判断右手是否配置 
        if self.setting['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            self.right_hand = True
            self.right_hand_joint = self.setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
            self.right_hand_type = "right"
            self.right_hand_force = self.setting['LINKER_HAND']['RIGHT_HAND']['TOUCH']
            if self.right_hand_joint == "L7":
                # The data length of L7 is 7, reinitialize here
                self.right_hand_pose = [255, 200, 255, 255, 255, 255, 180]
                self.right_hand_torque = [250, 250, 250, 250, 250, 250, 250]
                self.right_hand_speed = [120, 250, 250, 250, 250, 250, 250]
            elif self.right_hand_joint == "L10":
                self.right_hand_pose = [255, 200, 255, 255, 255, 255, 180, 180, 180, 41]
            elif self.right_hand_joint == "L20":
                self.right_hand_pose = [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255]
            elif self.right_hand_joint == "L21":
                self.right_hand_pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
            elif self.right_hand_joint == "L25":
                self.right_hand_pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]


        return self.left_hand ,self.left_hand_joint ,self.left_hand_type ,self.left_hand_force,self.left_hand_pose, self.left_hand_torque, self.left_hand_speed ,self.right_hand ,self.right_hand_joint ,self.right_hand_type ,self.right_hand_force,self.right_hand_pose, self.right_hand_torque, self.right_hand_speed,self.setting

        