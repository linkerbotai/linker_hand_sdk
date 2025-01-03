#!/usr/bin/env python

 

import rospy

from std_msgs.msg import String
from sensor_msgs.msg import JointState
import std_msgs.msg

import time

import threading

import signal
import sys

show_count=0
show_count_obj=0
show_step=0
joint_state = JointState()
def send_messages():

    rospy.init_node('dong_test_sender', anonymous=True)

    pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)

    rate = rospy.Rate(30)  # 设置频率为10Hz
    joint_state.header = std_msgs.msg.Header()
    joint_state.header.seq=0
    joint_state.header.stamp = rospy.Time.now() # 或者使用rospy.Time(secs=0, nsecs=0)来获取特定时间
    joint_state.header.frame_id = ''
    # position_values = [250, 250, 250, 250, 250, 250, 128, 128, 128, 128, 250, 0, 0, 0, 0, 250, 250, 250, 250, 250]
    # joint_state.position = position_values
    joint_state.name=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6',

                        'joint7', 'joint8', 'joint9', 'joint10', 'joint11', 'joint12',

                        'joint13', 'joint14', 'joint15', 'joint16', 'joint17', 'joint18',

                        'joint19', 'joint20']
    joint_state.velocity = [0] * len(joint_state.position)  # 与position数组长度相同，全部填充为0
    joint_state.effort = [0] * len(joint_state.position)  # 为每个关节设置努力为零
    pub.publish(joint_state)
    while not rospy.is_shutdown():  # 持续1秒
        position =show_left()
        if(position is not None):
            joint_state.position = position
        # rospy.loginfo(f"Publishing joint states {joint_state.__str__}")
        pub.publish(joint_state)
        rate.sleep()

