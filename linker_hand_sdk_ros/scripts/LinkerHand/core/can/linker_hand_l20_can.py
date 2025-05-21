import sys
import time
import can
import threading
from enum import Enum

class FrameProperty(Enum):
    INVALID_FRAME_PROPERTY = 0x00  # Invalid CAN frame property | No return
    JOINT_PITCH_R = 0x01           # Short frame pitch angle - finger base flexion | Returns this type of data
    JOINT_YAW_R = 0x02             # Short frame yaw angle - finger abduction/adduction | Returns this type of data
    JOINT_ROLL_R = 0x03            # Short frame roll angle - only used for thumb | Returns this type of data
    JOINT_TIP_R = 0x04             # Short frame fingertip angle control | Returns this type of data
    JOINT_SPEED_R = 0x05           # Short frame speed - motor running speed control | Returns this type of data
    JOINT_CURRENT_R = 0x06         # Short frame current - motor running current feedback | Returns this type of data
    JOINT_FAULT_R = 0x07           # Short frame fault - motor running fault feedback | Returns this type of data
    REQUEST_DATA_RETURN = 0x09     # Request data return | Returns all data
    JOINT_PITCH_NR = 0x11          # Pitch angle - finger base flexion | No return for this type of data
    JOINT_YAW_NR = 0x12            # Yaw angle - finger abduction/adduction | No return for this type of data
    JOINT_ROLL_NR = 0x13           # Roll angle - only used for thumb | No return for this type of data
    JOINT_TIP_NR = 0x14            # Fingertip angle control | No return for this type of data
    JOINT_SPEED_NR = 0x15          # Speed - motor running speed control | No return for this type of data
    JOINT_CURRENT_NR = 0x16        # Current - motor running current feedback | No return for this type of data
    JOINT_FAULT_NR = 0x17          # Fault - motor running fault feedback | No return for this type of data
    HAND_UID = 0xC0                # Device unique identifier Read only --------
    HAND_HARDWARE_VERSION = 0xC1   # Hardware version Read only --------
    HAND_SOFTWARE_VERSION = 0xC2   # Software version Read only --------
    HAND_COMM_ID = 0xC3            # Device ID Read/Write 1 byte
    HAND_SAVE_PARAMETER = 0xCF     # Save parameters Write only --------


class LinkerHandL20Can:
    def __init__(self, can_channel='can0', baudrate=1000000, can_id=0x28):
        self.can_id = can_id
        self.running = True
        self.x05, self.x06, self.x07 = [],[],[]
        
        # Initialize CAN bus according to operating system
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

        # Initialize data storage
        self.x01, self.x02, self.x03, self.x04 = [[0.0] * 5 for _ in range(4)]
        self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc = \
            [[0.0] * 5 for _ in range(4)]

        # Start receive thread
        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_command(self, frame_property, data_list):
        print("66666")
        """
        Send command to CAN bus
        :param frame_property: Data frame property
        :param data_list: Data payload
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
        Receive and process CAN bus response messages
        """
        while self.running:
            try:
                msg = self.bus.recv(timeout=1.0)  # Blocking receive, 1 second timeout
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
            elif frame_type == 0xC0:
                print(f"Device ID info: {response_data}")
                if self.can_id == 0x28:
                    self.right_hand_info = response_data
                elif self.can_id == 0x27:
                    self.left_hand_info = response_data
            elif frame_type == 0x05:
                self.x05 = list(response_data)
            elif frame_type == 0x06:
                self.x06 = list(response_data)
            elif frame_type == 0x07:
                self.x07 = list(response_data)
            elif frame_type == 0x20:
                d = list(response_data)
                self.normal_force = [float(i) for i in d] 
            elif frame_type == 0x21:
                d = list(response_data)
                self.tangential_force = [float(i) for i in d]
            elif frame_type == 0x22:
                d = list(response_data)
                self.tangential_force_dir = [float(i) for i in d]
            elif frame_type == 0x23:
                d = list(response_data)
                self.approach_inc = [float(i) for i in d]
    def pose_slice(self, p):
        """Slice the joint array into finger action arrays"""
        try:
            finger_base = [int(val) for val in p[0:5]]   # Finger base
            yaw_angles = [int(val) for val in p[5:10]]    # Yaw
            thumb_yaw = [int(val) for val in p[10:15]]     # Thumb yaw to palm, others are 0
            finger_tip = [int(val) for val in p[15:20]]    # Fingertip flexion
            return finger_base, yaw_angles, thumb_yaw, finger_tip
        except Exception as e:
            print(e)
    def set_joint_positions(self, position):
        if len(position) != 20:
            print("L20 finger joint length is incorrect")
            return
        finger_base, yaw_angles, thumb_yaw, finger_tip = self.pose_slice(position)
        self.set_thumb_roll(thumb_yaw) # Thumb yaw to palm movement
        self.set_finger_tip(finger_tip) # Fingertip movement
        self.set_finger_base(finger_base) # Finger base movement
        self.set_finger_middle(yaw_angles) # Yaw movement
    def set_speed(self, speed=[]):
        self.send_command(0x05,speed)
    def set_torque(self, torque=[]):
        '''Set torque, not supported for L20'''
        print("Set torque, not supported for L20")
    def set_current(self, current=[]):
        '''Set current'''
        self.set_electric_current(e_c=current)
    def get_version(self):
        '''Get version, currently not supported'''
        return [0] * 5
    def get_current_status(self):
        '''Get current finger joint status'''
        self.send_command(0x01,[])
        self.send_command(0x02,[])
        self.send_command(0x03,[])
        self.send_command(0x04,[])
        return self.x01 + self.x02 + self.x03 + self.x04
    def get_speed(self):
        '''Get current motor speed'''
        self.send_command(0x05, [0])
        time.sleep(0.001)
        return self.x05
    def get_current(self):
        '''Get current threshold'''
        self.send_command(0x06, [0])
        return self.x06
    def get_torque(self):
        '''Get current motor torque, not supported for L20'''
        return [0] * 5
    def get_fault(self):
        return self.x07
    def get_temperature(self):
        '''Get motor temperature, not supported for L20'''
        return [0]* 10
    def clear_faults(self):
        '''Clear motor faults'''
        self.send_command(0x07, [1, 1, 1, 1, 1])

    def get_touch_type(self):
        '''Get touch type, not supported'''
        return [-1] * 5
    
    def get_touch(self):
        '''Get touch data, not supported'''
        return [-1] * 6

    def get_faults(self):
        '''Get motor fault codes'''
        self.send_command(0x07, [])
        return self.x07
    def get_force(self):
        '''Get pressure sensor data'''
        return [self.normal_force,self.tangential_force,self.tangential_force_dir,self.approach_inc]
    def close_can_interface(self):
        if self.bus:
            self.bus.shutdown()  # Close CAN bus