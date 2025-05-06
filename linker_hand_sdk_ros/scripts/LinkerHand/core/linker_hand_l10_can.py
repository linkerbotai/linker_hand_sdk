#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import can
import time,sys
import threading
import numpy as np
from enum import Enum
from sensor_msgs.msg import JointState

class FrameProperty(Enum):
    INVALID_FRAME_PROPERTY = 0x00
    JOINT_POSITION_RCO = 0x01
    MAX_PRESS_RCO = 0x02
    JOINT_POSITION2_RCO = 0x04
    JOINT_SPEED = 0x05
    REQUEST_DATA_RETURN = 0x09
    JOINT_POSITION_N = 0x11
    MAX_PRESS_N = 0x12
    HAND_NORMAL_FORCE = 0X20
    HAND_TANGENTIAL_FORCE = 0X21
    HAND_TANGENTIAL_FORCE_DIR = 0X22
    HAND_APPROACH_INC = 0X23
    MOTOR_TEMPERATURE_1 = 0x33
    MOTOR_TEMPERATURE_2 = 0x34

class LinkerHandL10Can:
    def __init__(self,can_id, can_channel='can0', baudrate=1000000, ):
        self.x01 = [0] * 5
        self.x02 = [0] * 5
        self.x04 = [0] * 5
        self.x05 = [0] * 5
        self.x33 = self.x34 = [0] * 5
        # 故障码
        self.x35,self.x36 = [0] * 5,[0] * 5
        self.xb0,self.xb1,self.xb2,self.xb3,self.xb4,self.xb5 = [-1] * 5,[-1] * 5,[-1] * 5,[-1] * 5,[-1] * 5,[-1] * 5
        self.can_id = can_id
        self.joint_angles = [0] * 10
        self.pressures = [200] * 5  # 默认扭矩200
        self.bus = self.init_can_bus(can_channel, baudrate)
        self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = [[0.0] * 5 for _ in range(4)]
        self.version = None
        # 启动接收线程
        self.running = True
        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def init_can_bus(self, channel, baudrate):
        if sys.platform == "linux":
            return can.interface.Bus(channel=channel, interface="socketcan", bitrate=baudrate)
        elif sys.platform == "win32":
            return can.interface.Bus(channel='PCAN_USBBUS1', interface='pcan', bitrate=baudrate)
        else:
            raise EnvironmentError("Unsupported platform for CAN interface")

    def send_frame(self, frame_property, data_list):
        """发送一个带有指定属性和数据的单个CAN帧。"""
        frame_property_value = int(frame_property.value) if hasattr(frame_property, 'value') else frame_property
        data = [frame_property_value] + [int(val) for val in data_list]
        msg = can.Message(arbitration_id=self.can_id, data=data, is_extended_id=False)
        try:
            self.bus.send(msg)
        except can.CanError as e:
            print(f"Failed to send message: {e}")
        time.sleep(0.005)

    def set_joint_positions(self, joint_angles):
        """将10个关节的位置设置（joint_angles: 10个数值的列表）。"""
        self.joint_angles = joint_angles
        # 分帧发送角度控制 L10协议为前6和后4分开
        self.send_frame(FrameProperty.JOINT_POSITION2_RCO, self.joint_angles[6:])
        time.sleep(0.001)
        self.send_frame(FrameProperty.JOINT_POSITION_RCO, self.joint_angles[:6])
        

    def set_max_torque_limits(self, pressures,type="get"):
        """设置最大扭矩限制"""
        if type == "get":
            self.pressures = [0.0]
        else:
            self.pressures = pressures[:5]
        #self.send_frame(FrameProperty.MAX_PRESS_RCO, self.pressures)
        
        
    def set_joint_speed_l10(self,speed=[180]*5):
        self.x05 = speed
        for i in range(2):
            time.sleep(0.01)
            self.send_frame(0x05, speed)
    def set_speed(self,speed=[180]*5):
        self.x05 = speed
        for i in range(2):
            time.sleep(0.01)
            self.send_frame(0x05, speed)
    def request_all_status(self):
        """获取所有关节位置和压力。"""
        self.send_frame(FrameProperty.REQUEST_DATA_RETURN, [])
    ''' -------------------压力传感器---------------------- '''
    def get_normal_force(self):
        self.send_frame(FrameProperty.HAND_NORMAL_FORCE,[])

    def get_tangential_force(self):
        self.send_frame(FrameProperty.HAND_TANGENTIAL_FORCE,[])

    def get_tangential_force_dir(self):
        self.send_frame(FrameProperty.HAND_TANGENTIAL_FORCE_DIR,[])
    def get_approach_inc(self):
        self.send_frame(FrameProperty.HAND_APPROACH_INC,[])
    ''' -------------------电机温度---------------------- '''
    def get_motor_temperature(self):
        self.send_frame(FrameProperty.MOTOR_TEMPERATURE_1,[])
        self.send_frame(FrameProperty.MOTOR_TEMPERATURE_2,[])
    # 电机故障码
    def get_motor_fault_code(self):
        self.send_frame(0x35,[])
        self.send_frame(0x36,[])
    def receive_response(self):
        """接收CAN响应并处理."""
        while self.running:
            try:
                msg = self.bus.recv(timeout=1.0)
                if msg:
                    self.process_response(msg)
            except can.CanError as e:
                print(f"Error receiving CAN message: {e}")

    def process_response(self, msg):
        """处理接收到的CAN消息。"""
        if msg.arbitration_id == self.can_id:
            frame_type = msg.data[0]
            response_data = msg.data[1:]
            if frame_type == FrameProperty.JOINT_POSITION_RCO.value:   # 0x01
                self.x01 = list(response_data)  # 
            elif frame_type == FrameProperty.MAX_PRESS_RCO.value:    # 0x02
                self.x02 = list(response_data)
            elif frame_type == FrameProperty.JOINT_POSITION2_RCO.value:    # 0x04
                self.x04 = list(response_data)
            elif frame_type == 0x05:
                #self.x05 = list(response_data)
                pass
            elif frame_type == 0x20:
                #ColorMsg(msg=f"五指法向压力：{list(response_data)}")
                d = list(response_data)
                self.normal_force = [float(i) for i in d]
            elif frame_type == 0x21:
                #ColorMsg(msg=f"五指切向压力：{list(response_data)}")
                d = list(response_data)
                self.tangential_force = [float(i) for i in d]
            elif frame_type == 0x22:
                #ColorMsg(msg=f"五指切向压力方向：{list(response_data)}")
                d = list(response_data)
                self.tangential_force_dir = [float(i) for i in d]
            elif frame_type == 0x23:
                #ColorMsg(msg=f"五指接近度：{list(response_data)}")
                d = list(response_data)
                self.approach_inc = [float(i) for i in d]
            elif frame_type == 0x33:
                self.x33 = list(response_data)
            elif frame_type == 0x34:
                self.x34 = list(response_data)
            elif frame_type == 0x35:
                self.x35 = list(response_data)
            elif frame_type == 0x36:
                self.x36 = list(response_data)
            elif frame_type == 0xb0:
                self.xb0 = list(response_data)
            elif frame_type == 0xb1:
                self.xb1 = list(response_data)
            elif frame_type == 0xb2:
                self.xb2 = list(response_data)
            elif frame_type == 0xb3:
                self.xb3 = list(response_data)
            elif frame_type == 0xb4:
                self.xb4 = list(response_data)
            elif frame_type == 0xb5:
                self.xb5 = list(response_data)
            elif frame_type == 0x64:
                self.version = list(response_data)

    def set_torque(self,torque=[]):
        '''设置最大扭矩'''
        self.send_frame(0x02, torque)
    def get_version(self):
        '''获取版本'''
        self.send_frame(0x64,[])
        time.sleep(0.001)
        return self.version
    def get_current_status(self):
        '''获取当前关节状态'''
        self.send_frame(0x01,[])
        time.sleep(0.001)
        self.send_frame(0x04,[])
        time.sleep(0.001)
        return self.x01 + self.x04
    def get_speed(self):
        '''获取当前速度'''
        return self.x05
    def get_press(self):
        '''获取当前扭矩'''
        self.set_max_torque_limits(pressures=[0.0], type="get")
        time.sleep(0.001)
        return self.x02
    def get_force(self):
        '''获取压感数据'''
        return [self.normal_force,self.tangential_force , self.tangential_force_dir , self.approach_inc]
    def get_temperature(self):
        '''获取电机当前温度'''
        self.get_motor_temperature()
        return self.x33+self.x34

    def get_touch_type(self):
        '''获取触摸类型'''
        self.send_frame(0xb1,[])
        time.sleep(0.002)
        if len(self.xb1) == 2:
            return 2
        else:
            return -1
    
    def get_touch(self):
        '''获取触摸数据'''
        self.send_frame(0xb1,[])
        self.send_frame(0xb2,[])
        self.send_frame(0xb3,[])
        self.send_frame(0xb4,[])
        self.send_frame(0xb5,[])
        return [self.xb1[1],self.xb2[1],self.xb3[1],self.xb4[1],self.xb5[1],0] # 最后一位是手掌，目前没有

    def get_torque(self):
        '''暂不支持'''
        
        return [-1] * 5
    def get_fault(self):
        '''获取电机故障'''
        self.get_motor_fault_code()
        return self.x35+self.x36
    def get_current(self):
        '''获取电流'''
        return [None]*10
    def close_can_interface(self):
        """Stop the CAN communication."""
        self.running = False
        if self.receive_thread.is_alive():
            self.receive_thread.join()
        if self.bus:
            self.bus.shutdown()