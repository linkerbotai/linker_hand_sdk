#!/usr/bin/env python3
import rospy, time,json,random,sys,os,threading,math,signal,ctypes
from LinkerHand.utils.RM_API2.Python.Robotic_Arm.rm_robot_interface import *

from utils.color_msg import ColorMsg


class LinkerHandL10For485:
    def __init__(self,ip="192.168.1.18", linkerhand_id=39, modbus_port = 1,modbus_baudrate = 115200,modbus_timeout = 5):
        '''
        初始化睿尔曼485接口
        :params
        arm: 初始化的睿尔曼机械臂
        linkerhand_id: 灵巧手ID 左手40 右手39
        '''
        # modbus相关参数
        self.modbus_port = modbus_port
        self.modbus_baudrate = modbus_baudrate
        self.modbus_timeout = modbus_timeout
        # 灵巧手ID
        self.linkerhand_id = linkerhand_id
        self.hand_modbus_register = {
            'ANGLE_SET': {'addr': 0, 'unit': ctypes.c_byte, 'length': 10},
            'SPEED_SET': {'addr': 10, 'unit': ctypes.c_byte, 'length': 5},
            'MAX_TORQUE_SET': {'addr': 15, 'unit': ctypes.c_byte, 'length': 5},
            'ANGLE_STATUS': {'addr': 0, 'unit': ctypes.c_byte, 'length': 10},
            'FORCE_STATUS': {'addr': 20, 'unit': ctypes.c_byte, 'length': 20},
        }
        #self.arm.rm_set_modbus_mode(self.modbus_port,self.modbus_baudrate,self.modbus_timeout)
        #modbus_state = self.arm.rm_set_controller_rs485_mode(self.modbus_port,self.modbus_baudrate)
        
        # 必须先设置手的速度和扭矩，否则无法移动
        self.set_speed()
        #self.set_torque()

    def set_speed(self, speed=[120,200,200,200,200]):
        """
        设置机械手的速度。
        :param speed: list, 范围为 0-255。
        """
        # tmp_speed = [x & 0xFF for x in speed]
        # set_speed_state = []
        # for i in range(self.hand_modbus_register['SPEED_SET']['length']):
        #     write_params = rm_peripheral_read_write_params_t(self.modbus_port, self.hand_modbus_register['SPEED_SET']['addr'] + i, self.linkerhand_id)
        #     rs = self.arm.rm_write_single_register(write_params, tmp_speed[i])
        #     set_speed_state.append(rs)
        #     time.sleep(0.01)
        # if all(x == 0 for x in set_speed_state):
        #     ColorMsg(msg=f"速度设置成功:{speed}", color="green")
        # else:
        #     ColorMsg(msg=f"速度设置失败:{speed}", color="red")

        
        self.arm = RoboticArm(rm_thread_mode_e.RM_TRIPLE_MODE_E)
        self.handle = self.arm.rm_create_robot_arm("192.168.1.18", 8080,0)
        print("*" * 20)
        print(self.handle.id)
        modbus_state = self.arm.rm_set_tool_rs485_mode(mode=1,baudrate=115200)
        # print(modbus_state)
        write_params = rm_modbus_rtu_write_params_t(
            address=0,            # 功能地址，对应 Thumb_Pitch
            device=40,            # 外设设备地址
            type=1,               # 控制器端 modbus 主机
            num=5,                # 只写一个值
            data=[255]*5           # 写入的值
        )
        rs = self.arm.rm_write_modbus_rtu_registers(write_params)
        # param = rm_modbus_rtu_read_params_t(0, 40, 1, 5)
        
        # rs = self.arm.rm_read_modbus_rtu_input_registers(param)

        # read_params = rm_modbus_rtu_read_params_t(address=9, device=0x28, type=0, num=1)
        # rs = self.arm.rm_read_modbus_rtu_input_registers(read_params)
        print("_-" * 20)
        print(rs)
    
    def set_torque(self, force=[200,200,200,200,200]):
        """
        设置机械手的扭矩
        :param force: list, 范围为 0-255。
        """
        tmp_force = [x & 0xFF for x in force]
        set_force_state = []
        for i in range(self.hand_modbus_register['MAX_TORQUE_SET']['length']):
            write_params = rm_peripheral_read_write_params_t(self.modbus_port, self.hand_modbus_register['MAX_TORQUE_SET']['addr'] + i, self.linkerhand_id)
            rs = self.arm.rm_write_single_register(write_params, tmp_force[i])
            time.sleep(0.01)
            set_force_state.append(rs)
        if all(x == 0 for x in set_force_state):
            ColorMsg(msg=f"扭矩设置成功:{force}", color="green")
        else:
            ColorMsg(msg=f"扭矩设置失败:{force}", color="red")

    def set_joint_positions(self, pose=[80,80,80,80,80,80,80,80,80,80]):
        """
        设置灵巧手的运动范围
        :param angle: list, 范围为 0-255。
        """
        tmp_angle = [int(x) & 0xFF for x in pose]
        set_angle_state = []
        for i in range(self.hand_modbus_register['ANGLE_SET']['length']):
            write_params = rm_peripheral_read_write_params_t(self.modbus_port, self.hand_modbus_register['ANGLE_SET']['addr'] + i, self.linkerhand_id)
            rs = self.arm.rm_write_single_register(write_params, tmp_angle[i])
            time.sleep(0.01)
            set_angle_state.append(rs)
        if all(x == 0 for x in set_angle_state):
            ColorMsg(msg=f"手指运动成功:{pose}", color="green")
        else:
            ColorMsg(msg=f"手指运动失败:{pose}", color="red")

    def get_version(self):
        '''获取版本 暂不支持'''
        return [-1] * 5
    def get_current(self):
        '''获取当前电流 暂不支持'''
        return [-1] * 5
    def get_current_status(self):
        '''获取当前状态 暂不支持'''
        return [-1] * 10
    def get_touch_type(self):
        '''获取压感类型 暂不支持'''
        return [-1] * 5
    def get_force(self):
        '''获取压感数据 暂不支持'''
        return [-1] * 5
    def get_touch(self):
        '''获取压感数据 暂不支持'''
        return [-1] * 5
    def get_torque(self):
        '''获取扭矩 暂不支持'''
        return [-1] * 5
    def get_temperature(self):
        '''获取电机温度 暂不支持'''
        return [-1] * 10
    def get_fault(self):
        '''获取电机故障 暂不支持'''
        return [-1] * 10

