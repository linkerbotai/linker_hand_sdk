#!/usr/bin/env python3
import rospy,rospkg
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import std_msgs.msg
import time
import threading
import signal
import sys,os
joint_state = JointState()
hand_joint = "L25" # 控制L20版本灵巧手
hand_type = "left" # 控制左手

def send_messages():
    rospy.init_node('dong_test_sender', anonymous=True)
    if hand_type == "left":
        pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)
    elif hand_type == "right":
        pub = rospy.Publisher('/cb_right_hand_control_cmd', JointState, queue_size=10)
    if hand_joint == "L25":
        
        # 张开步骤
        pos1_1 = [230, 0, 0,15, 5, 250, 55, 0, 75, 95, 85, 0, 0, 0, 0, 250, 0, 40, 35, 5, 250, 0, 5, 0, 0]
        pos1_2 = [80, 255, 255, 255, 255, 180, 51, 51, 72, 202, 202, 255.0, 255.0, 255.0, 255.0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
        # 握拳步骤
        pos2_1 = [230, 0, 0,15, 5, 250, 55, 0, 75, 95, 85, 0, 0, 0, 0, 80, 0, 40, 35, 5, 250, 0, 5, 0, 0]
        #pos2_2 = [250, 0, 0,15, 5, 42, 55, 0, 75, 95, 85, 0, 0, 0, 0, 250, 0, 40, 35, 5, 90, 0, 5, 0, 0]
        pos2_2 = [230, 0, 0, 15, 5, 42, 55, 0, 75, 95, 85, 0, 0, 0, 0, 90, 0, 40, 35, 5, 120, 0, 5, 0, 0]
    rate = rospy.Rate(30)  # 设置频率为30Hz
    joint_state.header = std_msgs.msg.Header()
    joint_state.header.seq=0
    joint_state.header.stamp = rospy.Time.now() 
    joint_state.header.frame_id = ''
    joint_state.name=['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6',
                        'joint7', 'joint8', 'joint9', 'joint10', 'joint11', 'joint12',
                        'joint13', 'joint14', 'joint15', 'joint16', 'joint17', 'joint18',
                        'joint19', 'joint20']
    count = 0
    while not rospy.is_shutdown():  # 持续1秒
        joint_state.position = pos2_1
        joint_state.velocity = [0] * len(joint_state.position)  # 与position数组长度相同，全部填充为0
        joint_state.effort = [0] * len(joint_state.position)  
        pub.publish(joint_state)
        print(pos2_1)
        time.sleep(1.3)
        joint_state.position = pos2_2
        joint_state.velocity = [0] * len(joint_state.position)  # 与position数组长度相同，全部填充为0
        joint_state.effort = [0] * len(joint_state.position)  
        pub.publish(joint_state)
        print(pos2_2)
        time.sleep(5)

        joint_state.position = pos1_1
        joint_state.velocity = [0] * len(joint_state.position)  # 与position数组长度相同，全部填充为0
        joint_state.effort = [0] * len(joint_state.position)  
        pub.publish(joint_state)
        print(pos1_1)
        time.sleep(0.5)
        joint_state.position = pos1_2
        joint_state.velocity = [0] * len(joint_state.position)  # 与position数组长度相同，全部填充为0
        joint_state.effort = [0] * len(joint_state.position)  
        pub.publish(joint_state)
        print(pos1_1)
            
        rate.sleep()
        print(f"循环完成{count}次")
        count = count+1
        time.sleep(3)


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