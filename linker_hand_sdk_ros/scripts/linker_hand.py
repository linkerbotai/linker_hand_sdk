#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
'''
Author: HJX
Date: 2025-04-08 09:07:49
LastEditors: Please set LastEditors
LastEditTime: 2025-04-11 09:15:56
FilePath: /Linker_Hand_SDK_ROS/src/linker_hand_sdk_ros/scripts/linker_hand.py
Description: 
symbol_custom_string_obkorol_copyright: 
'''
import rospy, signal, rospkg, sys, os, math, time, threading, json
import numpy as np
from std_msgs.msg import String, Header, Float32MultiArray
from sensor_msgs.msg import JointState
from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.color_msg import ColorMsg
from LinkerHand.utils.open_can import OpenCan

class LinkerHand:
    def __init__(self):
        rospy.init_node('linker_hand_sdk', anonymous=True)
        OpenCan().open_can0()
        self.rate = rospy.Rate(60)
        self.left_vel,self.right_vel = [],[]
        self.left_hand, self.left_hand_joint, self.left_hand_type, self.left_hand_force, self.right_hand, self.right_hand_joint, self.right_hand_type, self.right_hand_force, self.setting = InitLinkerHand().current_hand()
        self._init_topic()
        self.hand_setting_sub = rospy.Subscriber("/cb_hand_setting_cmd", String, self.hand_setting_cb)
        # 开启线程发布手的状态
        self.thread = threading.Thread(target=self.publish_hand_state)
        # 设置为守护线程，主程序退出时，线程也退出
        self.thread.daemon = True
        # 启动线程
        self.thread.start()
        rospy.spin()

    def _init_topic(self):
        if self.left_hand == True:
            self.init_left_hand()
            # Left LinkerHand控制话题
            self.left_hand_cmd_sub = rospy.Subscriber("/cb_left_hand_control_cmd", JointState, self.left_hand_cb, queue_size=1)
            # Left LinkerHand状态发布话题
            self.left_hand_state_pub = rospy.Publisher('/cb_left_hand_state', JointState, queue_size=10)
            # Left LinkerHand电机温度、当前速度、当前扭矩、当前电机故障码、压力传感器等数据发布话题
            self.left_hand_info_pub = rospy.Publisher("/cb_left_hand_info", String, queue_size=10)
            if self.left_hand_force == True:
                # Left LinkerHand压力传感器数据发布话题
                self.left_hand_pressure_pub = rospy.Publisher("/cb_left_hand_force", Float32MultiArray, queue_size=10)
        if self.right_hand == True:
            self.init_right_hand()
            # Right LinkerHand控制话题
            self.right_hand_cmd_sub = rospy.Subscriber("/cb_right_hand_control_cmd", JointState, self.right_hand_cb, queue_size=1)
            # Right LinkerHand状态发布话题
            self.right_hand_state_pub = rospy.Publisher('/cb_right_hand_state', JointState, queue_size=10)
            # Right LinkerHand电机温度、当前速度、当前扭矩、当前电机故障码、压力传感器等数据发布话题
            self.right_hand_info_pub = rospy.Publisher("/cb_right_hand_info", String, queue_size=10)
            if self.right_hand_force == True:
                # Right LinkerHand压力传感器数据发布话题
                self.right_hand_pressure_pub = rospy.Publisher("/cb_right_hand_force", Float32MultiArray, queue_size=10)
                
    def init_left_hand(self):
        pose = None
        torque = [200, 200, 200, 200, 200]
        speed = [80, 200, 200, 200, 200]
        if self.left_hand_joint == "L7":
            self.left_hand_api = LinkerHandApi(hand_type="left", hand_joint="L7")
            # The data length of L7 is 7, reinitialize here
            pose = [255, 200, 255, 255, 255, 255, 180]
            torque = [250, 250, 250, 250, 250, 250, 250]
            speed = [120, 180, 180, 180, 180, 180, 180]
        elif self.left_hand_joint == "L10":
            self.left_hand_api = LinkerHandApi(hand_type="left", hand_joint="L10")
            pose = [255, 200, 255, 255, 255, 255, 180, 180, 180, 41]
        elif self.left_hand_joint == "L20":
            self.left_hand_api = LinkerHandApi(hand_type="left", hand_joint="L20")
            pose = [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255]
        elif self.left_hand_joint == "L25":
            self.left_hand_api = LinkerHandApi(hand_type="left", hand_joint="L25")
            pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
            
        else:
            ColorMsg(msg=f"Left hand joint type error, please check the configuration file", color="red")
            sys.exit(1)
        if pose is not None:
            self.left_hand_api.set_speed(speed=speed)
            self.left_hand_api.set_torque(torque=torque)
            self.left_hand_api.finger_move(pose=pose)

    def init_right_hand(self):
        pose = None
        torque = [200, 200, 200, 200, 200]
        speed = [120, 200, 200, 200, 200]
        if self.right_hand_joint == "L7":
            self.right_hand_api = LinkerHandApi(hand_type="right", hand_joint="L7")
            # The data length of L7 is 7, reinitialize here
            pose = [255, 200, 255, 255, 255, 255, 180]
            torque = [250, 250, 250, 250, 250, 250, 250]
            speed = [120, 250, 250, 250, 250, 250, 250]
        elif self.right_hand_joint == "L10":
            self.right_hand_api = LinkerHandApi(hand_type="right", hand_joint="L10")
            pose = [255, 200, 255, 255, 255, 255, 180, 180, 180, 41]
        elif self.right_hand_joint == "L20":
            self.right_hand_api = LinkerHandApi(hand_type="right", hand_joint="L20")
            pose = [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255]
        elif self.right_hand_joint == "L25":
            self.right_hand_api = LinkerHandApi(hand_type="right", hand_joint="L25")
            pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        else:
            ColorMsg(msg=f"Right hand joint type error, please check the configuration file", color="red")
            sys.exit(1)
        if pose is not None:
            self.right_hand_api.set_speed(speed=speed)
            self.right_hand_api.set_torque(torque=torque)
            self.right_hand_api.finger_move(pose=pose)

    def publish_hand_state(self):
        rate = 1.0 / 60  # 60 FPS
        while not rospy.is_shutdown():
            if self.left_hand == True:
                state = self.left_hand_api.get_state()
                left_vel = self.left_hand_api.get_joint_speed()
                if all(x == 0 for x in  self.left_vel):
                    self.left_hand_state_pub.publish(self.joint_state_msg(state,[0]*len(state)))
                else:
                    self.left_hand_state_pub.publish(self.joint_state_msg(state,left_vel))
                left_info_msg = String()
                left_info_msg.data = json.dumps(self.hand_info(hand_type="left"))
                self.left_hand_info_pub.publish(left_info_msg)
                if self.left_hand_force == True:
                    force = self.left_hand_api.get_force()
                    t_force = [item for sublist in force for item in sublist]
                    left_force_msg = Float32MultiArray()
                    left_force_msg.data = t_force
                    self.left_hand_pressure_pub.publish(left_force_msg)
            if self.right_hand == True:
                state = self.right_hand_api.get_state()
                if all(x == 0 for x in  self.left_vel):
                    right_vel = self.right_hand_api.get_joint_speed()
                else:
                    right_vel = [0] * len(state)
                self.right_hand_state_pub.publish(self.joint_state_msg(state,right_vel))
                right_info_msg = String()
                right_info_msg.data = json.dumps(self.hand_info(hand_type="right"))
                self.right_hand_info_pub.publish(right_info_msg)
                if self.right_hand_force == True:
                    force = self.right_hand_api.get_force()
                    t_force = [item for sublist in force for item in sublist]
                    right_force_msg = Float32MultiArray()
                    right_force_msg.data = t_force
                    self.right_hand_pressure_pub.publish(right_force_msg)
            self.rate.sleep()

    def hand_info(self,hand_type="left"):
        if hand_type == "left":
            if self.left_hand_force == True:
                force = self.left_hand_api.get_force()
            else:
                force = None
            data = {
                "left_hand":{
                    "version": self.left_hand_api.get_version(),
                    "hand_joint": self.left_hand_joint,
                    "speed": self.left_hand_api.get_speed(),
                    "current": self.left_hand_api.get_current(),
                    "fault": self.left_hand_api.get_fault(),
                    "motor_temperature": self.left_hand_api.get_temperature(),
                    "torque": force,
                }
            }
            return data
        elif hand_type == "right":
            if self.right_hand_force == True:
                force = self.right_hand_api.get_force()
            else:
                force = None
            data = {
                "right_hand":{
                    "version": self.right_hand_api.get_version(),
                    "hand_joint": self.right_hand_joint,
                    "speed": self.right_hand_api.get_speed(),
                    "current": self.right_hand_api.get_current(),
                    "fault": self.right_hand_api.get_fault(),
                    "motor_temperature": self.right_hand_api.get_temperature(),
                    "torque": force,
                }
            }
            return data
    def left_hand_cb(self, msg):
        #print(list(msg.position))
        self.left_hand_api.finger_move(pose=list(msg.position))
        vel = list(msg.velocity)
        self.left_vel = vel
        if all(x == 0 for x in vel):
            return
        else:
            if self.left_hand_joint == "L7" and len(vel) == 7:
                speed = vel
                self.left_hand_api.set_joint_speed(speed=speed)
            elif self.left_hand_joint == "L10" and len(vel) == 10:
                speed = [vel[0],vel[2],vel[3],vel[4],vel[5]]
                self.left_hand_api.set_joint_speed(speed=speed)
            elif self.left_hand_joint == "L20" and len(vel) == 20:
                speed = [vel[10],vel[1],vel[2],vel[3],vel[4]]
                self.left_hand_api.set_joint_speed(speed=speed)
            elif self.left_hand_joint == "L25" and len(vel) == 25:
                speed = vel
                self.left_hand_api.set_joint_speed(speed=speed)
        
    def right_hand_cb(self, msg):
        self.right_hand_api.finger_move(pose=list(msg.position))
        vel = list(msg.velocity)
        self.right_vel = vel
        if all(x == 0 for x in vel):
            return
        else:
            if self.right_hand_joint == "L7" and len(vel) == 7:
                speed = vel
                self.right_hand_api.set_joint_speed(speed=speed)
            elif self.right_hand_joint == "L10" and len(vel) == 10:
                speed = [vel[0],vel[2],vel[3],vel[4],vel[5]]
                self.right_hand_api.set_joint_speed(speed=speed)
            elif self.right_hand_joint == "L20" and len(vel) == 20:
                speed = [vel[10],vel[1],vel[2],vel[3],vel[4]]
                self.right_hand_api.set_joint_speed(speed=speed)
            elif self.right_hand_joint == "L25" and len(vel) == 25:
                speed = vel
                self.right_hand_api.set_joint_speed(speed=speed)
        
    def joint_state_msg(self, pose,vel=[]):
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = []
        joint_state.position = pose
        if len(vel) > 1:
            joint_state.velocity = vel
        return joint_state
    
    def hand_setting_cb(self, msg):
        hand_left, hand_right = False, False
        data = json.loads(msg.data)
        print(f"收到设置命令：{data['setting_cmd']}")
        print(data)
        #except:
            #ColorMsg(msg="设置命令参数不正确", color="red")
        if data["params"]["hand_type"] == "left" and self.left_hand == True:
            hand = self.left_hand_api
            hand_left = True
        elif data["params"]["hand_type"] == "right" and self.right_hand == True:
            hand = self.right_hand_api
            hand_right = True
        else:
            print("请指定要设定的手部位")
            return
        # 设置最大扭矩
        if data["setting_cmd"] == "set_max_torque_limits": # 设置最大扭矩
            torque = list(data["params"]["torque"])
            hand.set_torque(torque=torque)
            
        if data["setting_cmd"] == "set_speed": # 设置速度
            if isinstance(data["params"]["speed"], list) == True:
                speed = data["params"]["speed"]
                hand.set_speed(speed=speed)
            else:
                ColorMsg(msg=f"设置速度参数错误,speed必须为list", color="red")

        
        if data["setting_cmd"] == "clear_faults": # 清除错误
            if hand_left == True and self.left_hand_joint == "L10" :
                ColorMsg(msg=f"L10左手不能清除错误")
            elif hand_right == True and self.right_hand_joint == "L10" :
                ColorMsg(msg=f"L10右手不能清除错误")
            else:
                hand.clear_faults()
        if data["setting_cmd"] == "get_faults": # 获取错误
            f = hand.get_fault()
            ColorMsg(msg=f"获取错误：{f}")
        if data["setting_cmd"] == "electric_current": # 获取电流
            ColorMsg(msg=f"获取电流：{hand.get_current()}")
        if data["setting_cmd"] == "set_electric_current": # 设置电流
            if isinstance(data["params"]["current"], list) == True:
                hand.set_current(data["params"]["current"])
        # except:
        #     ColorMsg(msg=f"命令参数错误", color="red")
    
def signal_handler(sig, frame):

    sys.exit(0)  # Exit the program normally

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill command
    linker_hand = LinkerHand()