def show_left():
    global show_count
    global show_count_obj
    global show_step
    show_count= show_count+1
    if(show_count>=show_count_obj):
        show_count=0
        if(show_step==0):
            show_step=show_step+1
            show_count_obj = 50
            return[128, 250, 250, 250, 250, 250, 128, 128, 128, 128, 250, 0, 0, 0, 0, 250, 250, 250, 250, 250]
        elif(show_step==1): #// 伸出食指， 其他三指弯曲，拇指搭在中指上
            show_step=show_step+1
            show_count_obj = 40
            #        1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
            return[190,250,  5,  5,  5,120,128,128,128,120,180,  0,  0,  0,  0,  5,250,  5,  5,  5]
        elif(show_step==2): #// 弯曲中指无名指小拇指远端关节
            show_step=show_step+1
            show_count_obj = 13
            #        1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
            return[190,210,  5,  5,  5,120,  5,128,128,120,180,  0,  0,  0,  0,  5,250,  5,  5,  5]
        elif(show_step==3): #// 舒展中指无名指小拇指远端关节
            show_step=show_step+1
            show_count_obj = 13
            #        1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
            return[190,170,  5,  5,  5,120,128,128,128,120,180,  0,  0,  0,  0,  5,250,  5,  5,  5]
        elif(show_step==4): #// 弯曲中指无名指小拇指远端关节
            show_step=show_step+1
            show_count_obj = 13
            #        1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20
            return[190,210,  5,  5,  5,120,250,128,128,120,180,  0,  0,  0,  0,  5,250,  5,  5,  5]
        elif(show_step==5): #//  舒展中指无名指小拇指远端关节
            show_step=show_step+1
            show_count_obj = 13
            return[190,250,  5,  5,  5,120,128,128,128,120,180,  0,  0,  0,  0,  5,250,  5,  5,  5]
        # elif(show_step==6): #// 先食指回正 防止干涉
        #     show_step=show_step+1
        #     show_count_obj = 2  
        #     return[190, 50,250,250,250,250,80,120,168,250,140,  0,  0,  0,  0,  5,  5,250,250,250]
        # elif(show_step==7): #// 收Y
        #     show_step=show_step+1
        #     show_count_obj = 10
        #     return[100,250,250, 0,  0, 180,128,128,128,128,200, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==8): #// 食指和中指做Y
        #     show_step=show_step+1
        #     show_count_obj = 10
        #     return[100,250,250, 0,  0, 180, 58,200,128,128,200, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==9): #// 收Y
        #     show_step=show_step+1
        #     show_count_obj = 10
        #     return[100,250,250, 0,  0, 180,128,128,128,128,200, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==10): #// 中指和食指弯曲伸直交替两遍
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,100,100, 0,  0, 180,128,128,128,128,200, 0, 0, 0, 0,  0,100,100,  0, 0]
        # elif(show_step==11): #// 中指和食指弯曲伸直交替两遍
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,250, 0,  0, 180,128,128,128,128,200, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==12): #// 中指和食指弯曲伸直交替两遍
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,100,100, 0,  0, 180,128,128,128,128,200, 0, 0, 0, 0,  0,100,100,  0, 0]
        # elif(show_step==13): #// 中指和食指弯曲伸直交替两遍
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,250, 0,  0, 180,128,128,128,128,200, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==14): #// 蜷曲拇指
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return[250,250,250, 0,  0, 150,128,128,128,128,250, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==15): #// 拇指收于掌内
        #     show_step=show_step+1
        #     show_count_obj = 10
        #     return[250,250,250, 0,  0,  5 ,128,128,128,128,250, 0, 0, 0, 0,  0,250,250,  0, 0]
        # elif(show_step==16): #// 收4指
        #     show_step=show_step+1
        #     show_count_obj = 30
        #     return[250,100,100,100,100, 5 ,128,128,128,128,250, 0, 0, 0, 0,  0,10, 10,  10, 10]
        # elif(show_step==17): #// 依次放开4指和拇指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,100,100,100,250, 5 ,128,128,128,128,250, 0, 0, 0, 0,  0,10, 10,  10, 250]
        # elif(show_step==18): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,100,100,250,250, 5 ,128,128,128,128,250, 0, 0, 0, 0,  0,10, 10,  250, 250]
        # elif(show_step==19): #// 2
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,100,250,250,250, 5 ,128,128,128,128,250, 0, 0, 0, 0,  0,10, 250,  250, 250]
        # elif(show_step==20): #// 3
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,250,250,250,250, 5 ,128,128,128,128,250, 0, 0, 0, 0,  0,250, 250,  250, 250]
        # elif(show_step==21): #// 40
        #     show_step=show_step+1
        #     show_count_obj = 10
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==22): #// 并拢拇指
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250,250,250,128,128,128,128, 10, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==23): #// 反转拇指指掌心
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return[  0,250,250,250,250,250,128,128,128,128, 10, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==24): #// 分两步回到初始位置
        #     show_step=show_step+1
        #     show_count_obj = 30
        #     return[  0,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==25): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 50
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==26): #// 2
        #     show_step=show_step+1
        #     show_count_obj = 10
        #     return[250,250,250,250,250,250,200,200,200,200,250, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==27): #// 3
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,250,250,250,250,250, 80, 80, 80, 80,250, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==28): #// 4
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,250, 250,  250, 250]
        # elif(show_step==29): #// 依次蜷曲4小指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return [250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0, 250,  250, 250]
        # elif(show_step==30): #// 蜷曲4指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,  250, 250]
        # elif(show_step==31): #// 4
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0, 250]
        # elif(show_step==32): #// 4
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0,  0]
        # elif(show_step==33): #// 依次蜷曲4小指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,  0,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0,  0]
        # elif(show_step==34): #// 依次蜷曲4小指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,  0,  0,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0,  0]
        # elif(show_step==35): #// 依次蜷曲4小指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,  0,  0,  0,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0,  0]
        # elif(show_step==36): #// 依次蜷曲4小指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[250,  0,  0,  0,  0,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0,  0]
        # elif(show_step==37): #// 蜷曲拇指
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return [  0,  0,  0,  0,  0,250,128,128,128,128,250, 0, 0, 0, 0, 200,  0,  0,   0,  0]
        # elif(show_step==38): #// 打开食指和小指
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return[250,  0,  0,  0,  0,250,128,128,128,128,250, 0, 0, 0, 0, 250,  0,  0,   0,  0]
        # elif(show_step==39): #// 打开食指和小指
        #     show_step=show_step+1
        #     show_count_obj = 30
        #     return[250,250,  0,  0,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,250,  0,   0,250]
        # elif(show_step==40): #// 将拇指搭上666
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return[100,250,  0,  0,250,200,128,128,128,128,100, 0, 0, 0, 0,100,250,  0,   0,250]
        # elif(show_step==41): #// 左右动手指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,  0,  0,250,200, 80,128,128,200,100, 0, 0, 0, 0,100,250,  0,   0,250]
        # elif(show_step==42): #// 左右动手指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,  0,  0,250,200,200,128,128, 80,100, 0, 0, 0, 0,100,250,  0,   0,250]
        # elif(show_step==43): #// 左右动手指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,  0,  0,250,200, 80,128,128,200,100, 0, 0, 0, 0,100,250,  0,   0,250]
        # elif(show_step==44): #// 左右动手指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,  0,  0,250,200,200,128,128, 80,100, 0, 0, 0, 0,100,250,  0,   0,250]
        # elif(show_step==45): #// 左右动手指
        #     show_step=show_step+1
        #     show_count_obj = 15
        #     return[100,250,  0,  0,250,200,128,128,128,128,100, 0, 0, 0, 0,100,250,  0,   0,250]
        # elif(show_step==46): #//  展开
        #     show_step=show_step+1
        #     show_count_obj = 50
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==47): #// 拇指和食指捏
        #     show_step=show_step+1
        #     show_count_obj = 50
        #     return[ 55, 0,250,250,250,170,128,128,128,128,70, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==48): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250, 20,250,250,220,128,128,128,128,100, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==49): #// 拇指和中指捏
        #     show_step=show_step+1
        #     show_count_obj = 35
        #     return[ 55,250, 0,250,250,140,128,128,128,128,60, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==50): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250, 20,250,170,128,128,128,128,100, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==51): #// 拇指和无名指捏
        #     show_step=show_step+1
        #     show_count_obj = 35
        #     return[ 55,250,250, 0 ,250,110,128,128,128,128,50, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==52): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250, 20,130,128,128,128,128,100, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==53): #// 拇指和小指捏
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return[ 55,250,250,250,  0, 60,128,128,128,128,50, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==54): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250, 20,130,128,128,128,128,100, 0, 0, 0, 0,250,250,250, 250,250]
        # elif(show_step==55): #// 拇指和小指掐
        #     show_step=show_step+1
        #     show_count_obj = 40
        #     return[160,250,250,250,160, 60,128,128,128,128,50, 0, 0, 0, 0,100,250,250, 250, 80]
        # elif(show_step==56): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250,250,130,128,128,128,128,100, 0, 0, 0, 0,250,250,250,  50, 250]
        # elif(show_step==57): #// 拇指和无名指掐
        #     show_step=show_step+1
        #     show_count_obj = 35
        #     return[160,250,250,150,250,100,128,128,128,128,50, 0, 0, 0, 0,100,250,250, 80, 250]
        # elif(show_step==58): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250,250,180,128,128,128,128,100, 0, 0, 0, 0, 250,250, 50,  250, 250]
        # elif(show_step==59): #// 拇指和中指掐
        #     show_step=show_step+1
        #     show_count_obj = 35
        #     return[160,250,150,250,250,135,128,128,128,128,70, 0, 0, 0, 0,100,250,85, 250, 250]
        # elif(show_step==60): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 20
        #     return[250,250,250,250,250,220,128,128,128,128,100, 0, 0, 0, 0, 250, 50,250,  250, 250]
        # elif(show_step==61): #// 拇指和食指掐
        #     show_step=show_step+1
        #     show_count_obj = 35
        #     return[165,150,250,250,250,170,128,128,128,128,70, 0, 0, 0, 0,100,80,250, 250, 250]
        # elif(show_step==62): #// 1
        #     show_step=show_step+1
        #     show_count_obj = 60
        #     return[250,250,250,250,250,250,128,128,128,128,250, 0, 0, 0, 0, 250,250,250,  250, 250]
        else:
            show_step=1

def signal_handler(sig, frame):

    print('You pressed Ctrl+C!')

    sys.exit(0)  # 0表示正常退出
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':

    try:
        print("测试中")
        send_messages()
    except KeyboardInterrupt:
         print("Caught KeyboardInterrupt, exiting gracefully.")
    except rospy.ROSInterruptException:
        print("ROSInterruptException")
    finally:
         print("Cleaning up...")