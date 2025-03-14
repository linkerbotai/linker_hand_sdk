#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import std_msgs.msg
import time,json
import signal
import sys
import argparse


def send_messages(hand_type="right"):

    rospy.init_node('set_disability', anonymous=True)

    pub = rospy.Publisher('/cb_hand_setting_cmd', String, queue_size=10)

    rate = rospy.Rate(30)  # 设置频率为30Hz
    msg = String()
    cmd = {
        "setting_cmd":"set_disability",
        "params":{
            "hand_type":hand_type,
        }
    }
    msg.data = json.dumps(cmd)
    print(msg)
    time.sleep(0.1)
    pub.publish(msg)




def signal_handler(sig, frame):

    print('You pressed Ctrl+C!')

    sys.exit(0)  # 0表示正常退出
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    '''bash
    python set_disability.py --hand_type=left or right
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--hand_type", type=str, default="left")
    args = parser.parse_args()
    try:
        send_messages(hand_type=args.hand_type)
    except KeyboardInterrupt:
         print("Caught KeyboardInterrupt, exiting gracefully.")
    except rospy.ROSInterruptException:
        print("ROSInterruptException")
    finally:
         print("Cleaning up...")