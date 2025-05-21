#!/usr/bin/env python3 
# -*- coding: utf-8 -*-

import rospy, signal, rospkg, sys, os, math, time, threading, json
import numpy as np
from std_msgs.msg import String, Header, Float32MultiArray
from sensor_msgs.msg import JointState
from common.mapping import *
from LinkerHand.linker_hand_api import LinkerHandApi
from LinkerHand.utils.init_linker_hand import InitLinkerHand
from LinkerHand.utils.load_write_yaml import LoadWriteYaml
from LinkerHand.utils.color_msg import ColorMsg
from LinkerHand.utils.open_can import OpenCan

class LinkerHand:
    def __init__(self):
        self.hand_type = rospy.get_param('~hand_type', "right")
        self.hand_joint = rospy.get_param('~hand_joint', "L10")
        self.hand_force = rospy.get_param('~touch', "true")
        self.can = rospy.get_param('~can', "can0")
        self.modbus = rospy.get_param('~modbus', "None")
        self.hand = True
        self.open_can = OpenCan()
        self.open_can.open_can(self.can)
        self.vel = []
        self.touch_type = -1
        self.t_force = [-1] * 5
        self.hand_data_dic = {
            "version": [], # Dexterous hand version number
            "hand_joint": [], # Dexterous hand joint type
            "state": [], # Current state of the dexterous hand
            "vel": [], # Current joint speed of the dexterous hand, requires remote control
            "speed": [], # Current speed threshold of the dexterous hand
            "current": [], # Current of the dexterous hand
            "fault": [], # Current fault of the dexterous hand
            "motor_temperature": [], # Current motor temperature of the dexterous hand
            "torque": [], # Current torque of the dexterous hand
            "is_touch": self.hand_force,
            "touch_type": [],
            "touch": [],
            "finger_order":[]
        }
        self.hand_state = {
            "state": [],
            "vel": []
        }
        self.last_process_time = 0
        self.max_hz = 30
        self.min_interval = 1.0 / self.max_hz
        self.hand_setting_sub = rospy.Subscriber("/cb_hand_setting_cmd", String, self._hand_setting_cb)
        self.lock = threading.Lock()
        self._init_hand(hand_type=self.hand_type)
        
    
    def _init_hand(self, hand_type=None):
        if hand_type == "left":
            if self.hand == True:
                ColorMsg(msg=f"Enable {hand_type} configuration file left hand: {self.hand}")
                self.api = LinkerHandApi(hand_type=self.hand_type, hand_joint=self.hand_joint,can=self.can,modbus=self.modbus)
                self.touch_type = self.api.get_touch_type()
                # Left LinkerHand control topic
                self.hand_cmd_sub = rospy.Subscriber("/cb_left_hand_control_cmd", JointState, self.left_hand_cb, queue_size=1)
                self.hand_cmd_sub_arc = rospy.Subscriber("/cb_left_hand_control_cmd_arc", JointState, self.left_hand_arc_cb, queue_size=1)
                # Left LinkerHand state publishing topic
                self.hand_state_pub = rospy.Publisher('/cb_left_hand_state', JointState, queue_size=10)
                self.hand_state_arc_pub = rospy.Publisher('/cb_left_hand_state_arc', JointState, queue_size=10)
                # Left LinkerHand motor temperature, current speed, current torque, motor fault code, pressure sensor, etc. publishing topic
                self.hand_info_pub = rospy.Publisher("/cb_left_hand_info", String, queue_size=10)
                if self.hand_force == True:
                    # Left LinkerHand pressure sensor data publishing topic
                    if self.touch_type == 2:
                        self.matrix_touch_pub = rospy.Publisher("/cb_left_hand_matrix_touch" ,String, queue_size=10)
                        print("Initialize the left-hand matrix sensor")
                    elif self.touch_type != -1:
                        self.hand_pressure_pub = rospy.Publisher("/cb_left_hand_force", Float32MultiArray, queue_size=10)
            else:
                ColorMsg(msg=f"Left hand {self.hand_joint} is not enabled in the configuration file")
        elif hand_type == "right":
            if self.hand == True:
                ColorMsg(msg=f"Enable {hand_type} configuration file right hand: {self.hand}")
                self.api = LinkerHandApi(hand_type=self.hand_type, hand_joint=self.hand_joint,can=self.can,modbus=self.modbus)
                self.touch_type = self.api.get_touch_type()
                # Right LinkerHand control topic
                self.hand_cmd_sub = rospy.Subscriber("/cb_right_hand_control_cmd", JointState, self.right_hand_cb, queue_size=1)
                self.hand_cmd_sub_arc = rospy.Subscriber("/cb_right_hand_control_cmd_arc", JointState, self.right_hand_arc_cb, queue_size=1)
                # Right LinkerHand state publishing topic
                self.hand_state_pub = rospy.Publisher('/cb_right_hand_state', JointState, queue_size=10)
                self.hand_state_arc_pub = rospy.Publisher('/cb_right_hand_state_arc', JointState, queue_size=10)
                # Right LinkerHand motor temperature, current speed, current torque, motor fault code, pressure sensor, etc. publishing topic
                self.hand_info_pub = rospy.Publisher("/cb_right_hand_info", String, queue_size=10)
                if self.hand_force == True:
                    # Right LinkerHand pressure sensor data publishing topic
                    if self.touch_type == 2:
                        self.matrix_touch_pub = rospy.Publisher("/cb_right_hand_matrix_touch" ,String, queue_size=10)
                        print("Initialize the right-hand matrix sensor")
                    elif self.touch_type != -1:
                        self.hand_pressure_pub = rospy.Publisher("/cb_right_hand_force", Float32MultiArray, queue_size=10)
            else:
                ColorMsg(msg=f"Right hand {self.hand_joint} is not enabled in the configuration file")
        pose = None
        torque = [200, 200, 200, 200, 200]
        speed = [80, 200, 200, 200, 200]
        if self.hand_joint == "L7":
            # The data length of L7 is 7, reinitialize here
            pose = [255, 200, 255, 255, 255, 255, 180]
            torque = [250, 250, 250, 250, 250, 250, 250]
            speed = [120, 180, 180, 180, 180, 180, 180]
        elif self.hand_joint == "L10":
            pose = [255, 200, 255, 255, 255, 255, 180, 180, 180, 41]
        elif self.hand_joint == "L20":
            pose = [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255]
        elif self.hand_joint == "L21":
            pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        elif self.hand_joint == "L25":
            pose = [75, 255, 255, 255, 255, 176, 97, 81, 114, 147, 202, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        if pose is not None:
            self.api.set_speed(speed=speed)
            self.api.set_torque(torque=torque)
            self.api.finger_move(pose=pose)


    def _hand_setting_cb(self, msg):
        data = json.loads(msg.data)
        print(f"Received setting command: {data['setting_cmd']}")
        if data["params"]["hand_type"] == "left" and self.hand == True:
            hand = self.api
            hand_left = True
        elif data["params"]["hand_type"] == "right" and self.hand == True:
            hand = self.api
            hand_right = True
        else:
            print("Please specify the hand part to be set")
            return
        # Set maximum torque
        if data["setting_cmd"] == "set_max_torque_limits": # Set maximum torque
            torque = list(data["params"]["torque"])
            hand.set_torque(torque=torque)
            
        if data["setting_cmd"] == "set_speed": # Set speed
            if isinstance(data["params"]["speed"], list) == True:
                speed = data["params"]["speed"]
                hand.set_speed(speed=speed)
            else:
                ColorMsg(msg=f"Speed parameter error, speed must be a list", color="red")
        if data["setting_cmd"] == "clear_faults": # Clear faults
            if hand_left == True and self.hand_joint == "L10" :
                ColorMsg(msg=f"L10 left hand cannot clear faults")
            elif hand_right == True and self.hand_joint == "L10" :
                ColorMsg(msg=f"L10 right hand cannot clear faults")
            else:
                hand.clear_faults()
        if data["setting_cmd"] == "get_faults": # Get faults
            f = hand.get_fault()
            ColorMsg(msg=f"Get faults: {f}")
        if data["setting_cmd"] == "electric_current": # Get current
            ColorMsg(msg=f"Get current: {hand.get_current()}")
        if data["setting_cmd"] == "set_electric_current": # Set current
            if isinstance(data["params"]["current"], list) == True:
                hand.set_current(data["params"]["current"])


    def run(self):
        self.thread_get_state = threading.Thread(target=self._get_hand_state)
        self.thread_get_state.daemon = True
        self.thread_get_state.start()
        
        self.thread_get_info = threading.Thread(target=self._get_hand_info)
        self.thread_get_info.daemon = True
        self.thread_get_info.start()
        # self.thread_get_info.join()

        if self.touch_type == 2:
            self.thread_get_matrix_touch = threading.Thread(target=self._get_matrix_touch)
            self.thread_get_matrix_touch.daemon = True
            self.thread_get_matrix_touch.start()
            # self.thread_get_matrix_touch.join()
        elif self.touch_type != -1 and self.touch_type != 2:
            self.thread_get_touch = threading.Thread(target=self._get_hand_touch)
            self.thread_get_touch.daemon = True
            self.thread_get_touch.start()
            # self.thread_get_touch.join()
        

    def _get_hand_state(self):
        hand_state = {
            'state':[],
            'vel':[]
        }
        while True:
            if self.hand_state_pub.get_num_connections() > 0:
                hand_state['state'] = self.api.get_state()
                hand_state['vel'] = self.api.get_joint_speed()
                self.pub_hand_state(hand_state=hand_state)
            time.sleep(0.02)

    def pub_hand_state(self,hand_state):
        state = hand_state['state']
        if self.hand_type == "left":
            state_arc = range_to_arc_left(state,self.hand_joint)
        if self.hand_type == "right":
            state_arc = range_to_arc_right(state,self.hand_joint)
        vel = hand_state['vel']
        if state == None:
            return
        if all(x == 0 for x in  vel):
            self.hand_state_pub.publish(self.joint_state_msg(state,[0]*len(state)))
            self.hand_state_arc_pub.publish(self.joint_state_msg(state_arc,[0]*len(state)))
        else:
            self.hand_state_pub.publish(self.joint_state_msg(state,vel))
            self.hand_state_arc_pub.publish(self.joint_state_msg(state_arc,vel))
    
    def _get_hand_touch(self):
        while True:
            with self.lock:
                if self.hand_pressure_pub.get_num_connections() > 0:
                    if self.hand_force == True:
                        #self.touch_type = self.api.get_touch_type()
                        if self.touch_type == 2:
                            break
                            self.t_force = self.api.get_touch()
                        elif self.touch_type != -1:
                            force = self.api.get_force()
                            self.t_force = [item for sublist in force for item in sublist]
                    else:
                        self.touch_type = -1
                    if self.hand_force == True:
                        if self.touch_type != 2 and self.touch_type !=-1:
                            t_force = self.t_force
                            force_msg = Float32MultiArray()
                            force_msg.data = t_force
                            self.hand_pressure_pub.publish(force_msg)
            time.sleep(0.02)

    def _get_matrix_touch(self):
        while True:
            with self.lock:
                if self.matrix_touch_pub.get_num_connections() > 0:
                    if self.touch_type == 2:
                        thumb_matrix, index_matrix , middle_matrix , ring_matrix , little_matrix = self.api.get_matrix_touch()
                        matrix_dic = {
                            "thumb_matrix":thumb_matrix.tolist(),
                            "index_matrix":index_matrix.tolist(),
                            "middle_matrix":middle_matrix.tolist(),
                            "ring_matrix":ring_matrix.tolist(),
                            "little_matrix":little_matrix.tolist()
                        }
                        m_t = String()
                        m_t.data = json.dumps(matrix_dic)
                        self.matrix_touch_pub.publish(m_t)
            time.sleep(0.02) 
    def _get_hand_info(self):
        while True:
            with self.lock:
                if self.hand_info_pub.get_num_connections() > 0:
                    data = {}
                    if self.hand == True:
                        joint = self.hand_joint
                    data = {
                        "version": self.api.get_version(), # Dexterous hand version number
                        "hand_joint": joint, # Dexterous hand joint type
                        "speed": self.api.get_speed(), # Current speed threshold of the dexterous hand
                        "current": self.api.get_current(), # Current of the dexterous hand
                        "fault": self.api.get_fault(), # Current fault of the dexterous hand
                        "motor_temperature": self.api.get_temperature(), # Current motor temperature of the dexterous hand
                        "torque": self.api.get_torque(), # Current torque of the dexterous hand
                        "is_touch":self.hand_force,
                        "touch_type": self.touch_type,
                        "finger_order": self.api.get_finger_order() # Finger motor order
                    }
                    self.pub_hand_info(dic=data)
            time.sleep(0.01)

            

    def pub_hand_info(self,dic):
        msg = String()
        msg.data = json.dumps(dic)
        self.hand_info_pub.publish(msg)


    def left_hand_cb(self, msg):
        now = time.time()
        if now - self.last_process_time < self.min_interval:
            return  # 丢弃当前帧，限频处理
        self.last_process_time = now
        self.api.finger_move(pose=list(msg.position))
        vel = list(msg.velocity)
        self.vel = vel
        if all(x == 0 for x in vel):
            return
        else:
            if self.hand_joint == "L7" and len(vel) == 7:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L10" and len(vel) == 10:
                speed = [vel[0],vel[2],vel[3],vel[4],vel[5]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L20" and len(vel) == 20:
                speed = [vel[10],vel[1],vel[2],vel[3],vel[4]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L21" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L25" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)

    def left_hand_arc_cb(self,msg):
        now = time.time()
        if now - self.last_process_time < self.min_interval:
            return  # 丢弃当前帧，限频处理
        self.last_process_time = now
        pose_range = arc_to_range_left(msg.position,self.hand_joint)
        self.api.finger_move(pose=list(pose_range))
        vel = list(msg.velocity)
        self.vel = vel
        if all(x == 0 for x in vel):
            return
        else:
            if self.hand_joint == "L7" and len(vel) == 7:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L10" and len(vel) == 10:
                speed = [vel[0],vel[2],vel[3],vel[4],vel[5]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L20" and len(vel) == 20:
                speed = [vel[10],vel[1],vel[2],vel[3],vel[4]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L21" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L25" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)


    def right_hand_cb(self, msg):
        now = time.time()
        if now - self.last_process_time < self.min_interval:
            return  # 丢弃当前帧，限频处理
        self.last_process_time = now
        self.api.finger_move(pose=list(msg.position))
        vel = list(msg.velocity)
        self.vel = vel
        if all(x == 0 for x in vel):
            return
        else:
            if self.hand_joint == "L7" and len(vel) == 7:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L10" and len(vel) == 10:
                speed = [vel[0],vel[2],vel[3],vel[4],vel[5]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L20" and len(vel) == 20:
                speed = [vel[10],vel[1],vel[2],vel[3],vel[4]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L21" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L25" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)

    def right_hand_arc_cb(self, msg):
        now = time.time()
        if now - self.last_process_time < self.min_interval:
            return  # 丢弃当前帧，限频处理
        self.last_process_time = now
        pose_range = arc_to_range_right(msg.position,self.hand_joint)
        self.api.finger_move(pose=list(pose_range))
        vel = list(msg.velocity)
        self.vel = vel
        if all(x == 0 for x in vel):
            return
        else:
            if self.hand_joint == "L7" and len(vel) == 7:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L10" and len(vel) == 10:
                speed = [vel[0],vel[2],vel[3],vel[4],vel[5]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L20" and len(vel) == 20:
                speed = [vel[10],vel[1],vel[2],vel[3],vel[4]]
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L21" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)
            elif self.hand_joint == "L25" and len(vel) == 25:
                speed = vel
                self.api.set_joint_speed(speed=speed)

    def joint_state_msg(self, pose,vel=[]):
        joint_state = JointState()
        joint_state.header = Header()
        joint_state.header.stamp = rospy.Time.now()
        joint_state.name = []
        joint_state.position = pose
        if len(vel) > 1:
            joint_state.velocity = vel
        return joint_state
    
        

    def signal_handler(self,sig, frame):
        self.open_can.close_can(self.can)
        sys.exit(0)  # Exit the program normally

if __name__ == '__main__':
    rospy.init_node('linker_hand_sdk', anonymous=True)
    linker_hand = LinkerHand()
    signal.signal(signal.SIGINT, linker_hand.signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, linker_hand.signal_handler)  # kill command
    linker_hand.run()
    rospy.spin()
