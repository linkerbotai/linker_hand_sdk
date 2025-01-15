import rospy,rospkg
import time,os,sys
from std_msgs.msg import String,Header, Float32MultiArray
from sensor_msgs.msg import JointState

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.color_msg import ColorMsg


'''
/cb_left_hand_force # 左手力传感器
/cb_right_hand_force # 右手力传感器

'''

class GetLinkerHandPressure():
    def __init__(self,loop=False):
        self.loop = loop
        if self.loop == True:
            self.loop_acquisition()
            rospy.spin()
        else:
            self.single_acquisition()
    
    def loop_acquisition(self):
        rospy.Subscriber("/cb_left_hand_force",Float32MultiArray,self.left_hand_cb,queue_size=1)
        rospy.Subscriber("/cb_right_hand_force", Float32MultiArray, self.right_hand_cb, queue_size=1)
    def left_hand_cb(self,msg):
        data = self.list_slice(data=msg.data)
        # 五指法相力 数值越大法向力值越大
        # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 26.0, 34.0, 255.0, 0.0]
        hand_normal_force = data[0]
        ColorMsg(msg=f"左手五指法相力: {list(hand_normal_force)}", color="green")
        # 五指切向力 数值越大切向力值越大
        # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 12.0, 3.0, 4.0, 0.0]
        hand_tangential_force = data[1]
        ColorMsg(msg=f"左手五指切向力: {list(hand_tangential_force)}", color="green")
        # 五指切向力方向 数值0-127对应实际切向力角度0-359，注意在手指不受力即无法判断切向力方向时数值保持为255。
        hand_tangential_force_dir = data[2]
        ColorMsg(msg=f"左手五指切向力方向: {list(hand_tangential_force_dir)}", color="green")
        # 五指接近感应
        hand_approach_inc = data[3]
        ColorMsg(msg=f"左手五指接近感应: {list(hand_approach_inc)}", color="green")
    
    def right_hand_cb(self, msg):
        data = self.list_slice(data=msg.data)
        # 五指法相力 数值越大法向力值越大
        # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 26.0, 34.0, 255.0, 0.0]
        hand_normal_force = data[0]
        ColorMsg(msg=f"右手五指法相力: {list(hand_normal_force)}", color="green")
        # 五指切向力 数值越大切向力值越大
        # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 12.0, 3.0, 4.0, 0.0]
        hand_tangential_force = data[1]
        ColorMsg(msg=f"右手五指切向力: {list(hand_tangential_force)}", color="green")
        # 五指切向力方向 数值0-127对应实际切向力角度0-359，注意在手指不受力即无法判断切向力方向时数值保持为255。
        hand_tangential_force_dir = data[2]
        ColorMsg(msg=f"右手五指切向力方向: {list(hand_tangential_force_dir)}", color="green")
        # 五指接近感应
        hand_approach_inc = data[3]
        ColorMsg(msg=f"右手五指接近感应: {list(hand_approach_inc)}", color="green")


    def single_acquisition(self):
        left_hand = None
        right_hand = None
        try:
            left_hand = rospy.wait_for_message("/cb_left_hand_force",Float32MultiArray,timeout=0.1)
        except:
            ColorMsg(msg="左手没有数据", color="yellow")
        try:
            right_hand = rospy.wait_for_message("/cb_right_hand_force",Float32MultiArray,timeout=0.1)
        except:
            ColorMsg(msg="右手没有数据", color="yellow")
        if left_hand != None:
            data = self.list_slice(data=left_hand.data)
            # 五指法相力 数值越大法向力值越大
            # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 26.0, 34.0, 255.0, 0.0]
            left_hand_normal_force = data[0]
            ColorMsg(msg=f"左手五指法相力: {list(left_hand_normal_force)}", color="green")
            # 五指切向力 数值越大切向力值越大
            # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 12.0, 3.0, 4.0, 0.0]
            left_hand_tangential_force = data[1]
            ColorMsg(msg=f"左手五指切向力: {list(left_hand_tangential_force)}", color="green")
            # 五指切向力方向 数值0-127对应实际切向力角度0-359，注意在手指不受力即无法判断切向力方向时数值保持为255。
            left_hand_tangential_force_dir = data[2]
            ColorMsg(msg=f"左手五指切向力方向: {list(left_hand_tangential_force_dir)}", color="green")
            # 五指接近感应
            left_hand_approach_inc = data[3]
            ColorMsg(msg=f"左手五指接近感应: {list(left_hand_approach_inc)}", color="green")
        if right_hand != None:
            data = self.list_slice(data=right_hand.data)
            # 五指法相力 数值越大法向力值越大
            # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 26.0, 34.0, 255.0, 0.0]
            right_hand_normal_force = data[0]
            ColorMsg(msg=f"右手五指法相力: {list(right_hand_normal_force)}", color="green")
            # 五指切向力 数值越大切向力值越大
            # [大拇指, 食指, 中指, 无名指, 小拇指]->[0.0, 12.0, 3.0, 4.0, 0.0]
            right_hand_tangential_force = data[1]
            ColorMsg(msg=f"右手五指切向力: {list(right_hand_tangential_force)}", color="green")
            # 五指切向力方向 数值0-127对应实际切向力角度0-359，注意在手指不受力即无法判断切向力方向时数值保持为255。
            right_hand_tangential_force_dir = data[2]
            ColorMsg(msg=f"右手五指切向力方向: {list(right_hand_tangential_force_dir)}", color="green")
            # 五指接近感应
            right_hand_approach_inc = data[3]
            ColorMsg(msg=f"右手五指接近感应: {list(right_hand_approach_inc)}", color="green")
    
    def list_slice(self,data,n=5):
        n = 5  # 每个子列表的长度
        result = [data[i:i + n] for i in range(0, len(data), n)]
        return result

if __name__ == '__main__':
    rospy.init_node('get_linker_hand_force', anonymous=True)
    loop = rospy.get_param('~loop', default=True)  # 默认获取全局参数
    gh = GetLinkerHandPressure(loop=loop)
    