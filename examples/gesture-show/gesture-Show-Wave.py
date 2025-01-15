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

    rate = rospy.Rate(30)  # 设置频率为30Hz
    joint_state.header = std_msgs.msg.Header()
    joint_state.header.seq=0
    joint_state.header.stamp = rospy.Time.now() 
    joint_state.header.frame_id = ''
    joint_state.name=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6',

                        'joint7', 'joint8', 'joint9', 'joint10', 'joint11', 'joint12',

                        'joint13', 'joint14', 'joint15', 'joint16', 'joint17', 'joint18',

                        'joint19', 'joint20']
    joint_state.velocity = [0] * len(joint_state.position)  # 与position数组长度相同，全部填充为0
    joint_state.effort = [0] * len(joint_state.position)  
    pub.publish(joint_state)
    while not rospy.is_shutdown():  # 持续1秒
        position =show_left()
        if(position is not None):
            joint_state.position = position
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
            show_count_obj = 40
            return[128, 250, 250, 250, 250, 250, 128, 128, 128, 128, 250, 0, 0, 0, 0, 250, 250, 250, 250, 250]
        elif(show_step==1): #// 弯曲四指小节
            show_step=show_step+1
            show_count_obj = 30
            return[128,250,250,250,250,250,128,128,128,128,250,  0,  0,  0,  0,250,  0,  0,  0,  0]
        elif(show_step==2): #// 弯曲四指小节和大节
            show_step=show_step+1
            show_count_obj = 33
            return[128,  0,  0,  0,  0,250,128,128,128,128,250,  0,  0,  0,  0,250,  0,  0,  0,  0]
        elif(show_step==3): #// 舒展四指小节 弯曲大节
            show_step=show_step+1
            show_count_obj = 30
            return[128,  0,  0,  0,  0,250,128,128,128,128,250,  0,  0,  0,  0,250,250,250,250,250]
        elif(show_step==4): #// 全部舒展 回归初始位置
            show_step=show_step+1
            show_count_obj = 30
            return[128,250,250,250,250,250,128,128,128,128,250,  0,  0,  0,  0,250,250,250,250,250]
        else:
            show_step=0

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