#!/usr/bin/env python3
import rospy,rospkg
import json
from std_msgs.msg import String

class CheckHand:
    def __init__(self):
        self.left_hand_exist = False
        self.right_hand_exist = False
        self.left_hand_joint = None
        self.right_hand_joint = None
        self.left_hand_type = None
        self.right_hand_type = None

    def _check_topic_exists(self,topic_name):
        # 获取所有已发布的话题
        published_topics = rospy.get_published_topics()
        # 遍历话题列表，检查目标话题是否存在
        for topic, _ in published_topics:
            if topic == topic_name:
                return True
        return False
    def check_hand(self):
        left_hand_info = None
        right_hand_info = None
        if self._check_topic_exists('/cb_left_hand_info'):
            left_hand_info = rospy.wait_for_message('/cb_left_hand_info',String,timeout=0.1)
        if self._check_topic_exists('/cb_right_hand_info'):
            right_hand_info = rospy.wait_for_message('/cb_right_hand_info',String,timeout=0.1)
        if left_hand_info is not None:
            msg = json.loads(left_hand_info.data)
            self.left_hand_exist = True
            self.left_hand_joint = msg['left_hand']["hand_joint"]
            self.left_hand_type = "left"
        if right_hand_info is not None:
            msg = json.loads(right_hand_info.data)
            print("msg:",msg)
            self.right_hand_exist = True
            self.right_hand_joint = msg['right_hand']["hand_joint"]
            self.right_hand_type = "right"
        return self.left_hand_exist,self.right_hand_exist,self.left_hand_joint,self.right_hand_joint,self.left_hand_type,self.right_hand_type

    
    
    