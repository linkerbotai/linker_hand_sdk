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

class LinkerHandL10Can:
    def __init__(self, config,can_id, can_channel='can0', baudrate=1000000, ):
        self.x01 = [0] * 5
        self.x02 = [0] * 5
        self.x04 = [0] * 5
        self.x05 = [0] * 5
        self.can_id = can_id
        self.joint_angles = [0] * 10
        self.pressures = [200] * 5  # 默认扭矩200
        self.bus = self.init_can_bus(can_channel, baudrate)
        self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = [[0.0] * 5 for _ in range(4)]
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
        time.sleep(0.002)

    def set_joint_positions(self, joint_angles):
        """将10个关节的位置设置（joint_angles: 10个数值的列表）。"""
        self.joint_angles = joint_angles
        # 分帧发送角度控制
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
    def set_torque(self,torque=[180,180,180,180,180]):
        self.send_frame(0x02, torque)
        
    def set_joint_speed_l10(self,speed=[180]*5):
        print(speed)
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
                # print("x01")
                # print(self.x01)
            elif frame_type == FrameProperty.MAX_PRESS_RCO.value:    # 0x02
                self.x02 = list(response_data)
            elif frame_type == FrameProperty.JOINT_POSITION2_RCO.value:    # 0x04
                self.x04 = list(response_data)
                # print("x04")
                # print(self.x04)
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

    def get_current_status(self):
        return self.x01 + self.x04
    def get_speed(self):
        return self.x05
    def get_press(self):
        self.set_max_torque_limits(pressures=[0.0], type="get")
        time.sleep(0.001)
        return self.x02
    def get_force(self):
        return [self.normal_force,self.tangential_force , self.tangential_force_dir , self.approach_inc]
    def close_can_interface(self):
        """Stop the CAN communication."""
        self.running = False
        if self.receive_thread.is_alive():
            self.receive_thread.join()
        if self.bus:
            self.bus.shutdown()