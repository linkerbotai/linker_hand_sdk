#!/usr/bin/env python3
import rospy,rospkg
import time,os,sys,json
from std_msgs.msg import String,Header, Float32MultiArray
from sensor_msgs.msg import JointState

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.color_msg import ColorMsg


'''
/cb_left_hand_info # 左手topic
/cb_right_hand_info # 右手topic

'''

class GetLinkerHandFault():
    def __init__(self,loop=False):
        self.loop = loop
        if self.loop == True:
            self.loop_acquisition()
            rospy.spin()
        else:
            self.single_acquisition()
    
    def loop_acquisition(self):
        rospy.Subscriber("/cb_left_hand_info",String,self.left_hand_cb,queue_size=1)
        rospy.Subscriber("/cb_right_hand_info", String, self.right_hand_cb, queue_size=1)
    def left_hand_cb(self,msg):
        data = json.loads(msg.data)
        # 五指当前错误代码 [大拇指, 食指, 中指, 无名指, 小拇指]->[0, 16, 0, 16, 0]
        left_fault = data["right_hand"]["fault"]
        tmp = []
        for index,item in enumerate(left_fault):
            a = self.get_active_bits(item)
            if len(a) > 0:
                tmp.append(a[0])
            else:
                tmp.append(0)
        ColorMsg(msg=f"当前左手五指错误代码为: {tmp}", color="green")
    
    def right_hand_cb(self, msg):
        data = json.loads(msg.data)
       # 五指当前错误代码 [大拇指, 食指, 中指, 无名指, 小拇指]->[0, 16, 0, 16, 0]
        right_fault = data["right_hand"]["fault"]
        tmp = []
        for index,item in enumerate(right_fault):
            a = self.get_active_bits(item)
            if len(a) > 0:
                tmp.append(a[0])
            else:
                tmp.append(0)
        ColorMsg(msg=f"当前右手五指错误代码为: {tmp}", color="green")
       


    def single_acquisition(self):
        left_hand = None
        right_hand = None
        try:
            left_hand = rospy.wait_for_message("/cb_left_hand_info",String,timeout=0.1)
        except:
            ColorMsg(msg="左手没有数据", color="yellow")
        try:
            right_hand = rospy.wait_for_message("/cb_right_hand_info",String,timeout=0.1)
        except:
            ColorMsg(msg="右手没有数据", color="yellow")
        if left_hand != None:
            data = json.loads(left_hand.data)
            # 五指当前错误代码 [大拇指, 食指, 中指, 无名指, 小拇指]->[0, 16, 0, 16, 0]
            left_fault = data["right_hand"]["fault"]
            ColorMsg(msg=f"当前左手五指错误代码为: {left_fault}", color="green")
        if right_hand != None:
            data = json.loads(right_hand.data)
            # 五指当前错误代码 [大拇指, 食指, 中指, 无名指, 小拇指]->[0, 16, 0, 16, 0]
            right_fault = data["right_hand"]["fault"]
            ColorMsg(msg=f"当前右手五指错误代码为: {right_fault}", color="green")
    
    def decimal_to_bits(self,decimal_value, bit_length=8):
        """
        将十进制数转换为固定长度的二进制位列表。
        """
        return [int(x) for x in f"{decimal_value:0{bit_length}b}"][::-1]

    def get_active_bits(self,decimal_value, bit_length=8):
        """
        获取十进制数对应二进制位中所有激活的位（值为1的位索引）。

        :param decimal_value: int, 十进制输入数。
        :param bit_length: int, 二进制长度，默认为8。
        :return: list, 激活的位索引。
        """
        # 调用 decimal_to_bits 转换十进制为二进制位列表
        bit_list = self.decimal_to_bits(decimal_value, bit_length)
        # 遍历列表，找到所有值为1的位置
        return [i for i, bit in enumerate(bit_list) if bit == 1]

if __name__ == '__main__':
    rospy.init_node('get_linker_hand_fault', anonymous=True)
    loop = rospy.get_param('~loop', default=True)  # 默认获取全局参数
    gh = GetLinkerHandFault(loop=loop)
    