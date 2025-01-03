import sys
import os
import time
import rospy
import can
import threading
from sensor_msgs.msg import JointState
from utils.enum import FrameProperty
from utils.color_msg import ColorMsg


class LinkerHandL20Can:
    def __init__(self, config, can_channel='can0', baudrate=1000000, can_id=0x28):
        self.config = config
        self.can_id = can_id
        self.running = True
        self.x05, self.x06, self.x07 = [],[],[]
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
        if can_id == 0x28:  # 左手
            self.pub = rospy.Publisher("/cb_left_hand_state", JointState, queue_size=10)
            self.hand_exists = config['LINKER_HAND']['LEFT_HAND']['EXISTS']
            self.hand_joint = config['LINKER_HAND']['LEFT_HAND']['JOINT']
            self.hand_names = config['LINKER_HAND']['LEFT_HAND']['NAME']
        elif can_id == 0x27:  # 右手
            self.pub = rospy.Publisher("/cb_right_hand_state", JointState, queue_size=10)
            self.hand_exists = config['LINKER_HAND']['RIGHT_HAND']['EXISTS']
            self.hand_joint = config['LINKER_HAND']['RIGHT_HAND']['JOINT']
            self.hand_names = config['LINKER_HAND']['RIGHT_HAND']['NAME']

        # 初始化数据存储
        self.x01, self.x02, self.x03, self.x04 = [[0.0] * 5 for _ in range(4)]
        self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = \
            [[0.0] * 5 for _ in range(4)]

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

    def set_finger_base(self, angles):
        self.send_command(FrameProperty.JOINT_PITCH_R, angles)

    def set_finger_tip(self, angles):
        self.send_command(FrameProperty.JOINT_TIP_R, angles)

    def set_finger_middle(self, angles):
        self.send_command(FrameProperty.JOINT_YAW_R, angles)

    def set_thumb_roll(self, angle):
        self.send_command(FrameProperty.JOINT_ROLL_R, angle)

    def send_command(self, frame_property, data_list):
        frame_property_value = int(frame_property.value) if hasattr(frame_property, 'value') else frame_property
        data = [frame_property_value] + [int(val) for val in data_list]
        
        msg = can.Message(arbitration_id=self.can_id, data=data, is_extended_id=False)
        try:
            self.bus.send(msg)
        except can.CanError:
            print("Message NOT sent")
        time.sleep(0.002)

    def set_joint_pitch(self, frame, angles):
        self.send_command(frame, angles)

    def set_joint_yaw(self, angles):
        self.send_command(0x02, angles)

    def set_joint_roll(self, thumb_roll):
        self.send_command(0x03, [thumb_roll, 0, 0, 0, 0])

    def set_joint_speed(self, speed):
        self.x05 = speed
        self.send_command(0x05, speed)
    def set_electric_current(self, e_c=[]):
        self.send_command(0x06, e_c)

    def get_normal_force(self):
        self.send_command(0x20,[])

    def get_tangential_force(self):
        self.send_command(0x21,[])

    def get_tangential_force_dir(self):
        self.send_command(0x22,[])
    def get_approach_inc(self):
        self.send_command(0x23,[])



    def get_electric_current(self, e_c=[]):
        self.send_command(0x06, e_c)
    def clear_faults(self):
        self.send_command(0x07, [1, 1, 1, 1, 1])
    def get_faults(self):
        self.send_command(0x07, [0, 0, 0, 0, 0])
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
                # print("x01")
                # print(self.x01)
            elif frame_type == 0x02:
                self.x02 = list(response_data)
                # print("x02")
                # print(self.x02)
            elif frame_type == 0x03:
                self.x03 = list(response_data)
                # print("x03")
                # print(self.x03)
            elif frame_type == 0x04:
                self.x04 = list(response_data)
                # print("x04")
                # print(self.x04)
            elif frame_type == 0xC0:
                print(f"Device ID info: {response_data}")
                if self.can_id == 0x28:
                    self.right_hand_info = response_data
                elif self.can_id == 0x27:
                    self.left_hand_info = response_data
            elif frame_type == 0x05:
                #ColorMsg(msg=f"速度设置为：{list(response_data)}", color="yellow")
                #self.x05 = list(response_data)
                pass
            elif frame_type == 0x06:
                #ColorMsg(msg=f"当前电流状态：{list(response_data)}")
                self.x06 = list(response_data)
            elif frame_type == 0x07:
                #ColorMsg(msg=f"电机故障状态反馈：{list(response_data)}", color="yellow")
                self.x07 = list(response_data)
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
        return self.x01 + self.x02 + self.x03 + self.x04
    def get_force(self):
        return [self.normal_force,self.tangential_force , self.tangential_force_dir , self.approach_inc]
    def get_speed(self):
        return self.x05
    def get_current(self):
        return self.x06
    def get_fault(self):
        return self.x07
    def close_can_interface(self):
        if self.bus:
            self.bus.shutdown()  # 关闭 CAN 总线

