import sys
import os
import time
import rospy
import can
import threading
from sensor_msgs.msg import JointState
from utils.enum import FrameProperty
from utils.color_msg import ColorMsg


class LinkerHandL25Can:
    def __init__(self, config, can_channel='can0', baudrate=1000000, can_id=0x28):
        self.config = config
        self.can_id = can_id
        self.running = True
        self.x01, self.x02, self.x03, self.x04,self.x05,self.x06,self.x07, self.x08,self.x09,self.x0A,self.x0B,self.x0C,self.x0D,self.x0E,self.speed = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        # 根据操作系统初始化 CAN 总线
        if sys.platform == "linux":
            self.bus = can.interface.Bus(
                channel=can_channel, interface="socketcan", bitrate=baudrate, 
                can_filters=[{"can_id": can_id, "can_mask": 0x7FF}]
            )
        elif sys.platform == "win32":
            self.bus = can.interface.Bus(
                channel='PCAN_USBBUS1', interface='pcan', bitrate=baudrate, 
                can_filters=[{"can_id": can_id, "can_mask": 0x7FF}]
            )
        else:
            raise EnvironmentError("Unsupported platform for CAN interface")

        # 根据 can_id 初始化 publisher 和相关参数
        if can_id == 0x27:  # 左手
            self.pub = rospy.Publisher("/cb_left_hand_state", JointState, queue_size=10)
            self.hand_exists = config['LINKER_HAND']['LEFT_HAND']['EXISTS']
            self.hand_names = config['LINKER_HAND']['LEFT_HAND']['NAME']


        # # 初始化数据存储
        # self.x01, self.x02, self.x03, self.x04 = [[0.0] * 5 for _ in range(4)]
        # self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = \
        #     [[0.0] * 5 for _ in range(4)]

        # 启动接收线程
        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_command(self, frame_property, data_list):
        """
        发送命令到 CAN 总线
        :param frame_property: 数据帧属性
        :param data_list: 数据载荷
        """
        frame_property_value = int(frame_property.value) if hasattr(frame_property, 'value') else frame_property
        data = [frame_property_value] + [int(val) for val in data_list]
        msg = can.Message(arbitration_id=self.can_id, data=data, is_extended_id=False)
        try:
            self.bus.send(msg)
            print(f"Message sent: ID={hex(self.can_id)}, Data={data}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")

    def receive_response(self):
        """
        接收并处理 CAN 总线的响应消息
        """
        while self.running:
            try:
                msg = self.bus.recv(timeout=1.0)  # 阻塞接收，1 秒超时
                if msg:
                    self.process_response(msg)
            except can.CanError as e:
                print(f"Error receiving message: {e}")

    # def set_finger_base(self, angles):
    #     self.send_command(FrameProperty.JOINT_PITCH_R, angles)

    # def set_finger_tip(self, angles):
    #     self.send_command(FrameProperty.JOINT_TIP_R, angles)

    # def set_finger_middle(self, angles):
    #     self.send_command(0x04, angles)

    # def set_thumb_roll(self, angle):
    #     self.send_command(FrameProperty.JOINT_ROLL_R, angle)

    def send_command(self, frame_property, data_list):
        frame_property_value = int(frame_property.value) if hasattr(frame_property, 'value') else frame_property
        data = [frame_property_value] + [int(val) for val in data_list]
        
        msg = can.Message(arbitration_id=self.can_id, data=data, is_extended_id=False)
        try:
            self.bus.send(msg)
        except can.CanError:
            print("Message NOT sent")
        time.sleep(0.002)
    
    def set_01(self, angles):
        # print("_-"*20)
        # print("set_01")
        # print(angles)
        self.send_command(0x01, angles)
        
    def set_02(self, angles):
        # print("_-"*20)
        # print("set_02")
        # print(angles)
        self.send_command(0x02, angles)

    def set_03(self, angles):
        # print("_-"*20)
        # print("set_03")
        # print(angles)
        self.send_command(0x03, angles)

    def set_04(self, angles):
        # print("_-"*20)
        # print("set_04")
        # print(angles)
        self.send_command(0x04, angles)

    def set_05(self, angles):
        # print("_-"*20)
        # print("set_05")
        # print(angles)
        self.send_command(0x05, angles)
    def set_06(self, angles):
        # print("_-"*20)
        # print("set_06")
        # print(angles)
        self.send_command(0x06, angles)
    def set_speed(self, speed):
        self.speed = [0,0,0,0,0]
        self.send_command(0x41, speed)
        # self.send_command(0x09, speed)
        # self.send_command(0x0A, speed)
        # self.send_command(0x0B, speed)
        # self.send_command(0x0C, speed)
        # self.send_command(0x0D, speed)
        # self.send_command(0x0E, speed)
    def set_finger_torque(self, torque):
        self.send_command(0x42, torque)

    def request_device_info(self):
        self.send_command(0xC0, [0])
        self.send_command(0xC1, [0])
        self.send_command(0xC2, [0])

    def save_parameters(self):
        self.send_command(0xCF, [])
    def process_response(self, msg):
        if msg.arbitration_id == self.can_id:
            frame_type = msg.data[0]
            response_data = msg.data[1:]
            if frame_type == 0x01:
                self.x01 = list(response_data)
            elif frame_type == 0x02:
                self.x02 = list(response_data)
            elif frame_type == 0x03:
                self.x03 = list(response_data)
            elif frame_type == 0x04:
                self.x04 = list(response_data)
            elif frame_type == 0x05:
                self.x05 = list(response_data)
            elif frame_type == 0x06:
                self.x06 = list(response_data)
            elif frame_type == 0xC0:
                print(f"Device ID info: {response_data}")
                if self.can_id == 0x28:
                    self.right_hand_info = response_data
                elif self.can_id == 0x27:
                    self.left_hand_info = response_data
            elif frame_type == 0x08:
                self.x08 = list(response_data)
            elif frame_type == 0x09:
                self.x09 = list(response_data)
            elif frame_type == 0x0A:
                self.x0A = list(response_data)
            elif frame_type == 0x0B:
                self.x0B = list(response_data)
            elif frame_type == 0x0C:
                self.x0C = list(response_data)
            elif frame_type == 0x0D:
                self.x0D = list(response_data)
            elif frame_type == 0x22:
                #ColorMsg(msg=f"五指切向压力方向：{list(response_data)}")
                d = list(response_data)
                self.tangential_force_dir = [float(i) for i in d]
            elif frame_type == 0x23:
                #ColorMsg(msg=f"五指接近度：{list(response_data)}")
                d = list(response_data)
                self.approach_inc = [float(i) for i in d]
            elif frame_type == 0x41:
                self.speed = list(response_data)
            elif frame_type == 0x42:
                self.finger_torque = list(response_data)

    def get_current_status(self):
        print(self.x02)
        return self.x01, self.x02, self.x03, self.x04, self.x05, self.x06
    
    def get_speed(self):
        #self.send_command(0x41, [0])
        return self.speed
        # self.send_command(0x09, [0])
        # self.send_command(0x0A, [0])
        # self.send_command(0x0B, [0])
        # self.send_command(0x0C, [0])
        # self.send_command(0x0D, [0])
        # self.send_command(0x0E, [0])
        # return self.x09+self.x0A+self.x0B+self.x0C+self.x0D+self.x0E
    def get_finger_torque(self):
        return self.finger_torque
    # def get_current(self):
    #     return self.x06
    # def get_fault(self):
    #     return self.x07
    def close_can_interface(self):
        if self.bus:
            self.bus.shutdown()  # 关闭 CAN 总线

