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
        return: hand_joint str L7/L10/L20/L25, hand_type str left or right
        '''
        # 判断左手是否配置
        self.left_hand = None
        self.left_hand_joint = None
        self.left_hand_type = None
        self.left_hand_force = None
        self.right_hand = None
        self.right_hand_joint = None
        self.right_hand_type = None
        self.right_hand_force = None
        if self.setting['LINKER_HAND']['LEFT_HAND']['EXISTS'] == True:
            self.left_hand = True
            self.left_hand_joint = self.setting['LINKER_HAND']['LEFT_HAND']['JOINT']
            self.left_hand_type = "left"
            self.left_hand_force = self.setting['LINKER_HAND']['LEFT_HAND']['TOUCH']
        # 判断右手是否配置
        if self.setting['LINKER_HAND']['RIGHT_HAND']['EXISTS'] == True:
            self.right_hand = True
            self.right_hand_joint = self.setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
            self.right_hand_type = "right"
            self.right_hand_force = self.setting['LINKER_HAND']['RIGHT_HAND']['TOUCH']
        # # gui控制只支持单手，这里进行左右手互斥
        # if self.left_hand == True and self.right_hand == True:
        #     self.left_hand = True
        #     self.right_hand = False
        # if self.left_hand == True:
        #     print("左手")
        #     self.hand_exists = True
        #     self.hand_joint = self.setting['LINKER_HAND']['LEFT_HAND']['JOINT']
        #     self.hand_type = "left"
        # if self.right_hand == True:
        #     print("右手")
        #     self.hand_exists = True
        #     self.hand_joint = self.setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
        #     self.hand_type = "right"
        # return self.hand_joint, self.hand_type
        return self.left_hand ,self.left_hand_joint ,self.left_hand_type ,self.left_hand_force ,self.right_hand ,self.right_hand_joint ,self.right_hand_type ,self.right_hand_force,self.setting

        