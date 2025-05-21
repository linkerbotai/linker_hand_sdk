import rospy
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import std_msgs.msg
import time
import numpy as np  # 用于处理数组
joint_state = JointState() 
hand = {"joint1":55,
        "joint2":250,   #0
        "joint3":250,
        "joint4":250,
        "joint5":250,
        "joint6":170,
        "joint7":128,
        "joint8":128,
        "joint9":128,
        "joint10":128,
        "joint11":70,
        "joint12":0,
        "joint13":0,
        "joint14":0,
        "joint15":0,
        "joint16":250,
        "joint17":250,
        "joint18":250,
        "joint19":250,
        "joint20":250,
        }
hand_real_time =list(hand.values())
hand_data_holder= None
touched_flag = False
is_first_touch = True
class LIPDController:
    def __init__(self, mode_, kp_, ki_, kd_, forcetarget_, tolerance_):
        self.mode = mode_
        self.kp = kp_ #// 比例增益
        self.ki = ki_ #// 微分增益
        self.kd = kd_ #// 泄露因子
        self.ft = forcetarget_ #// 目标值
        self.tr = tolerance_ #// 误差范围
        self.pre_error = 0 #// 前一个误差
        self.yout = 0 #// 控制器输出
        self.fb = 0 #// 力反馈
        self.appro = 0 # 接近值
        self.error = 0
        self.sum = 0
        self.state = 0
        self.FAST_STEP = 1.5  #10
        self.SLOW_STEP = 0.1  #1
 
    def update(self, cap, fb):
        self.fb = fb
        self.appro = cap
        
        if self.mode == 0:  # 接近模式
            self.error = self.fb - self.ft
            if(self.state==0):
                if self.fb >= 0.01:
                    self.state = 1
                elif 1< self.appro <= 10:
                    self.yout = self.SLOW_STEP
                elif 10 < self.appro < 256:
                    # self.yout = self.SLOW_STEP
                    self.yout = self.FAST_STEP - (self.appro - 20) / (250 - 20) * (self.FAST_STEP - self.SLOW_STEP)
                else:
                     self.yout=self.FAST_STEP
            elif(self.state==1):
                if(self.fb<=0):
                    print(f"物品移动走了，继续抓握")
                    self.state=0
                    self.yout=0
                else:
                    self.PID()
            else:
                self.yout=0
        
        elif self.mode == 1:  # 另一种接近模式
            self.error = (self.appro - self.ft) / 1000
            if self.appro < 250:
                self.yout = self.FAST_STEP / 2
            elif 250 <= self.appro <= 254:
                self.yout = self.SLOW_STEP
            else:
                self.PID()
        
        elif self.mode == 2:  # 接触模式
            self.error = self.fb - self.ft
            if self.fb <= 0.01:
                self.yout = self.SLOW_STEP
            else:
                self.PID()
        
        else:
            self.yout = 0
        
        # 打印调试信息
        # print(f"sum: {self.sum}==== yout: {self.yout}")
        return self.yout
    
    def PID(self):
        if self.fb < self.ft + self.tr and self.fb > self.ft - self.tr:
            self.yout = 0
        else:
            self.sum += self.error
            self.sum = max(-10, min(self.sum, 10))
            self.yout = self.kp * self.error + self.kd * (self.error - self.pre_error) + self.ki * self.sum
            self.yout = -self.yout
            self.yout /= 80  # 调整输出值
        self.pre_error = self.error
 

# 初始化LIPD控制器
lipd_controller = LIPDController(0, 0.5, 0.001, 0.1, 0.35, 0.005)

def lip_callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "lip back I heard appro:%s   fb:%s", data.data[16],data.data[1])
    hand_touch_data = data.data
    global lipd_controller
    global hand
    global touched_flag
    global is_first_touch
    global hand_real_time
    global joint_state
    global pub
    appro=hand_touch_data[16]
    fb = hand_touch_data[1]
    yout = lipd_controller.update(appro,fb)
    joint = hand["joint2"]

    if(yout<1.5 and yout >-1.5):
        # yout=0
        hand["joint2"]=hand["joint2"]-yout
        handtemp = hand["joint2"]
        if(handtemp>255):
            hand["joint2"]= 255
        elif(handtemp<0):
            hand["joint2"]=0
        joint_state.position=list(hand.values())
        pub.publish(joint_state)
    elif(yout>1.5):
        yout=1.5
        hand["joint2"]=hand["joint2"]-yout
        handtemp = hand["joint2"]
        if(handtemp>255):
            hand["joint2"]= 255
        elif(handtemp<0):
            hand["joint2"]=0
        joint_state.position=list(hand.values())
        pub.publish(joint_state)
    elif(yout<-1.5):
        yout=-1.5
        hand["joint2"]=hand["joint2"]-yout
        handtemp = hand["joint2"]
        if(handtemp>255):
            hand["joint2"]= 255
        elif(handtemp<0):
            hand["joint2"]=0
        joint_state.position=list(hand.values())
        pub.publish(joint_state)
    elif(yout==0 and is_first_touch == True):
        joint_state.position=hand_real_time
        pub.publish(joint_state)
        is_first_touch=False
    else:
        if(is_first_touch):
            hand["joint2"]=hand["joint2"]-yout
            handtemp = hand["joint2"]
            if(handtemp>255):
                hand["joint2"]= 255
            elif(handtemp<0):
                hand["joint2"]=0
            joint_state.position=list(hand.values())
            pub.publish(joint_state)

def hand_status(data):
    # rospy.loginfo(rospy.get_caller_id() + "hand status I heard %s", data.position)
    global hand_real_time
    hand_real_time[1]=data.position[1]

 # 初始化ROS节点
rospy.init_node('grasp_force_control', anonymous=True)
pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)
sub = rospy.Subscriber('/cb_left_hand_touch', Float32MultiArray, lip_callback)
hand_sub = rospy.Subscriber('/cb_left_hand_state', JointState, hand_status)  



# 初始化ROS节点
def main():
    global joint_state
    global pub
    global hand
    global sub
    rate = rospy.Rate(100)  # 100 Hz
    joint_state.header = std_msgs.msg.Header()
    joint_state.header.seq=0
    joint_state.header.stamp = rospy.Time.now() 
    joint_state.header.frame_id = ''
    joint_state.name=list(hand.keys())
    joint_state.velocity = [0] * len(joint_state.position)  
    joint_state.effort = [0] * len(joint_state.position)  
    joint_state.position = list(hand.values())
    print("开始演示")
    rospy.sleep(1)
    pub.publish(joint_state)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
   
    except KeyboardInterrupt:
         print("Caught KeyboardInterrupt, exiting gracefully.")
    except rospy.ROSInterruptException:
        print("ROSInterruptException")
    finally:
         print("Cleaning up...")
 
