#!/usr/bin/env python
#本demo为适配蜗轮蜗杆版本L10灵巧手，默认支持左手，如需支持右手，请将cb_left_hand_control_cmd 改为cb_right_hand_control_cmd
 

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
hand = {"joint1":255,   #拇指根部弯曲
        "joint2":128,   #拇指侧摆
        "joint3":255,   #食指根部弯曲  
        "joint4":255,   #中指根部弯曲
        "joint5":255,   #无名指根部弯曲
        "joint6":255,   #小指根部弯曲
        "joint7":128,   #食指侧摆
        "joint8":128,   #中指侧摆
        "joint9":128,   #无名指侧摆
        "joint10":255,  #拇指旋转
        }

def send_messages():

    rospy.init_node('dong_test_sender', anonymous=True) 

    pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)

    rate = rospy.Rate(30)  # 设置频率为30Hz
    joint_state.header = std_msgs.msg.Header()
    joint_state.header.seq=0
    joint_state.header.stamp = rospy.Time.now() # 或者使用rospy.Time(secs=0, nsecs=0)来获取特定时间
    joint_state.header.frame_id = ''
    joint_state.name=list(hand.keys())
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
    global show_count #当前步骤已等待时长
    global show_count_obj  #当前步骤动作应等待时长
    global show_step  #执行步骤号
    global hand
    show_count= show_count+1
    if(show_count>=show_count_obj):
        show_count=0
        if(show_step==0):
            show_step=show_step+1
            show_count_obj = 100
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint3'] = 250
            hand['joint4'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 250
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==1): #// 收小指与无名指
            show_step=show_step+1
            show_count_obj = 10
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint5'] = 0
            hand['joint6'] = 0
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==2): #// 将拇指搭到小指与无名指上面
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 40
            hand['joint2'] = 240
            hand['joint10'] = 80
            return list(hand.values())
        elif(show_step==3): #// 食指和中指向一侧倾斜
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 200
            return list(hand.values())
        elif(show_step==4): #// 另一侧
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 50
            return list(hand.values())
        elif(show_step==5): #//  两支回中
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 128
            return list(hand.values())
        elif(show_step==6): #// 食指和中指做Y
            show_step=show_step+1
            show_count_obj = 2  
            hand['joint7'] = 50
            return list(hand.values())
        elif(show_step==7): #// 收Y
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 128
            return list(hand.values())
        elif(show_step==8): #// 食指和中指做Y
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 50
            return list(hand.values())
        elif(show_step==9): #// 收Y
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 128
            return list(hand.values())
        elif(show_step==10): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 100
            hand['joint4'] = 100
            return list(hand.values())
        elif(show_step==11): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 250
            hand['joint4'] = 250
            return list(hand.values())
        elif(show_step==12): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 100
            hand['joint4'] = 100
            return list(hand.values())
        elif(show_step==13): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint3'] = 250
            hand['joint4'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 250
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==14): #// 蜷曲拇指
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 0
            hand['joint2'] = 240
            hand['joint10'] = 80
            return list(hand.values())
        elif(show_step==15): #// 拇指收于掌内
            show_step=show_step+1
            return list(hand.values())
        elif(show_step==16): #// 收4指
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 0
            hand['joint2'] = 255
            hand['joint3'] = 43
            hand['joint4'] = 38
            hand['joint5'] = 46
            hand['joint6'] = 37
            hand['joint7'] = 255
            hand['joint8'] = 255
            hand['joint9'] = 255
            hand['joint10'] = 0
            return list(hand.values())
        elif(show_step==17): #// 依次放开4指和拇指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint6'] = 250
            return list(hand.values())
        elif(show_step==18): #// 1
            show_step=show_step+1
            show_count_obj = 15
            hand['joint5'] = 250
            return list(hand.values())
        elif(show_step==19): #// 2
            show_step=show_step+1
            show_count_obj = 15
            hand['joint4'] = 250
            return list(hand.values())
        elif(show_step==20): #// 3
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 250
            return list(hand.values())
        elif(show_step==21): #// 40
            show_step=show_step+1
            show_count_obj = 20
            hand['joint1'] = 250
            hand['joint2'] = 110
            hand['joint10'] = 240
            return list(hand.values())
        elif(show_step==22): #// 并拢拇指
            show_step=show_step+1
            show_count_obj = 20
            hand['joint1'] = 250
            hand['joint2'] = 10
            hand['joint10'] = 110
            return list(hand.values())
        elif(show_step==23): #// 反转拇指指掌心
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 0
            hand['joint2'] = 10
            hand['joint10'] = 110
            return list(hand.values())
        elif(show_step==24): #// 分两步回到初始位置
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 0
            hand['joint2'] = 240
            hand['joint10'] = 110
            return list(hand.values())
        elif(show_step==25): #// 1
            show_step=show_step+1
            show_count_obj = 50
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint10'] = 110
            return list(hand.values())
        elif(show_step==26): #// 2
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 200
            hand['joint8'] = 200
            hand['joint9'] = 200
            return list(hand.values())
        elif(show_step==27): #// 3
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 80
            hand['joint8'] = 80
            hand['joint9'] = 80
            return list(hand.values())
        elif(show_step==28): #// 4
            show_step=show_step+1
            show_count_obj = 20
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            return list(hand.values())
        elif(show_step==29): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==30): #// 蜷曲4指
            show_step=show_step+1
            return list(hand.values())
        elif(show_step==31): #// 4
            show_step=show_step+1
            return list(hand.values())
        elif(show_step==32): #// 4
            show_step=show_step+1
            return list(hand.values())
        elif(show_step==33): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 0
            hand['joint4'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 250
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==34): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint4'] = 0
            return list(hand.values())
        elif(show_step==35): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint5'] = 0
            return list(hand.values())
        elif(show_step==36): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint6'] = 0
            return list(hand.values())
        elif(show_step==37): #// 蜷曲拇指
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 0
            return list(hand.values())
        elif(show_step==38): #// 打开食指和小指
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 250
            hand['joint2'] = 230
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==39): #// 打开食指和小指
            show_step=show_step+1
            show_count_obj = 30
            hand['joint3'] = 250
            hand['joint6'] = 250
            return list(hand.values())
        elif(show_step==40): #// 将拇指搭上666
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 0
            hand['joint2'] = 100
            hand['joint10'] = 160
            return list(hand.values())
        elif(show_step==41): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 80
            hand['joint9'] = 200
            return list(hand.values())
        elif(show_step==42): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 200
            hand['joint9'] = 80
            return list(hand.values())
        elif(show_step==43): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 80
            hand['joint9'] = 200
            return list(hand.values())
        elif(show_step==44): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 200
            hand['joint9'] = 80
            return list(hand.values())
        elif(show_step==45): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 128
            hand['joint9'] = 128
            return list(hand.values())
        elif(show_step==46): #//  展开
            show_step=show_step+1
            show_count_obj = 50
            hand['joint1'] = 250
            hand['joint2'] = 180
            hand['joint3'] = 250
            hand['joint4'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 250
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==47): #// 拇指和食指捏
            show_step=show_step+1
            show_count_obj = 80
            hand['joint1'] = 40
            hand['joint2'] = 0
            hand['joint3'] = 105
            hand['joint4'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 250
            hand['joint10'] = 250
            return list(hand.values())
        elif(show_step==48): #// 1
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 250
            hand['joint3'] = 250
            return list(hand.values())
        elif(show_step==49): #// 拇指和中指捏
            show_step=show_step+1
            show_count_obj = 45
            hand['joint1'] = 25
            hand['joint4'] = 99
            hand['joint10'] = 188
            return list(hand.values())
        elif(show_step==50): #// 1
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 250
            hand['joint4'] = 250
            return list(hand.values())
        elif(show_step==51): #// 拇指和无名指捏
            show_step=show_step+1
            show_count_obj = 45
            hand['joint1'] = 35
            hand['joint5'] = 103
            hand['joint10'] = 132
            return list(hand.values())
        elif(show_step==52): #// 1
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 250
            hand['joint5'] = 250
            return list(hand.values())
        elif(show_step==53): #// 拇指和小指捏
            show_step=show_step+1
            show_count_obj = 45
            hand['joint1'] = 30
            hand['joint6'] = 92
            hand['joint10'] = 81
            return list(hand.values())
        elif(show_step==54): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint1'] = 250
            hand['joint2'] = 250
            hand['joint3'] = 250
            hand['joint4'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 250
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            hand['joint10'] = 250
            return list(hand.values())


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