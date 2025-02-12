#!/usr/bin/env python3
import rospy,time,json
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import argparse
global hand_type
def set_disability():
    pub = rospy.Publisher('/cb_hand_setting_cmd', String, queue_size=10)
    msg = String()
    cmd = {
        "setting_cmd":"set_disability",
        "params":{
            "hand_type":hand_type,
        }
    }
    msg.data = json.dumps(cmd)
    time.sleep(0.1)
    pub.publish(msg)

def doMsg(msg):
    if hand_type == "left":
        pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)
    elif hand_type == "right":
        pub = rospy.Publisher('/cb_right_hand_control_cmd', JointState, queue_size=10)
    print("_-"*30)
    print(hand_type)
    pub.publish(msg)

if __name__ == "__main__":
    '''bash
    python set_remote_control.py --hand_type=left or right
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--hand_type", type=str, default="left")
    args = parser.parse_args()
    hand_type = args.hand_type
    #2.初始化 ROS 节点:命名(唯一)
    rospy.init_node("set_remote_control")
    rate = rospy.Rate(60)  # 设置频率为30Hz
    # 首先设置为失能模式
    set_disability()
    rospy.loginfo(f"开始T24版本{hand_type}遥操模式")
    if hand_type == "left":
        sub = rospy.Subscriber("/cb_left_hand_state",JointState,doMsg,queue_size=10)
    elif hand_type == "right":
        sub = rospy.Subscriber("/cb_right_hand_state",JointState,doMsg,queue_size=10)
    rospy.spin()