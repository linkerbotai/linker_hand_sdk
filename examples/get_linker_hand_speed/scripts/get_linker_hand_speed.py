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

class GetLinkerHandSpeed():
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
       # 五指当前速度 [大拇指, 食指, 中指, 无名指, 小拇指]->[180, 250, 250, 250, 250]
       left_speed = data["right_hand"]["speed"]
       ColorMsg(msg=f"当前左手五指速度为: {left_speed}", color="green")
    
    def right_hand_cb(self, msg):
       data = json.loads(msg.data)
       # 五指当前速度 [大拇指, 食指, 中指, 无名指, 小拇指]->[180, 250, 250, 250, 250]
       right_speed = data["right_hand"]["speed"]
       ColorMsg(msg=f"当前右手五指速度为: {right_speed}", color="green")
       


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
            # 五指当前速度 [大拇指, 食指, 中指, 无名指, 小拇指]->[180, 250, 250, 250, 250]
            left_speed = data["right_hand"]["speed"]
            ColorMsg(msg=f"当前左手五指速度为: {left_speed}", color="green")
        if right_hand != None:
            data = json.loads(right_hand.data)
            # 五指当前速度 [大拇指, 食指, 中指, 无名指, 小拇指]->[180, 250, 250, 250, 250]
            right_speed = data["right_hand"]["speed"]
            ColorMsg(msg=f"当前右手五指速度为: {right_speed}", color="green")
    


if __name__ == '__main__':
    rospy.init_node('get_linker_hand_speed', anonymous=True)
    loop = rospy.get_param('~loop', default=True)  # 默认获取全局参数
    gh = GetLinkerHandSpeed(loop=loop)
    