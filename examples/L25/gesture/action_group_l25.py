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
hand = {"joint1":250,
        "joint2":250, 
        "joint3":250,
        "joint4":250,
        "joint5":250,
        "joint6":250,
        "joint7":250,
        "joint8":250,
        "joint9":250,
        "joint10":250,
        "joint11":250,
        "joint12":0,
        "joint13":0,
        "joint14":0,
        "joint15":0,
        "joint16":250,
        "joint17":250,
        "joint18":250,
        "joint19":250,
        "joint20":250,
        "joint21":250,
        "joint22":250,
        "joint23":250,
        "joint24":250,
        "joint25":250,
        }

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
    global show_count
    global show_count_obj
    global show_step
    global hand
    show_count= show_count+1
    if(show_count>=show_count_obj):
        show_count=0
        if(show_step==0): #张开手掌
            show_step=show_step+1
            show_count_obj = 50
            hand['joint1'] = 75
            hand['joint2'] = 255
            hand['joint3'] = 255
            hand['joint4'] = 255
            hand['joint5'] = 255
            hand['joint6'] = 176
            hand['joint7'] = 51
            hand['joint8'] = 51
            hand['joint9'] = 125
            hand['joint10'] = 202
            hand['joint11'] = 202
            hand['joint12'] = 255
            hand['joint13'] = 255
            hand['joint14'] = 255
            hand['joint15'] = 255
            hand['joint16'] = 255
            hand['joint17'] = 255
            hand['joint18'] = 255
            hand['joint19'] = 255
            hand['joint20'] = 255
            hand['joint21'] = 255
            hand['joint22'] = 255
            hand['joint23'] = 255
            hand['joint24'] = 255
            hand['joint25'] = 255
            return list(hand.values())
        elif(show_step==1): #// 收小指与无名指
            show_step=show_step+1
            show_count_obj = 10
            hand['joint4'] = 0
            hand['joint5'] = 0
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            hand['joint10'] = 128
            hand['joint11'] = 250
            hand['joint16'] = 250
            hand['joint17'] = 250
            hand['joint18'] = 250
            hand['joint19'] = 0
            hand['joint20'] = 0
            hand['joint21'] = 250
            hand['joint22'] = 250
            hand['joint23'] = 250
            hand['joint24'] = 0
            hand['joint25'] = 0
            return list(hand.values())
        elif(show_step==2): #// 将拇指搭到小指与无名指上面
            show_step=show_step+1
            show_count_obj = 30
            hand['joint1'] = 100
            hand['joint6'] = 180
            hand['joint16'] = 0
            hand['joint21'] = 0
            return list(hand.values())
        elif(show_step==3): #// 食指和中指向一侧倾斜
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 200
            hand['joint8'] = 200
            hand['joint11'] = 200
            return list(hand.values())
        elif(show_step==4): #// 另一侧
            show_step=show_step+1
            show_count_obj = 13
            hand['joint7'] = 50
            hand['joint8'] = 50
            return list(hand.values())
        elif(show_step==5): #//  两支回中
            show_step=show_step+1
            show_count_obj = 13
            hand['joint7'] = 128
            hand['joint8'] = 128
            return list(hand.values())
        elif(show_step==6): #// 食指和中指做Y
            show_step=show_step+1
            show_count_obj = 2  
            hand['joint7'] = 50
            hand['joint8'] = 200
            return list(hand.values())
        elif(show_step==7): #// 收Y
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 128
            hand['joint8'] = 128
            return list(hand.values())
        elif(show_step==8): #// 食指和中指做Y
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 50
            hand['joint8'] = 200
            return list(hand.values())
        elif(show_step==9): #// 收Y
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 128
            hand['joint8'] = 128
            return list(hand.values())
        elif(show_step==10): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint2'] = 100
            hand['joint3'] = 100
            hand['joint17'] = 100
            hand['joint18'] = 100
            hand['joint22'] = 100
            hand['joint23'] = 100
            return list(hand.values())
        elif(show_step==11): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint2'] = 250
            hand['joint3'] = 250
            hand['joint17'] = 250
            hand['joint18'] = 250
            hand['joint22'] = 250
            hand['joint23'] = 250
            return list(hand.values())
        elif(show_step==12): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint2'] = 100
            hand['joint3'] = 100
            hand['joint17'] = 100
            hand['joint18'] = 100
            hand['joint22'] = 100
            hand['joint23'] = 100
            return list(hand.values())
        elif(show_step==13): #// 中指和食指弯曲伸直交替两遍
            show_step=show_step+1
            show_count_obj = 15
            hand['joint2'] = 250
            hand['joint3'] = 250
            hand['joint17'] = 250
            hand['joint18'] = 250
            hand['joint22'] = 250
            hand['joint23'] = 250
            return list(hand.values())
        elif(show_step==14): #// 蜷曲拇指
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 250
            hand['joint6'] = 150
            hand['joint11'] = 250
            hand['joint23'] = 250
            return list(hand.values())
        elif(show_step==15): #// 拇指收于掌内
            show_step=show_step+1
            show_count_obj = 10
            hand['joint6'] = 5
            return list(hand.values())
        elif(show_step==16): #// 收4指
            show_step=show_step+1
            show_count_obj = 30
            hand['joint2'] = 100
            hand['joint3'] = 100
            hand['joint4'] = 100
            hand['joint5'] = 100
            hand['joint17'] = 100
            hand['joint18'] = 100
            hand['joint19'] = 100
            hand['joint20'] = 100
            hand['joint22'] = 100
            hand['joint23'] = 100
            hand['joint24'] = 100
            hand['joint25'] = 100
            return list(hand.values())
        elif(show_step==17): #// 依次放开4指和拇指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint5'] = 250
            hand['joint20'] = 250
            hand['joint25'] = 250
            return list(hand.values())
        elif(show_step==18): #// 1
            show_step=show_step+1
            show_count_obj = 15
            hand['joint4'] = 250
            hand['joint19'] = 250
            hand['joint24'] = 250
            return list(hand.values())
        elif(show_step==19): #// 2
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 250
            hand['joint18'] = 250
            hand['joint23'] = 250
            return list(hand.values())
        elif(show_step==20): #// 3
            show_step=show_step+1
            show_count_obj = 15
            hand['joint2'] = 250
            hand['joint17'] = 250
            hand['joint22'] = 250
            return list(hand.values())
        elif(show_step==21): #// 40
            show_step=show_step+1
            show_count_obj = 10
            hand['joint6'] = 250
            hand['joint16'] = 250
            hand['joint21'] = 250
            return list(hand.values())
        elif(show_step==22): #// 并拢拇指
            show_step=show_step+1
            show_count_obj = 20
            hand['joint11'] = 10
            return list(hand.values())
        elif(show_step==23): #// 反转拇指指掌心
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 0
            return list(hand.values())
        elif(show_step==24): #// 分两步回到初始位置
            show_step=show_step+1
            show_count_obj = 30
            hand['joint11'] = 250
            return list(hand.values())
        elif(show_step==25): #// 1
            show_step=show_step+1
            show_count_obj = 50
            hand['joint11'] = 250
            return list(hand.values())
        elif(show_step==26): #// 2
            show_step=show_step+1
            show_count_obj = 10
            hand['joint7'] = 200
            hand['joint8'] = 200
            hand['joint9'] = 200
            hand['joint10'] = 200
            return list(hand.values())
        elif(show_step==27): #// 3
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 80
            hand['joint8'] = 80
            hand['joint9'] = 80
            hand['joint10'] = 80
            return list(hand.values())
        elif(show_step==28): #// 4
            show_step=show_step+1
            show_count_obj = 20
            hand['joint7'] = 128
            hand['joint8'] = 128
            hand['joint9'] = 128
            hand['joint10'] = 128
            return list(hand.values())
        elif(show_step==29): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint17'] = 0
            hand['joint22'] = 0
            return list(hand.values())
        elif(show_step==30): #// 蜷曲4指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint18'] = 0
            hand['joint23'] = 0
            return list(hand.values())
        elif(show_step==31): #// 4
            show_step=show_step+1
            show_count_obj = 15
            hand['joint19'] = 0
            hand['joint24'] = 0
            return list(hand.values())
        elif(show_step==32): #// 4
            show_step=show_step+1
            show_count_obj = 15
            hand['joint20'] = 0
            hand['joint25'] = 0
            return list(hand.values())
        elif(show_step==33): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint2'] = 0
            return list(hand.values())
        elif(show_step==34): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint3'] = 0
            return list(hand.values())
        elif(show_step==35): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint4'] = 0
            return list(hand.values())
        elif(show_step==36): #// 依次蜷曲4小指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint5'] = 0
            return list(hand.values())
        elif(show_step==37): #// 蜷曲拇指
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 0
            hand['joint16'] = 200
            return list(hand.values())
        elif(show_step==38): #// 打开食指和小指
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 250
            hand['joint16'] = 250
            return list(hand.values())
        elif(show_step==39): #// 打开食指和小指
            show_step=show_step+1
            show_count_obj = 30
            hand['joint2'] = 250
            hand['joint5'] = 250
            hand['joint17'] = 250
            hand['joint20'] = 250
            hand['joint22'] = 250
            hand['joint25'] = 250
            return list(hand.values())
        elif(show_step==40): #// 将拇指搭上666
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 100
            hand['joint6'] = 200
            hand['joint11'] = 100
            hand['joint16'] = 100
            return list(hand.values())
        elif(show_step==41): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 80
            hand['joint10'] = 200
            return list(hand.values())
        elif(show_step==42): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 200
            hand['joint10'] = 80
            return list(hand.values())
        elif(show_step==43): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 80
            hand['joint10'] = 200
            return list(hand.values())
        elif(show_step==44): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 200
            hand['joint10'] = 80
            return list(hand.values())
        elif(show_step==45): #// 左右动手指
            show_step=show_step+1
            show_count_obj = 15
            hand['joint7'] = 128
            hand['joint10'] = 128
            return list(hand.values())
        elif(show_step==46): #//  展开
            show_step=show_step+1
            show_count_obj = 50
            hand['joint1'] = 250
            hand['joint3'] = 250
            hand['joint4'] = 250
            hand['joint6'] = 250
            hand['joint11'] = 250
            hand['joint16'] = 250
            hand['joint18'] = 250
            hand['joint19'] = 250
            hand['joint21'] = 250
            hand['joint23'] = 250
            hand['joint24'] = 250
            return list(hand.values())
        elif(show_step==47): #// 拇指和食指捏
            show_step=show_step+1
            show_count_obj = 50
            hand['joint1'] = 40
            hand['joint2'] = 0
            hand['joint6'] = 100
            hand['joint11'] = 70
            hand['joint17'] = 240
            hand['joint22'] = 240
            return list(hand.values())
        elif(show_step==48): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint2'] = 250
            hand['joint6'] = 220
            hand['joint11'] = 100
            hand['joint17'] = 250
            hand['joint22'] = 250
            return list(hand.values())
        elif(show_step==49): #// 拇指和中指捏
            show_step=show_step+1
            show_count_obj = 35
            hand['joint3'] = 0
            hand['joint6'] = 70
            hand['joint11'] = 60
            hand['joint18'] = 220
            hand['joint23'] = 220
            return list(hand.values())
        elif(show_step==50): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint3'] = 250
            hand['joint6'] = 100
            hand['joint11'] = 100
            hand['joint18'] = 250
            hand['joint23'] = 250
            return list(hand.values())
        elif(show_step==51): #// 拇指和无名指捏
            show_step=show_step+1
            show_count_obj = 35
            hand['joint4'] = 0
            hand['joint6'] = 30
            hand['joint11'] = 50
            hand['joint19'] = 220
            hand['joint24'] = 220
            return list(hand.values())
        elif(show_step==52): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint4'] = 250
            hand['joint6'] = 100
            hand['joint11'] = 100
            hand['joint19'] = 250
            hand['joint24'] = 250
            return list(hand.values())
        elif(show_step==53): #// 拇指和小指捏
            show_step=show_step+1
            show_count_obj = 40
            hand['joint5'] = 0
            hand['joint6'] = 0
            hand['joint11'] = 40
            hand['joint20'] = 230
            hand['joint25'] = 230
            return list(hand.values())
        elif(show_step==54): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint5'] = 20
            hand['joint6'] = 0
            hand['joint11'] = 100
            hand['joint20'] = 250
            hand['joint25'] = 250
            return list(hand.values())
        elif(show_step==55): #// 拇指和小指掐
            show_step=show_step+1
            show_count_obj = 40
            hand['joint1'] = 175
            hand['joint5'] = 175
            hand['joint6'] = 0
            hand['joint11'] = 0
            hand['joint16'] = 130
            hand['joint20'] = 100
            hand['joint21'] = 130
            hand['joint25'] = 80
            return list(hand.values())
        elif(show_step==56): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint1'] = 250
            hand['joint5'] = 250
            hand['joint6'] = 0
            hand['joint11'] = 0
            hand['joint16'] = 250
            hand['joint20'] = 250
            hand['joint21'] = 250
            hand['joint25'] = 250
            return list(hand.values())
        elif(show_step==57): #// 拇指和无名指掐
            show_step=show_step+1
            show_count_obj = 35
            hand['joint1'] = 170
            hand['joint4'] = 170
            hand['joint6'] = 30
            hand['joint11'] = 50
            hand['joint16'] = 130
            hand['joint19'] = 80
            hand['joint21'] = 130
            hand['joint24'] = 80
            return list(hand.values())
        elif(show_step==58): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint1'] = 250
            hand['joint4'] = 250
            hand['joint6'] = 30
            hand['joint11'] = 50
            hand['joint16'] = 250
            hand['joint19'] = 250
            hand['joint21'] = 250
            hand['joint24'] = 250
            return list(hand.values())
        elif(show_step==59): #// 拇指和中指掐
            show_step=show_step+1
            show_count_obj = 35
            hand['joint1'] = 155
            hand['joint3'] = 155
            hand['joint6'] = 70
            hand['joint11'] = 60
            hand['joint16'] = 130
            hand['joint19'] = 90
            hand['joint21'] = 130
            hand['joint24'] = 80
            return list(hand.values())
        elif(show_step==60): #// 1
            show_step=show_step+1
            show_count_obj = 20
            hand['joint1'] = 250
            hand['joint3'] = 250
            hand['joint6'] = 100
            hand['joint11'] = 100
            hand['joint16'] = 250
            hand['joint19'] = 250
            hand['joint21'] = 250
            hand['joint24'] = 250
            return list(hand.values())
        elif(show_step==61): #// 拇指和食指掐
            show_step=show_step+1
            show_count_obj = 35
            hand['joint1'] = 165
            hand['joint2'] = 165
            hand['joint6'] = 100
            hand['joint11'] = 70
            hand['joint16'] = 130
            hand['joint19'] = 80
            hand['joint21'] = 130
            hand['joint24'] = 80
            return list(hand.values())
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