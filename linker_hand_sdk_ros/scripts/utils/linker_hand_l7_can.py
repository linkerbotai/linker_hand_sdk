import can
import time,sys
import threading
import numpy as np
from enum import Enum
from sensor_msgs.msg import JointState


class LinkerHandL7Can:
    def __init__(self, config,can_id, can_channel='can0', baudrate=1000000, ):
        self.x01 = [0] * 7
        self.x02 = [0] * 7
        self.x05 = [0] * 7
        self.x33 = [0] * 7
        # 故障码
        self.x35 = [0] * 7,[0] * 7
        self.can_id = can_id
        self.joint_angles = [0] * 10
        self.pressures = [200] * 7  # 默认扭矩200
        self.bus = self.init_can_bus(can_channel, baudrate)
        self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = [[0.0] * 7 for _ in range(4)]
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
        time.sleep(0.001)

    def set_joint_positions(self, joint_angles):
        """将10个关节的位置设置（joint_angles: 10个数值的列表）。"""
        if len(joint_angles) > 7:
            self.joint_angles = joint_angles[:7]
        else:
            self.joint_angles = joint_angles
        # 分帧发送角度控制
        self.send_frame(0x01,self.joint_angles)
        # self.send_frame(FrameProperty.JOINT_POSITION2_RCO, self.joint_angles[6:])
        # time.sleep(0.001)
        # self.send_frame(FrameProperty.JOINT_POSITION_RCO, self.joint_angles[:6])
        

    def set_max_torque_limits(self, pressures,type="get"):
        """设置最大扭矩限制"""
        if type == "get":
            self.pressures = [0.0]
        else:
            self.pressures = pressures[:7]
        #self.send_frame(FrameProperty.MAX_PRESS_RCO, self.pressures)
    def set_torque(self,torque=[180] * 7):
        """设置L7最大扭矩限制"""
        print("设置最大扭矩")
        print(torque)
        self.send_frame(0x02, torque)
        
    def set_joint_speed(self,speed=[180]*7):
        """设置L7速度"""
        print(speed)
        self.x05 = speed
        for i in range(2):
            time.sleep(0.01)
            self.send_frame(0x05, speed)

    ''' -------------------压力传感器---------------------- '''
    def get_normal_force(self):
        self.send_frame(0x20,[])

    def get_tangential_force(self):
        self.send_frame(0x21,[])

    def get_tangential_force_dir(self):
        self.send_frame(0x22,[])
    def get_approach_inc(self):
        self.send_frame(0x23,[])
    ''' -------------------电机温度---------------------- '''
    def get_motor_temperature(self):
        self.send_frame(0x33,[])

    # 电机故障码
    def get_motor_fault_code(self):
        self.send_frame(0x35,[])

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
            if frame_type == 0x01:   # 0x01
                self.x01 = list(response_data)  #
                
            elif frame_type == 0x02:    # 0x02
                self.x02 = list(response_data)
            elif frame_type == 0x05: # 设置速度
                self.x05 = list(response_data)
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
            elif frame_type == 0x33: # L7温度
                self.x33 = list(response_data)
            elif frame_type == 0x35: # L7错误码
                self.x35 = list(response_data)
            elif frame_type == 0x64: # L7版本号
                self.version = list(response_data)

    def get_version(self):
        self.send_frame(0x64,[])
        time.sleep(0.001)
        return self.version
    def get_current_status(self):
        self.send_frame(0x01, '')
        time.sleep(0.001)
        return self.x01
    def get_speed(self):
        return self.x05
    # def get_press(self):
    #     self.set_max_torque_limits(pressures=[0.0], type="get")
    #     time.sleep(0.001)
    #     return self.x02
    def get_torque(self):
        '''暂不支持'''
        # self.send_frame(0x02, [])
        # time.sleep(0.001)
        # return self.x02
        return [0] * 7
    def get_force(self):
        '''获取压力'''
        return [self.normal_force,self.tangential_force , self.tangential_force_dir , self.approach_inc]
    def get_temperature(self):
        '''获取温度'''
        self.get_motor_temperature()
        return self.x33
    def get_fault(self):
        '''获取故障'''
        self.get_motor_fault_code()
        return self.x35
    def close_can_interface(self):
        """Stop the CAN communication."""
        self.running = False
        if self.receive_thread.is_alive():
            self.receive_thread.join()
        if self.bus:
            self.bus.shutdown()