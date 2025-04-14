#!/usr/bin/env python3
import rospy,rospkg
import signal
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import can
import json
import yaml
import time
import threading
import sys
import os
import subprocess
from std_msgs.msg import Header, Float32MultiArray
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.linker_hand_l20_can import LinkerHandL20Can
from utils.linker_hand_l10_can import LinkerHandL10Can
from utils.color_msg import ColorMsg
from utils.open_can import OpenCan
global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_name = "linker_hand_sdk_ros"
package_path = rospack.get_path(package_name)

class LinkerHandController:
    def __init__(self):
        self.password = ""
        self.left_hand_exists = None
        self.right_hand_exists = None
        self.left_hand_type = None
        self.right_hand_type = None
        self.left_hand_joint = None
        self.right_hand_joint = None
        self.can_status = False
        self.left_hand_can = None
        self.right_hand_can = None
        self.load_yaml()
        time.sleep(0.1)
        ColorMsg(msg=f"SDK version:{self.sdk_version}", color="green")
        self.open_can0()
        time.sleep(0.01)
        self.is_can_up_sysfs()
        
        self.check_left_hand()
        self.check_right_hand()
        self.hand_setting_sub = rospy.Subscriber("/cb_hand_setting_cmd", String, self.hand_setting_cb)
        time.sleep(0.1)
        self.position_send()

    # 验证左手状态
    def check_left_hand(self):
        if self.left_hand_exists == True:
            if self.left_hand_joint == "L20":
                ColorMsg(msg="左手L20配置文件中已开启", color="green")
                self.left_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x28, config=self.config)
                finger_base, yaw_angles, thumb_yaw, finger_tip = self.pose_slice(p=[255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255])
                self.left_hand_can_send(finger_base=finger_base,yaw_angles=yaw_angles,thumb_yaw=thumb_yaw,finger_tip=finger_tip)
                self.left_hand_can.set_joint_speed([250,250,250,250,250])
                ColorMsg(msg=f"当前左手L20速度为：{self.left_hand_can.get_speed()}", color="green")
            elif self.left_hand_joint == "L10":
                self.left_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x28, config=self.config)
                self.left_hand_can_send_l10(last_pose=[255, 200, 255, 255, 255, 255, 180, 180, 180, 41])
                self.left_hand_can.set_joint_speed_l10([120,250,250,250,250])
                ColorMsg(msg="左手L10配置文件中已开启", color="green")
                ColorMsg(msg=f"当前左手L10速度为：{self.left_hand_can.get_speed()}", color="green")
            self.left_hand_position = []
            self.left_hand_sub = rospy.Subscriber("/cb_left_hand_control_cmd", JointState, self.left_hand_cb, queue_size=1)
            self.left_hand_status_pub = rospy.Publisher("/cb_left_hand_state", JointState, queue_size=10)
            if self.left_hand_force == True:
                self.left_hand_pressure_pub = rospy.Publisher("/cb_left_hand_force", Float32MultiArray, queue_size=10)
            self.left_hand_info_pub = rospy.Publisher("/cb_left_hand_info", String, queue_size=10)
            

            

    # 验证右手状态
    def check_right_hand(self):
        if self.right_hand_exists == True:
            if self.right_hand_joint == "L20":
                ColorMsg(msg="右手L20配置文件中已开启", color="green")
                self.right_hand_can = LinkerHandL20Can(can_channel="can0", baudrate=1000000, can_id=0x27, config=self.config)
                finger_base, yaw_angles, thumb_yaw, finger_tip = self.pose_slice(p=[255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255])
                self.right_hand_can_send(finger_base=finger_base,yaw_angles=yaw_angles,thumb_yaw=thumb_yaw,finger_tip=finger_tip)
                self.right_hand_can.set_joint_speed([180,250,250,250,250])
                ColorMsg(msg=f"当前右手L20速度为：{self.right_hand_can.get_speed()}", color="green")
            elif self.right_hand_joint == "L10":
                self.right_hand_can = LinkerHandL10Can(can_channel="can0", baudrate=1000000, can_id=0x27, config=self.config)
                self.right_hand_can_send_l10(last_pose=[255, 128, 255, 255, 255, 255, 128, 128, 128, 128])
                self.right_hand_can.set_joint_speed_l10([250,250,250,250,250])
                ColorMsg(msg="右手L10配置文件中已开启", color="green")
                ColorMsg(msg=f"当前右手L10速度为：{self.right_hand_can.get_speed()}", color="green")
            self.right_hand_position = []
            self.right_hand_sub = rospy.Subscriber("/cb_right_hand_control_cmd", JointState, self.right_hand_cb, queue_size=1)
            self.right_hand_status_pub = rospy.Publisher("/cb_right_hand_state", JointState, queue_size=10)
            if self.right_hand_force == True:
                self.right_hand_pressure_pub = rospy.Publisher("/cb_right_hand_force", Float32MultiArray, queue_size=10)
            self.right_hand_info_pub = rospy.Publisher("/cb_right_hand_info", String, queue_size=10)
            

    # 左手接收到话题将数据处理后发送到CAN驱动左手运动
    def left_hand_cb(self, msg):
        position = msg.position
        if self.validate_joint_positions(positions=position) == False:
            ColorMsg(msg="手指关节数值不在正确范围之内", color="red")
            return
        velocity = msg.velocity
        effort = msg.effort
        if len(position) == 20 and self.left_hand_joint == "L20":
            self.left_hand_position = position
            self.left_hand_velocity = velocity
            self.left_hand_effort = effort
        elif len(position) == 10 and self.left_hand_joint == "L10":
            self.left_hand_position = position
            self.left_hand_velocity = velocity
            self.left_hand_effort = effort
        else:
            ColorMsg(msg="左手关节数与配置信息不符", color="red")

    def right_hand_cb(self, msg):
        position = msg.position
        if self.validate_joint_positions(positions=position) == False:
            ColorMsg(msg="手指关节数值不在正确范围之内", color="red")
            return
        velocity = msg.velocity
        effort = msg.effort
        if len(position) == 20 and self.right_hand_joint == "L20":
            self.right_hand_position = position
            self.right_hand_velocity = velocity
            self.right_hand_effort = effort
        elif len(position) == 10 and self.right_hand_joint == "L10":
            self.right_hand_position = position
            self.right_hand_velocity = velocity
            self.right_hand_effort = effort
        else:
            ColorMsg(msg="左手关节数与配置信息不符", color="red")

    # 验证接收到的手指关节坐标数值是否在0~255范围之内
    def validate_joint_positions(self, positions):
        # 检查 positions 列表中的每个值是否在 0 到 255 范围内
        for pos in positions:
            if int(pos) < 0 or int(pos) > 255:
                return False
        return True

    def position_send(self):
        while True:
            ''' ---------------左手------------------ '''
            if self.left_hand_exists == True:
                # 发送左手数据
                if len(self.left_hand_position) >= 16 and self.left_hand_joint == "L20":
                    finger_base, yaw_angles, thumb_yaw, finger_tip = self.pose_slice(p=self.left_hand_position)
                    self.left_hand_can_send(finger_base=finger_base,yaw_angles=yaw_angles,thumb_yaw=thumb_yaw,finger_tip=finger_tip)
                    # 获取L20左手错误状态
                    self.left_hand_can.get_faults()
                    # 获取L20左手当前电流
                    self.left_hand_can.get_electric_current()
                elif len(self.left_hand_position) == 10 and self.left_hand_joint == "L10":
                    self.left_hand_can_send_l10(last_pose=self.left_hand_position)
                # 发送左手状态
                self.left_hand_status()
                # 左手压力传感器
                if self.left_hand_force == True:
                    self.left_hand_touch()
            ''' ---------------右手------------------ '''
            if self.right_hand_exists == True:
            # 发送右手数据
                if len(self.right_hand_position) >= 16 and self.right_hand_joint == "L20":
                    finger_base, yaw_angles, thumb_yaw, finger_tip = self.pose_slice(p=self.right_hand_position)
                    self.right_hand_can_send(finger_base=finger_base,yaw_angles=yaw_angles,thumb_yaw=thumb_yaw,finger_tip=finger_tip)
                    # 获取L20右手错误状态
                    self.right_hand_can.get_faults()
                    # 获取L20右手当前电流
                    self.right_hand_can.get_electric_current()
                elif len(self.right_hand_position) == 10 and self.right_hand_joint == "L10":
                    self.right_hand_can_send_l10(last_pose=self.right_hand_position)
                #发送右手状态
                self.right_hand_status()
                # 右手压力传感器
                if self.right_hand_force == True:
                    self.right_hand_touch()
    # L20发送can数据
    def left_hand_can_send(self,finger_base, yaw_angles, thumb_yaw, finger_tip):
        self.left_hand_can.set_thumb_roll(thumb_yaw) # 大拇想手心横摆指移动
        self.left_hand_can.set_finger_tip(finger_tip) # 指尖移动
        self.left_hand_can.set_finger_base(finger_base) # 手指根部移动
        self.left_hand_can.set_finger_middle(yaw_angles) # 横摆移动
    # L10发送can数据
    def left_hand_can_send_l10(self,last_pose):
        self.left_hand_can.set_joint_positions(last_pose)
    # L20发送can数据
    def right_hand_can_send(self,finger_base, yaw_angles, thumb_yaw, finger_tip):
        self.right_hand_can.set_thumb_roll(thumb_yaw) # 大拇想手心横摆指移动
        self.right_hand_can.set_finger_tip(finger_tip) # 指尖移动
        self.right_hand_can.set_finger_base(finger_base) # 手指根部移动
        self.right_hand_can.set_finger_middle(yaw_angles) # 横摆移动
    # L10发送can数据
    def right_hand_can_send_l10(self,last_pose):
        self.right_hand_can.set_joint_positions(last_pose)

    def left_hand_status(self):
        if self.left_hand_exists:
            if self.left_hand_joint == "L20":
                current_pose = self.left_hand_can.get_current_status()
                data = {
                    "left_hand":{
                        "version": self.left_hand_can.get_version(),
                        "hand_joint": self.left_hand_joint,
                        "speed": self.left_hand_can.get_speed(),
                        "current": self.left_hand_can.get_current(),
                        "fault": self.left_hand_can.get_fault(),
                        "motor_temperature": self.left_hand_can.get_temperature()
                    }
                }
            if self.left_hand_joint == "L10":
                current_pose = self.left_hand_can.get_current_status()
                data = {
                    "left_hand":{
                        "version": self.left_hand_can.get_version(),
                        "hand_joint": self.left_hand_joint,
                        "speed": self.left_hand_can.get_speed(),
                        "max_press_rco": self.left_hand_can.get_press(),
                        "fault": self.left_hand_can.get_fault(),
                        "motor_temperature": self.left_hand_can.get_temperature()
                    }
                }
            msg = self.create_joint_state_msg(current_pose, self.left_hand_names)
            info = String()
            info.data = json.dumps(data)
            self.left_hand_info_pub.publish(info)
            self.left_hand_status_pub.publish(msg)

    def right_hand_status(self):
        if self.right_hand_exists:
            if self.right_hand_joint == "L20":
                current_pose = self.right_hand_can.get_current_status()
                data = {
                    "right_hand":{
                        "version": self.right_hand_can.get_version(),
                        "hand_joint": self.right_hand_joint,
                        "speed": self.right_hand_can.get_speed(),
                        "current": self.right_hand_can.get_current(),
                        "fault": self.right_hand_can.get_fault(),
                        "motor_temperature": self.right_hand_can.get_temperature()
                    }
                }
            if self.right_hand_joint == "L10":
                current_pose = self.right_hand_can.get_current_status()
                data = {
                    "right_hand":{
                        "version": self.right_hand_can.get_version(),
                        "hand_joint": self.right_hand_joint,
                        "speed": self.right_hand_can.get_speed(),
                        "max_press_rco": self.right_hand_can.get_press(),
                        "fault": self.right_hand_can.get_fault(),
                        "motor_temperature": self.right_hand_can.get_temperature()
                    }
                }
            msg = self.create_joint_state_msg(current_pose, self.right_hand_names)
            info = String()
            info.data = json.dumps(data)
            self.right_hand_info_pub.publish(info)
            self.right_hand_status_pub.publish(msg)

    def pose_slice(self, p):
        """将关节数组切片为手指动作数组"""
        try:
            finger_base = [int(val) for val in p[0:5]]   # 手指根部
            yaw_angles = [int(val) for val in p[5:10]]    # 横摆
            thumb_yaw = [int(val) for val in p[10:15]]     # 拇指向手心横摆，其他为0
            finger_tip = [int(val) for val in p[15:20]]    # 指尖弯曲
            return finger_base, yaw_angles, thumb_yaw, finger_tip
        except Exception as e:
            print(e)
            ColorMsg(msg="手部关节数据必须是正整数，范围:0~255之间", color="red")
    
    def create_joint_state_msg(self, position, names):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.name = names
        msg.position = list(map(float, position))
        msg.velocity = [0.0] * len(position)
        msg.effort = [0.0] * len(position)
        return msg
    # 左手压力传感器
    def left_hand_touch(self):
        self.left_hand_can.get_normal_force()
        self.left_hand_can.get_tangential_force()
        self.left_hand_can.get_tangential_force_dir()
        self.left_hand_can.get_approach_inc()
        d = self.left_hand_can.get_force()
        try:
            #print(d)
            msg = Float32MultiArray()
            msg.data = [item for sublist in d for item in sublist]
            self.left_hand_pressure_pub.publish(msg)
        except Exception as e:
            print(e)
    # 右手压力传感器
    def right_hand_touch(self):
        self.right_hand_can.get_normal_force()
        self.right_hand_can.get_tangential_force()
        self.right_hand_can.get_tangential_force_dir()
        self.right_hand_can.get_approach_inc()
        d = self.right_hand_can.get_force()
        try:
            #print(d)
            msg = Float32MultiArray()
            msg.data = [item for sublist in d for item in sublist]
            self.right_hand_pressure_pub.publish(msg)
        except Exception as e:
            print(e)
    
    def hand_setting_cb(self, msg):
        hand_left, hand_right = False, False
        data = json.loads(msg.data)
        print(f"收到设置命令：{data['setting_cmd']}")
        print(data)
        #except:
            #ColorMsg(msg="设置命令参数不正确", color="red")
        if data["params"]["hand_type"] == "left" and self.left_hand_exists:
            hand = self.left_hand_can
            hand_left = True
        elif data["params"]["hand_type"] == "right" and self.right_hand_exists:
            hand = self.right_hand_can
            hand_right = True
        else:
            print("请指定要设定的手部位")
            return
        # 设置最大扭矩
        if data["setting_cmd"] == "set_max_torque_limits": # 设置最大扭矩
            # 首先判断左右手
            if data["params"]["hand_type"] == "left":
                if self.left_hand_joint == "L10":# 判断是否为L10
                    torque = int(data["params"]["torque"])
                    ColorMsg(msg=f"设置L10左手最大扭矩为{torque}", color="yellow")
                    hand.set_max_torque_limits(pressures=[torque] * 5, type="set")
                elif self.left_hand_joint == "L20":# 判断是否为L20
                    ColorMsg(msg=f"L20左手不支持扭矩设置", color="red")
                    pass
            if data["params"]["hand_type"] == "right":
                if self.right_hand_joint == "L10":# 判断是否为L10
                    torque = int(data["params"]["torque"])
                    ColorMsg(msg=f"设置L10左手最大扭矩为{torque}", color="yellow")
                    hand.set_max_torque_limits(pressures=[torque] * 5, type="set")
                elif self.right_hand_joint >= 16:# 判断是否为L20
                    ColorMsg(msg=f"L20右手不支持扭矩设置", color="red")
                    pass
            
        if data["setting_cmd"] == "set_speed": # 设置速度
            if isinstance(data["params"]["speed"], list) == True:
                speed = data["params"]["speed"]
            else:
                speed = [int(data["params"]["speed"])] * 5
            hand_type = data["params"]["hand_type"]
            if hand_left == True and self.left_hand_joint == "L10" and hand_type=="left":
                hand.set_joint_speed_l10(speed=speed)
                speed = hand.get_speed()
                ColorMsg(msg=f"设置L10左手速度为{speed}", color="yellow")
            elif hand_right == True and self.right_hand_joint == "L10" and hand_type=="right":
                hand.set_joint_speed_l10(speed=speed)
                speed = hand.get_speed()
                ColorMsg(msg=f"设置L10右手速度为{speed}", color="yellow")
            elif hand_left == True and self.left_hand_joint == "L20" and hand_type=="left":
                hand.set_joint_speed(speed=speed)
            elif hand_right == True and self.right_hand_joint == "L20" and hand_type=="right":
                hand.set_joint_speed(speed=speed)

        
        if data["setting_cmd"] == "clear_faults": # 清除错误
            if hand_left == True and self.left_hand_joint == "L10" :
                ColorMsg(msg=f"L10左手不能清除错误")
            elif hand_right == True and self.right_hand_joint == "L10" :
                ColorMsg(msg=f"L10右手不能清除错误")
            else:
                hand.clear_faults()
        if data["setting_cmd"] == "get_faults": # 获取错误
            if hand_left == True and self.left_hand_joint == "L10" :
                ColorMsg(msg=f"L10左手不能获取错误")
            elif hand_right == True and self.right_hand_joint == "L10" :
                ColorMsg(msg=f"L10右手不能获取错误")
            else:
                hand.get_faults()
        if data["setting_cmd"] == "electric_current": # 获取电流
            if hand_left == True and self.left_hand_joint == "L10" :
                ColorMsg(msg=f"L10左手不能获取电压")
            elif hand_right == True and self.right_hand_joint == "L10" :
                ColorMsg(msg=f"L10右手不能获取电压")
            else:
                hand.get_electric_current()
        if data["setting_cmd"] == "set_electric_current": # 设置电流
            if hand_left == True and self.left_hand_joint == "L10" :
                ColorMsg(msg=f"L10左手不能获取电压")
            elif hand_right == True and self.right_hand_joint == "L10" :
                ColorMsg(msg=f"L10右手不能获取电压")
            else:
                tmp = int(data["params"]["electric_current"])
                e_c = [tmp] * 5
                hand.set_electric_current(e_c=e_c)
        # except:
        #     ColorMsg(msg=f"命令参数错误", color="red")


    def load_yaml(self):
        try:
            settings_yaml_path = package_path + "/config/setting.yaml"
            with open(settings_yaml_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                self.config = config
                self.sdk_version = config["VERSION"]
                self.left_hand_exists = config['LINKER_HAND']['LEFT_HAND']['EXISTS']
                self.left_hand_names = config['LINKER_HAND']['LEFT_HAND']['NAME']
                self.left_hand_joint = config['LINKER_HAND']['LEFT_HAND']['JOINT']
                self.left_hand_force = config['LINKER_HAND']['LEFT_HAND']['TOUCH']
                self.right_hand_exists = config['LINKER_HAND']['RIGHT_HAND']['EXISTS']
                self.right_hand_names = config['LINKER_HAND']['RIGHT_HAND']['NAME']
                self.right_hand_joint = config['LINKER_HAND']['RIGHT_HAND']['JOINT']
                self.right_hand_force = config['LINKER_HAND']['RIGHT_HAND']['TOUCH']
                self.password = config['PASSWORD']
        except Exception as e:
            rospy.logerr(f"Error reading setting.yaml: {e}")
    def open_can0(self):
        try:
            # 检查 can0 接口是否已存在并处于 up 状态
            result = subprocess.run(
                ["ip", "link", "show", "can0"],
                check=True,
                text=True,
                capture_output=True
            )
            if "state UP" in result.stdout:
                rospy.loginfo("CAN接口已经是 UP 状态")
                return
            # 如果没有处于 UP 状态，则配置接口
            subprocess.run(
                ["sudo", "-S", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "1000000"],
                input=f"{self.password}\n",
                check=True,
                text=True,
                capture_output=True
            )
            rospy.loginfo("CAN接口设置成功")
        except subprocess.CalledProcessError as e:
            rospy.logerr(f"CAN接口设置失败: {e.stderr}")
        except Exception as e:
            rospy.logerr(f"发生错误: {str(e)}")

    def is_can_up_sysfs(self, interface="can0"):
    # 检查接口目录是否存在
        if not os.path.exists(f"/sys/class/net/{interface}"):
            return False
        # 读取接口状态
        try:
            with open(f"/sys/class/net/{interface}/operstate", "r") as f:
                state = f.read().strip()
            if state == "up":
                self.can_status = True
            return self.can_status
        except Exception as e:
            print(f"Error reading CAN interface state: {e}")
            return False
        
    def close_can0(self):
        """关闭 can0 接口"""
        try:
            # 检查 can0 接口是否已存在并处于 down 状态
            result = subprocess.run(
                ["ip", "link", "show", "can0"],
                check=True,
                text=True,
                capture_output=True
            )
            if "state DOWN" in result.stdout:
                rospy.loginfo("CAN接口已经是 DOWN 状态")
                return

            # 如果接口处于 UP 状态，则关闭它
            subprocess.run(
                ["sudo", "-S", "ip", "link", "set", "can0", "down"],
                input=f"{self.password}\n",
                check=True,
                text=True,
                capture_output=True
            )
            rospy.loginfo("CAN接口关闭成功")
        except subprocess.CalledProcessError as e:
            rospy.logerr(f"CAN接口关闭失败: {e.stderr}")
        except Exception as e:
            rospy.logerr(f"发生错误: {str(e)}")

    def shutdown(self):
        #self.close_can0()
        pass
    
def signal_handler(sig, frame):
    # 通知其他功能包程序已退出
    m = String()
    d = {
        "close_sdk":True
    }
    m.data = json.dumps(d)
    for i in range(2):
        pub.publish(m)
        time.sleep(0.01)
    sys.exit(0)  # 正常退出程序
if __name__ == '__main__':
    rospy.init_node('linker_hand_sdk', anonymous=True)
    rospy.Rate(60)
    pub = rospy.Publisher('/close_sdk', String, queue_size=10)
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill 命令
    try:
        # 检查can端口如果没有打开则等待重试，一般是usb转can设备没有插上
        while True:
            can = OpenCan()
            can.open_can0()
            time.sleep(0.001)
            o = can.is_can_up_sysfs()
            if o == False:
                ColorMsg(msg=f"can0端口打开失败，3秒后自动重试", color="red")
                time.sleep(3)
            else:
                break
        linker_hand = LinkerHandController()
        rospy.spin()
    except rospy.ROSInterruptException:
        linker_hand.shutdown()
        rospy.loginfo("Node shutdown complete.")
    