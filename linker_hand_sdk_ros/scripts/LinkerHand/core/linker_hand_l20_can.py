import sys
import time
import can
import threading
from enum import Enum

class FrameProperty(Enum):
    INVALID_FRAME_PROPERTY = 0x00  # Invalid CAN frame property | No return
    JOINT_PITCH_R = 0x01           # Short frame pitch angle - finger base bending | Returns this type of data
    JOINT_YAW_R = 0x02             # Short frame yaw angle - finger lateral swing, control gap | Returns this type of data
    JOINT_ROLL_R = 0x03            # Short frame roll angle - only used for thumb auxiliary | Returns this type of data
    JOINT_TIP_R = 0x04             # Short frame fingertip angle control | Returns this type of data
    JOINT_SPEED_R = 0x05           # Short frame speed - motor running speed control | Returns this type of data
    JOINT_CURRENT_R = 0x06         # Short frame current - motor running current feedback | Returns this type of data
    JOINT_FAULT_R = 0x07           # Short frame fault - motor running fault feedback | Returns this type of data
    REQUEST_DATA_RETURN = 0x09     # Request data return | Returns all data
    JOINT_PITCH_NR = 0x11          # Pitch angle - finger base bending | Does not return this type of data
    JOINT_YAW_NR = 0x12            # Yaw angle - finger lateral swing, control gap | Does not return this type of data
    JOINT_ROLL_NR = 0x13           # Roll angle - only used for thumb auxiliary | Does not return this type of data
    JOINT_TIP_NR = 0x14            # Fingertip angle control | Does not return this type of data
    JOINT_SPEED_NR = 0x15          # Speed - motor running speed control | Does not return this type of data
    JOINT_CURRENT_NR = 0x16        # Current - motor running current feedback | Does not return this type of data
    JOINT_FAULT_NR = 0x17          # Fault - motor running fault feedback | Does not return this type of data
    HAND_UID = 0xC0                # Device unique identifier (read-only)
    HAND_HARDWARE_VERSION = 0xC1   # Hardware version (read-only)
    HAND_SOFTWARE_VERSION = 0xC2   # Software version (read-only)
    HAND_COMM_ID = 0xC3            # Device ID (read/write, 1 byte)
    HAND_SAVE_PARAMETER = 0xCF     # Save parameters (write-only)

class LinkerHandL20Can:
    def __init__(self, can_channel='can0', baudrate=1000000, can_id=0x28):
        self.can_id = can_id
        self.running = True
        self.x05, self.x06, self.x07 = [], [], []
        
        # Initialize CAN bus based on the operating system
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

        # Start the receiving thread
        self.receive_thread = threading.Thread(target=self.receive_response)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def send_command(self, frame_property, data_list):
        """
        Send a command to the CAN bus
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
        Receive and process response messages from the CAN bus
        """
        while self.running:
            try:
                msg = self.bus.recv(timeout=1.0)  # Blocking receive, 1-second timeout
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

    def set_joint_speed(self, speed):
        self.x05 = speed
        self.send_command(0x05, speed)

    def set_electric_current(self, e_c=[]):
        self.send_command(0x06, e_c)

    def get_normal_force(self):
        self.send_command(0x20, [])

    def get_tangential_force(self):
        self.send_command(0x21, [])

    def get_tangential_force_dir(self):
        self.send_command(0x22, [])

    def get_approach_inc(self):
        self.send_command(0x23, [])

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

    def set_joint_positions(self, position):
        if len(position) != 20:
            print("L20 finger joint length is incorrect")
            return
        finger_base, yaw_angles, thumb_yaw, finger_tip = self.pose_slice(position)
        self.set_thumb_roll(thumb_yaw)  # Thumb lateral movement
        self.set_finger_tip(finger_tip)  # Fingertip movement
        self.set_finger_base(finger_base)  # Finger base movement
        self.set_finger_middle(yaw_angles)  # Lateral movement

    def set_speed(self, speed=[]):
        self.send_command(0x05, speed)

    def set_torque(self, torque=[]):
        """Set torque. L20 does not support this."""
        print("Setting torque is not supported for L20")

    def set_current(self, current=[]):
        """Set current."""
        self.set_electric_current(e_c=current)

    def get_version(self):
        """Get version. Currently not supported."""
        return [0] * 5

    def get_current_status(self):
        """Get current finger joint status."""
        self.send_command(0x01, [])
        self.send_command(0x02, [])
        self.send_command(0x03, [])
        self.send_command(0x04, [])
        return self.x01 + self.x02 + self.x03 + self.x04

    def get_speed(self):
        """Get current motor speed."""
        self.send_command(0x05, [0])
        time.sleep(0.001)
        return self.x05

    def get_current(self):
        """Get current."""
        self.send_command(0x06, [0])
        return self.x06

    def get_torque(self):
        """Get current motor torque. L20 does not support this."""
        return [0] * 5

    def get_fault(self):
        return self.x07

    def get_temperature(self):
        """Get motor temperature. L20 does not support this."""
        return [0] * 10

    def clear_faults(self):
        """Clear motor faults."""
        self.send_command(0x07, [1, 1, 1, 1, 1])

    def get_touch_type(self):
        """Get touch type. Not supported."""
        return [-1] * 5

    def get_touch(self):
        """Get touch data. Not supported."""
        return [-1] * 6

    def get_faults(self):
        """Get motor fault codes."""
        self.send_command(0x07, [])
        return self.x07

    def get_force(self):
        """Get pressure sensing data."""
        return [self.normal_force, self.tangential_force, self.tangential_force_dir, self.approach_inc]

    def close_can_interface(self):
        if self.bus:
            self.bus.shutdown()  # Close CAN bus