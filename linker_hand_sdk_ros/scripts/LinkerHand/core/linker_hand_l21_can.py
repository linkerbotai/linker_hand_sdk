#!/usr/bin/env python3
import can
import time, sys, os
import threading
import numpy as np
from enum import Enum
current_dir = os.path.dirname(os.path.abspath(__file__))
target_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(target_dir)
from utils.color_msg import ColorMsg

class FrameProperty(Enum):
    # Finger motion control - parallel control commands
    ROLL_POS = 0x01  # Roll joint position
    YAWPOS = 0x02  # Yaw joint position
    ROOT1_POS = 0x03  # Root joint 1 position
    ROOT2_POS = 0x04  # Root joint 2 position
    ROOT3_POS = 0x05  # Root joint 3 position
    TIP_POS = 0x06  # Fingertip joint position
    # Finger motion control - serial control commands
    THUMB_POS = 0x41  # Thumb joint position
    INDEX_POS = 0x42  # Index finger joint position
    MIDDLE_POS = 0x43  # Middle finger joint position
    RING_POS = 0x44  # Ring finger joint position
    LITTLE_POS = 0x45  # Little finger joint position

    # Finger motion control - speed
    ROLL_SPEED = 0x09  # Roll joint speed
    YAW_SPEED = 0x0A  # Yaw joint speed
    ROOT1_SPEED = 0x0B  # Root joint 1 speed
    ROOT2_SPEED = 0x0C  # Root joint 2 speed
    ROOT3_SPEED = 0x0D  # Root joint 3 speed
    TIP_SPEED = 0x0E  # Fingertip joint speed
    THUMB_SPEED = 0x49  # Thumb speed
    INDEX_SPEED = 0x4A  # Index finger speed
    MIDDLE_SPEED = 0x4B  # Middle finger speed
    RING_SPEED = 0x4C  # Ring finger speed
    LITTLE_SPEED = 0x4D  # Little finger speed

    # Finger motion control - torque
    ROLL_TORQUE = 0x11  # Roll joint torque
    YAW_TORQUE = 0x12  # Yaw joint torque
    ROOT1_TORQUE = 0x13  # Root joint 1 torque
    ROOT2_TORQUE = 0x14  # Root joint 2 torque
    ROOT3_TORQUE = 0x15  # Root joint 3 torque
    TIP_TORQUE = 0x16  # Fingertip joint torque
    THUMB_TORQUE = 0x51  # Thumb torque
    INDEX_TORQUE = 0x52  # Index finger torque
    MIDDLE_TORQUE = 0x53  # Middle finger torque
    RING_TORQUE = 0x54  # Ring finger torque
    LITTLE_TORQUE = 0x55  # Little finger torque

    THUMB_FAULT = 0x59  # Thumb fault code | Returns this type of data
    INDEX_FAULT = 0x5A  # Index finger fault code | Returns this type of data
    MIDDLE_FAULT = 0x5B  # Middle finger fault code | Returns this type of data
    RING_FAULT = 0x5C  # Ring finger fault code | Returns this type of data
    LITTLE_FAULT = 0x5D  # Little finger fault code | Returns this type of data

    # Finger faults and temperature
    ROLL_FAULT = 0x19  # Roll joint fault code
    YAW_FAULT = 0x1A  # Yaw joint fault code
    ROOT1_FAULT = 0x1B  # Root joint 1 fault code
    ROOT2_FAULT = 0x1C  # Root joint 2 fault code
    ROOT3_FAULT = 0x1D  # Root joint 3 fault code
    TIP_FAULT = 0x1E  # Fingertip joint fault code
    ROLL_TEMPERATURE = 0x21  # Roll joint over-temperature protection threshold
    YAW_TEMPERATURE = 0x22  # Yaw joint over-temperature protection threshold
    ROOT1_TEMPERATURE = 0x23  # Root joint 1 over-temperature protection threshold
    ROOT2_TEMPERATURE = 0x24  # Root joint 2 over-temperature protection threshold
    ROOT3_TEMPERATURE = 0x25  # Root joint 3 over-temperature protection threshold
    TIP_TEMPERATURE = 0x26  # Fingertip joint over-temperature protection threshold
    THUMB_TEMPERATURE = 0x61  # Thumb over-temperature protection threshold
    INDEX_TEMPERATURE = 0x62  # Index finger over-temperature protection threshold
    MIDDLE_TEMPERATURE = 0x63  # Middle finger over-temperature protection threshold
    RING_TEMPERATURE = 0x64  # Ring finger over-temperature protection threshold
    LITTLE_TEMPERATURE = 0x65  # Little finger over-temperature protection threshold

    # Configuration and preset actions
    HAND_UID = 0xC0  # Device unique identifier
    HAND_HARDWARE_VERSION = 0xC1  # Hardware version
    HAND_SOFTWARE_VERSION = 0xC2  # Software version
    HAND_COMM_ID = 0xC3  # Device ID
    HAND_FACTORY_RESET = 0xCE  # Restore factory settings
    HAND_SAVE_PARAMETER = 0xCF  # Save parameters

    # Tactile sensor data
    HAND_NORMAL_FORCE = 0x90  # Normal force of five fingers
    HAND_TANGENTIAL_FORCE = 0x91  # Tangential force of five fingers
    HAND_TANGENTIAL_FORCE_DIR = 0x92  # Tangential direction of five fingers
    HAND_APPROACH_INC = 0x93  # Approach sensing of five fingers

    TOUCH_SENSOR_TYPE = 0xB0  # Sensor type
    THUMB_TOUCH = 0xB1  # Thumb tactile sensing
    INDEX_TOUCH = 0xB2  # Index finger tactile sensing
    MIDDLE_TOUCH = 0xB3  # Middle finger tactile sensing
    RING_TOUCH = 0xB4  # Ring finger tactile sensing
    LITTLE_TOUCH = 0xB5  # Little finger tactile sensing
    PALM_TOUCH = 0xB6  # Palm tactile sensing

    # Action control
    ACTION_PLAY = 0xA0  # Action

    # Combined command area
    FINGER_SPEED = 0x81  # Set maximum finger speed
    FINGER_TORQUE = 0x82  # Set maximum finger torque
    FINGER_FAULT = 0x83  # Clear finger faults and fault codes
    FINGER_TEMPERATURE = 0x84  # Finger joint temperatures



class LinkerHandL21Can:
    def __init__(self, can_channel='can0', baudrate=1000000, can_id=0x28):
        self.can_id = can_id
        self.running = True
        self.last_thumb_pos, self.last_index_pos,self.last_ring_pos,self.last_middle_pos, self.last_little_pos = None,None,None,None,None
        self.x01, self.x02, self.x03, self.x04,self.x05,self.x06,self.x07, self.x08,self.x09,self.x0A,self.x0B,self.x0C,self.x0D,self.x0E,self.speed = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        self.last_root1,self.last_yaw,self.last_roll,self.last_root2,self.last_tip = None,None,None,None,None
        # 速度
        self.x49, self.x4a, self.x4b, self.x4c, self.x4d,self.xc1 = [],[],[],[],[],[]
        self.x41,self.x42,self.x43,self.x44,self.x45 = [],[],[],[],[]
        # 扭矩
        self.x51, self.x52, self.x53, self.x54,self.x55 = [],[],[],[],[]
        # 故障码
        self.x59,self.x5a,self.x5b,self.x5c,self.x5d = [-1] * 5,[-1] * 5,[-1] * 5,[-1] * 5,[-1] * 5
        # 温度阈值
        self.x61,self.x62,self.x63,self.x64,self.x65 = [],[],[],[],[]
        # 压感
        self.x90,self.x91,self.x92,self.x93 = [],[],[],[]
        # 新压感
        self.xb0,self.xb1, self.xb2, self.xb3, self.xb4,self.xb5,self.xb6 = [],[],[],[],[],[],[]
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

        # 启动接收线程
        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_command(self, frame_property, data_list,sleep_time=0.003):
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
            #print(f"Message sent: ID={hex(self.can_id)}, Data={data}")
        except can.CanError as e:
            print(f"Failed to send message: {e}")
        time.sleep(sleep_time)

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
    

    def set_joint_positions(self, joint_ranges):
        if len(joint_ranges) == 25:
            l21_pose = self.joint_map(joint_ranges)
            # 使用列表推导式将列表每6个元素切成一个子数组
            chunks = [l21_pose[i:i+6] for i in range(0, 30, 6)]
            self.send_command(FrameProperty.THUMB_POS, chunks[0])
            time.sleep(0.001)
            self.send_command(FrameProperty.INDEX_POS, chunks[1])
            time.sleep(0.001)
            self.send_command(FrameProperty.MIDDLE_POS, chunks[2])
            time.sleep(0.001)
            self.send_command(FrameProperty.RING_POS, chunks[3])
            time.sleep(0.001)
            self.send_command(FrameProperty.LITTLE_POS, chunks[4])
            time.sleep(0.001)

    def set_joint_positions_by_topic(self, joint_ranges):
        if len(joint_ranges) == 25:
            #ROLL_POS = 0x01  # 横滚关节位置 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度 [10,11,12,13,14]
            #YAW_POS = 0x02  # 航向关节位置 | 坐标系建在每个手指的指根部位，按手指伸直的状态去定义旋转角度 [5,6,7,8,9]
            #ROOT1_POS = 0x03  # 指根1关节位置 | 最接近手掌的指根关节 [0,1,2,3,4]
            #ROOT2_POS = 0x04  # 指根2关节位置 | 最接近手掌的指根关节  [15, 16,17,18,19] 16~19预留
            #ROOT3_POS = 0x05  # 指根3关节位置 | 最接近手掌的指根关节 暂无
            #TIP_POS = 0x06  # 指尖关节位置 | 最接近手掌的指根关节 [20,21,22,23,24]
            # ["大拇指根部","食指根部","中指根部","无名指根部","小拇指根部","大拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","小拇指侧摆","大拇指横滚","预留","预留","预留","预留","大拇指中部","预留","预留","预留","预留","大拇指指尖","食指指尖","中指指尖","无名指指尖","小拇指指尖"]
            
            l21_pose = self.slice_list(joint_ranges,5)
            if self._list_d_value(self.last_root1, l21_pose[0]):
                self.set_root1_positions(l21_pose[0])
                self.last_root1 = l21_pose[0]
            if self._list_d_value(self.last_yaw, l21_pose[1]):  
                self.set_yaw_positions(l21_pose[1])
                self.last_yaw = l21_pose[1]
            if self._list_d_value(self.last_roll, l21_pose[2]):
                self.set_roll_positions(l21_pose[2])
                self.last_roll = l21_pose[2]
            if self._list_d_value(self.last_root2, l21_pose[3]):
                self.set_root2_positions(l21_pose[3])
                self.last_root2 = l21_pose[3]
            if self._list_d_value(self.last_tip, l21_pose[4]): 
                self.set_tip_positions(l21_pose[4])
                self.last_tip = l21_pose[4]
            

    def slice_list(self, input_list, slice_size):
        """
        将一个列表按指定大小切片。
    
        参数:
        input_list (list): 需要切片的列表。
        slice_size (int): 每个切片的元素个数。
    
        返回:
        list of lists: 切片后的列表。
        """
        # 使用列表推导式进行切片
        sliced_list = [input_list[i:i + slice_size] for i in range(0, len(input_list), slice_size)]
        return sliced_list

    def _list_d_value(self,list1, list2):
        if list1 == None:
            return True
        for a, b in zip(list1, list2):
            if abs(b - a) > 2:
                return True
                break
        return False
    # 设置所有手指横滚关节位置
    def set_roll_positions(self, joint_ranges):
        self.send_command(FrameProperty.ROLL_POS, joint_ranges)
    # 设置所有手指航向关节位置
    def set_yaw_positions(self, joint_ranges):
        #print(joint_ranges)
        self.send_command(FrameProperty.YAW_POS, joint_ranges)
    # 设置所有手指指根1关节位置
    def set_root1_positions(self, joint_ranges):
        self.send_command(FrameProperty.ROOT1_POS, joint_ranges)
    # 设置所有手指指根2关节位置
    def set_root2_positions(self, joint_ranges):
        self.send_command(FrameProperty.ROOT2_POS, joint_ranges)
    # 设置所有手指指根3关节位置
    def set_root3_positions(self, joint_ranges):
        self.send_command(FrameProperty.ROOT3_POS, joint_ranges)
    # 设置所有手指指尖关节位置
    def set_tip_positions(self, joint_ranges=[80]*5):
        self.send_command(FrameProperty.TIP_POS, joint_ranges)
    # 设置大拇指扭矩
    def set_thumb_torque(self, j=[]):
        self.send_command(FrameProperty.THUMB_TORQUE, j)
    # 设置食指扭矩
    def set_index_torque(self, j=[]):
        self.send_command(FrameProperty.INDEX_TORQUE, j)
    # 设置中指扭矩
    def set_middle_torque(self, j=[]):
        self.send_command(FrameProperty.MIDDLE_TORQUE, j)
    # 设置无名指扭矩
    def set_ring_torque(self, j=[]):
        self.send_command(FrameProperty.RING_TORQUE, j)
    # 设置小拇指扭矩
    def set_little_torque(self, j=[]):
        self.send_command(FrameProperty.LITTLE_TORQUE, j)

    # 获取大拇指指关节位置
    def get_thumb_positions(self,j=[0]):
        self.send_command(FrameProperty.THUMB_POS, j)
    # 获取食指关节位置
    def get_index_positions(self, j=[0]):
        self.send_command(FrameProperty.INDEX_POS,j)
    # 获取中指关节位置
    def get_middle_positions(self, j=[0]):
        self.send_command(FrameProperty.MIDDLE_POS,j)
    # 获取无名指关节位置
    def get_ring_positions(self, j=[0]):
        self.send_command(FrameProperty.RING_POS,j)
    # 获取小拇指关节位置
    def get_little_positions(self, j=[0]):
        self.send_command(FrameProperty.LITTLE_POS, j)
    # 大拇指所有电机故障码
    def get_thumbn_fault(self,j=[]):
        self.send_command(FrameProperty.THUMB_FAULT,j)
    # 食指指所有电机故障码
    def get_index_fault(self,j=[]):
        self.send_command(FrameProperty.INDEX_FAULT,j)
    # 中指所有电机故障码
    def get_middle_fault(self,j=[]):
        self.send_command(FrameProperty.MIDDLE_FAULT,j)
    # 无名指所有电机故障码
    def get_ring_fault(self,j=[]):
        self.send_command(FrameProperty.RING_FAULT,j)
    # 小拇指所有电机故障码
    def get_little_fault(self,j=[]):
        self.send_command(FrameProperty.LITTLE_FAULT,j)
    # 大拇指温度阈值
    def get_thumb_threshold(self,j=[]):
        self.send_command(FrameProperty.THUMB_TEMPERATURE, '')
    # 食指指温度阈值
    def get_index_threshold(self,j=[]):
        self.send_command(FrameProperty.INDEX_TEMPERATURE, j)
    # 中指温度阈值
    def get_middle_threshold(self,j=[]):
        self.send_command(FrameProperty.MIDDLE_TEMPERATURE, j)
    # 无名指温度阈值
    def get_ring_threshold(self,j=[]):
        self.send_command(FrameProperty.RING_TEMPERATURE, j)
    # 小拇指温度阈值
    def get_little_threshold(self,j=[]):
        self.send_command(FrameProperty.LITTLE_TEMPERATURE, j)

    # 失能01模式
    def set_disability_mode(self, j=[1,1,1,1,1]):
        self.send_command(0x85,j)
    # 使能00模式
    def set_enable_mode(self, j=[00,00,00,00,00]):
        self.send_command(0x85,j)
    
    # 设置所有手指扭矩
    def set_torque(self,torque=[250]*5):
        t = torque[0]
        i = torque[1]
        m = torque[2]
        r = torque[3]
        l = torque[4]
        self.set_thumb_torque(j=[t]*5)
        self.set_index_torque(j=[i]*5)
        self.set_middle_torque(j=[m]*5)
        self.set_ring_torque(j=[r]*5)
        self.set_little_torque(j=[l]*5)
    
    def set_speed(self, speed):
        self.speed = speed
        if len(speed) < 25:
            thumb_speed = [self.speed[0]]*5
            index_speed = [self.speed[1]]*5
            middle_speed = [self.speed[2]]*5
            ring_speed = [self.speed[3]]*5
            little_speed = [self.speed[4]]*5
        else:
            thumb_speed = [self.speed[0],self.speed[1],self.speed[2],self.speed[3],self.speed[4]]
            index_speed = [self.speed[5],self.speed[6],self.speed[7],self.speed[8],self.speed[9]]
            middle_speed = [self.speed[10],self.speed[11],self.speed[12],self.speed[13],self.speed[14]]
            ring_speed = [self.speed[15],self.speed[16],self.speed[17],self.speed[18],self.speed[19]]
            little_speed = [self.speed[20],self.speed[21],self.speed[22],self.speed[23],self.speed[24]]
        self.send_command(FrameProperty.THUMB_SPEED, thumb_speed)
        self.send_command(FrameProperty.INDEX_SPEED, index_speed)
        self.send_command(FrameProperty.MIDDLE_SPEED, middle_speed)
        self.send_command(FrameProperty.RING_SPEED, ring_speed)
        self.send_command(FrameProperty.LITTLE_SPEED, little_speed)
        
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
            elif frame_type == 0x41: # 拇指关节位置返回值
                self.x41 = list(response_data)
            elif frame_type == 0x42: # 食指关节位置返回值
                #print("食指所有关节状态",list(response_data))
                self.x42 = list(response_data)
            elif frame_type == 0x43: # 中指关节位置返回值
                self.x43 = list(response_data)
            elif frame_type == 0x44: # 无名指关节位置返回值
                
                self.x44 = list(response_data)
            elif frame_type == 0x45: # 小拇指关节位置返回值
                self.x45 = list(response_data)
            elif frame_type == 0x49: # 拇指速度返回值
                self.x49 = list(response_data)
            elif frame_type == 0x4a: # 食指速度返回值
                self.x4a = list(response_data)
            elif frame_type == 0x4b: # 中指速度返回值
                self.x4b = list(response_data)
            elif frame_type == 0x4c: # 无名指速度返回值
                self.x4c = list(response_data)
            elif frame_type == 0x4d: # 小拇指速度返回值
                self.x4d = list(response_data)
            elif frame_type == 0xc1: # 版本号
                self.xc1 = list(response_data)
            elif frame_type == 0x51: # 大拇指转矩
                self.x51 = list(response_data)
            elif frame_type == 0x52: # 食指转矩
                self.x52 = list(response_data)
            elif frame_type == 0x53: # 中指转矩
                self.x53 = list(response_data)
            elif frame_type == 0x54: # 无名指转矩
                self.x54 = list(response_data)
            elif frame_type == 0x55: # 小拇指转矩
                self.x55 = list(response_data)
            elif frame_type == 0x59:
                self.x59 = list(response_data)
            elif frame_type == 0x5a:
                self.x5a = list(response_data)
            elif frame_type == 0x5b:
                self.x5b = list(response_data)
            elif frame_type == 0x5c:
                self.x5c = list(response_data)
            elif frame_type == 0x5d:
                self.x5d = list(response_data)
            elif frame_type == 0x61:
                self.x61 = list(response_data)
            elif frame_type == 0x62:
                self.x62 = list(response_data)
            elif frame_type == 0x63:
                self.x63 = list(response_data)
            elif frame_type == 0x64:
                self.x64 = list(response_data)
            elif frame_type == 0x65:
                self.x65 = list(response_data)
            elif frame_type == 0x90:
                self.x90 = list(response_data)
            elif frame_type == 0x91:
                self.x91 = list(response_data)
            elif frame_type == 0x92:
                self.x92 = list(response_data)
            elif frame_type == 0x93:
                self.x93 = list(response_data)
            elif frame_type == 0xb0: # 新传感器类型
                self.xb0 = list(response_data)
            elif frame_type == 0xb1: # 大拇指触觉传感器
                self.xb1 = list(response_data)
            elif frame_type == 0xb2: # 食指触觉传感器
                self.xb2 = list(response_data)
            elif frame_type == 0xb3: # 中指触觉传感器
                self.xb3 = list(response_data)
            elif frame_type == 0xb4: # 无名指触觉传感器
                self.xb4 = list(response_data)
            elif frame_type == 0xb5: # 小拇指触觉传感器
                self.xb5 = list(response_data)
            elif frame_type == 0xb6: # 手掌触觉传感器
                self.xb6 = list(response_data)

    # topic映射l21
    def joint_map(self, pose):
        # l21 CAN数据默认接收30个数据
        l21_pose = [0.0] * 30  # 初始化l21_pose为30个0.0

        # 映射表，通过字典简化映射关系
        mapping = {
            0: 10,  1: 5,   2: 0,   3: 15,  4: None,  5: 20,
            6: None, 7: 6,   8: 1,   9: 16,  10: None, 11: 21,
            12: None, 13: 7, 14: 2,  15: 17, 16: None, 17: 22,
            18: None, 19: 8,  20: 3,   21: 18, 22: None, 23: 23,
            24: None, 25: 9,  26: 4,   27: 19, 28: None, 29: 24
        }

        # 遍历映射字典，进行值的映射
        for l21_idx, pose_idx in mapping.items():
            if pose_idx is not None:
                l21_pose[l21_idx] = pose[pose_idx]

        return l21_pose

    # 将l21的状态值转换为CMD格式的状态值
    def state_to_cmd(self, l21_state):
        # l21 CAN默认接收30个数据，初始化pose为25个0.0
        pose = [0.0] * 25  # 原来控制l21的指令数据为25个

        # 映射关系，字典中存储l21_state索引和pose索引之间的映射关系
        mapping = {
            0: 10,  1: 5,   2: 0,   3: 15,  5: 20,  7: 6,
            8: 1,   9: 16,  11: 21, 13:7, 14: 2,  15: 17, 17: 22,
            19: 8,  20: 3,  21: 18, 23: 23, 25: 9,   26: 4,
            27: 19, 29: 24
        }
        # 遍历映射字典，更新pose的值
        for l21_idx, pose_idx in mapping.items():
            pose[pose_idx] = l21_state[l21_idx]
        return pose
    def action_play(self):
        self.send_command(0xA0,[])
    # 获取所有关节数据
    def get_current_status(self, j=''):
        self.send_command(FrameProperty.THUMB_POS, j,sleep_time=0.001)
        #time.sleep(0.001)
        self.send_command(FrameProperty.INDEX_POS,j,sleep_time=0.001)
        #time.sleep(0.001)
        self.send_command(FrameProperty.MIDDLE_POS,j,sleep_time=0.001)
        #time.sleep(0.001)
        self.send_command(FrameProperty.RING_POS,j,sleep_time=0.001)
        #time.sleep(0.001)
        self.send_command(FrameProperty.LITTLE_POS, j,sleep_time=0.001)
        #time.sleep(0.001)
        state= self.x41+ self.x42+ self.x43+ self.x44+ self.x45
        if len(state) == 30:
            l21_state = self.state_to_cmd(l21_state=state)
            return l21_state
        
    def get_current_state_topic(self):
        self.send_command(0x01,[])
        #time.sleep(0.001)
        self.send_command(0x02,[])
       # time.sleep(0.001)
        self.send_command(0x03,[])
        #time.sleep(0.001)
        self.send_command(0x04,[])
        #time.sleep(0.001)
        self.send_command(0x06,[])
        #time.sleep(0.001)
        state = self.x03+self.x02+self.x01+self.x04+self.x06
        return state
    
    def get_speed(self,j=''):
        self.send_command(FrameProperty.THUMB_SPEED, j) # 大拇指速度
        #time.sleep(0.01)
        self.send_command(FrameProperty.INDEX_SPEED, j) # 食指速度
        #time.sleep(0.01)
        self.send_command(FrameProperty.MIDDLE_SPEED, j) # 中指速度
        #time.sleep(0.01)
        self.send_command(FrameProperty.RING_SPEED, j) # 无名指速度
        #time.sleep(0.01)
        self.send_command(FrameProperty.LITTLE_SPEED, j) # 小拇指速度
        #time.sleep(0.01)
        speed = self.x49+ self.x4a+ self.x4b+ self.x4c+ self.x4d
        if len(speed) == 30:
            l21_speed = self.state_to_cmd(l21_state=speed)
            return l21_speed
    
    def get_finger_torque(self):
        return self.finger_torque()
    # def get_current(self):
    #     return self.x06
    def get_fault(self):
        self.get_thumbn_fault()
        #time.sleep(0.001)
        self.get_index_fault()
        #time.sleep(0.001)
        self.get_middle_fault()
        #time.sleep(0.001)
        self.get_ring_fault()
        #time.sleep(0.001)
        self.get_little_fault()
        #time.sleep(0.001)
        return [self.x59]+[self.x5a]+[self.x5b]+[self.x5c]+[self.x5d]
    def get_threshold(self):
        self.get_thumb_threshold()
        self.get_index_threshold()
        self.get_middle_threshold()
        self.get_ring_threshold()
        self.get_little_threshold()
        return [self.x61]+[self.x62]+[self.x63]+[self.x64]+[self.x65]
    def get_version(self):
        if self.xc1 == []:
            self.send_command(FrameProperty.HAND_HARDWARE_VERSION,[])
        return self.xc1
    def get_normal_force(self):
        self.send_command(FrameProperty.HAND_NORMAL_FORCE,[])
        return self.x90
    def get_tangential_force(self):
        self.send_command(FrameProperty.HAND_TANGENTIAL_FORCE,[])
        return self.x91
    def get_tangential_force_dir(self):
        self.send_command(FrameProperty.HAND_TANGENTIAL_FORCE_DIR,[])
        return self.x92
    def get_approach_inc(self):
        self.send_command(FrameProperty.HAND_APPROACH_INC,[])
        return self.x93
    
    def get_touch_type(self):
        '''获取触觉传感器类型数据'''
        self.send_command(FrameProperty.TOUCH_SENSOR_TYPE,[])
        #time.sleep(0.01)
        try:
            return self.xb0[0]
        except:
            pass
    def get_finger_torque(self):
        self.send_command(FrameProperty.THUMB_TORQUE,[])
        self.send_command(FrameProperty.INDEX_TORQUE,[])
        self.send_command(FrameProperty.MIDDLE_TORQUE,[])
        self.send_command(FrameProperty.RING_TORQUE,[])
        self.send_command(FrameProperty.LITTLE_TORQUE,[])
        return self.x51+self.x52+self.x53+self.x54+self.x55
    
    def get_torque(self):
        return self.get_finger_torque()
    def get_thumb_touch(self):
        '''获取大拇指触觉传感器数据'''
        self.send_command(FrameProperty.THUMB_TOUCH,[])
        #time.sleep(0.001)
        return self.xb1
    
    def get_index_touch(self):
        '''获取食指触觉传感器数据'''
        self.send_command(FrameProperty.INDEX_TOUCH,[])
        #time.sleep(0.001)
        return self.xb2
    
    def get_middle_touch(self):
        '''获取中指触觉传感器数据'''
        self.send_command(FrameProperty.MIDDLE_TOUCH,[])
        #time.sleep(0.001)
        return self.xb3
    
    def get_ring_touch(self):
        '''获取无名指触觉传感器数据'''
        self.send_command(FrameProperty.RING_TOUCH,[])
        return self.xb4
    
    def get_little_touch(self):
        '''获取小拇指触觉传感器数据'''
        self.send_command(FrameProperty.LITTLE_TOUCH,[])
        return self.xb5
    
    def get_palm_touch(self):
        '''获取手掌触觉传感器数据'''
        self.send_command(FrameProperty.PALM_TOUCH,[])
        return self.xb6
    
    def get_force(self):
        '''获取压感数据'''
        return [self.x90,self.x91 , self.x92 , self.x93]
    
    def get_touch(self):
        '''获取触觉传感器数据'''
        self.get_thumb_touch()
        self.get_index_touch()
        self.get_middle_touch()
        self.get_ring_touch()
        self.get_little_touch()
        self.get_palm_touch()
        try:
            return [self.xb1[1],self.xb2[1] , self.xb3[1] , self.xb4[1],self.xb5[1],self.xb6[1]]
        except:
            pass
    


    def get_current(self):
        '''暂不支持'''
        return [0] * 21
    def get_temperature(self):
        self.get_thumb_threshold()
        self.get_index_threshold()
        self.get_middle_threshold()
        self.get_ring_threshold()
        self.get_little_threshold()
        return self.x61+self.x62+self.x63+self.x64+self.x65
    
    def get_finger_order(self):
        return [
            "thumb_root",
            "index_finger_root",
            "middle_finger_root",
            "ring_finger_root",
            "little_finger_root",
            "thumb_abduction",
            "index_finger_abduction",
            "middle_finger_abduction",
            "ring_finger_abduction",
            "little_finger_abduction",
            "thumb_roll",
            "reserved",
            "reserved",
            "reserved",
            "reserved",
            "thumb_middle_joint",
            "reserved",
            "reserved",
            "reserved",
            "reserved",
            "thumb_tip",
            "index_finger_tip",
            "middle_finger_tip",
            "ring_finger_tip",
            "little_finger_tip"
        ]


    def close_can_interface(self):
        if self.bus:
            self.bus.shutdown()  # 关闭 CAN 总线