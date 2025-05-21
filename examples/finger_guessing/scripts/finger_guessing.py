#!/usr/bin/env python3
import rospy,rospkg
import signal
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import can
import json
import yaml
import time
import threading
import sys
import os
import subprocess
from std_msgs.msg import Header, Float32MultiArray
import cv2
import mediapipe as mp
rospack = rospkg.RosPack()
ros_linker_hand_sdk_path = rospack.get_path('linker_hand_sdk_ros')
sys.path.append(ros_linker_hand_sdk_path + '/scripts')
from LinkerHand.utils.init_linker_hand import InitLinkerHand

class FingerGuessing:
    def __init__(self):
        self.check_hand = InitLinkerHand()
        self.left_hand_exist,self.right_hand_exist,self.left_hand_joint,self.right_hand_joint,self.left_hand_type,self.right_hand_type = self.check_hand.current_hand()
        self.set_pub = rospy.Publisher('/cb_hand_setting_cmd', String, queue_size=1)
        # 只能单手使用
        if self.left_hand_exist == True and self.right_hand_exist == True:
            self.right_hand_exist = False
            self.right_hand_joint = None
            self.right_hand_type = None
        if self.left_hand_exist == True:
            self.hand_type = self.left_hand_type
            self.hand_joint = self.left_hand_joint
        elif self.right_hand_exist == True:
            self.hand_type = self.right_hand_type
            self.hand_joint = self.right_hand_joint
        if self.hand_joint == "L10":
            self.set_speed(speed=[130,250,250,250,250])
        if self.hand_joint == "L25":
            self.set_speed(speed=[80, 250, 250, 250, 250])
        print(f"{self.hand_type} -- {self.hand_joint}")
        self.hand_landmarks = None # 手部关键点
        self.shared_resource = 'NONE'
        self.isrunning = True
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.labels = ['Rock', 'Paper', 'Scissors','NONE']  # 石头、布、剪刀
        if self.hand_joint == 'L10':
            self.rock_pose = [120, 60, 5, 5, 5, 5, 250, 250, 250, 40] # 石头
            self.rock_pose_msg = self.create_joint_state_msg(self.rock_pose,[])
            self.paper_pose = [250, 230, 250, 250, 250, 250, 250, 250, 250, 70] # 布
            self.paper_pose_msg = self.create_joint_state_msg(self.paper_pose,[])
            self.scissors_pose = [120, 60, 250, 250, 0, 0,250, 250, 250, 40] # 剪刀
            self.scissors_pose_msg = self.create_joint_state_msg(self.scissors_pose,[])
        if self.hand_joint == 'L25':
            self.rock_pose = [250, 0, 0, 15, 5, 250, 55, 0, 75, 95, 85, 0, 0, 0, 0, 85, 0, 40, 35, 5, 70, 0, 5, 25, 0] # 石头
            self.rock_pose_1 = [250, 0, 0, 15, 5, 30, 55, 0, 75, 95, 85, 0, 0, 0, 0, 85, 0, 40, 35, 5, 70, 0, 5, 25, 0] # 石头
            self.rock_pose_msg = self.create_joint_state_msg(self.rock_pose,[])
            self.rock_pose_1_msg = self.create_joint_state_msg(self.rock_pose_1,[])
            self.paper_pose = [75, 250, 250, 250, 250, 175, 50, 50, 70, 200, 200, 0, 0, 0, 0, 250, 250, 250, 250, 250, 250, 0, 250, 250, 250] # 布
            self.paper_pose_msg = self.create_joint_state_msg(self.paper_pose,[])
            self.scissors_pose = [120, 60, 250, 250, 0, 0,250, 250, 250, 40] # 剪刀
            self.scissors_pose_msg = self.create_joint_state_msg(self.scissors_pose,[])
        if self.hand_type == 'left':
            self.hand_pub = rospy.Publisher(f"/cb_left_hand_control_cmd", JointState, queue_size=1)
        else:
            self.hand_pub = rospy.Publisher(f"/cb_right_hand_control_cmd", JointState, queue_size=1)
        self.stop_event = threading.Event()  # 创建一个事件对象
        self.camera_thread = threading.Thread(target=self.main)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        self.hand_control_thread = threading.Thread(target=self.hand_control_func)
        self.hand_control_thread.daemon = True
        self.hand_control_thread.start()
        
    def create_joint_state_msg(self, position, names):
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.name = names
        msg.position = list(map(float, position))
        msg.velocity = [0.0] * len(position)
        msg.effort = [0.0] * len(position)
        return msg
    def set_speed(self,speed=[130,250,250,250,250]):
        msg = String()
        cmd = {
            "setting_cmd":"set_speed",
            "params":{
                "hand_type": self.hand_type,
                "speed":speed,
            }
        }
        msg.data = json.dumps(cmd)
        for i in range(3):
            self.set_pub.publish(msg)
            time.sleep(0.1)
    def distance(self,m, n):
        return ((n.x-m.x)**2+(n.y-m.y)**2)**0.5
    def classify_gesture(self, landmarks):
        base = 0.1


        distance_0_8 = self.distance(landmarks.landmark[0],landmarks.landmark[8])
        distance_0_12 = self.distance(landmarks.landmark[0],landmarks.landmark[12])
        distance_0_16 = self.distance(landmarks.landmark[0],landmarks.landmark[16])
        distance_0_20 = self.distance(landmarks.landmark[0],landmarks.landmark[20])
        distance_0_7 = self.distance(landmarks.landmark[0], landmarks.landmark[7])
        distance_0_11 = self.distance(landmarks.landmark[0], landmarks.landmark[11])
        distance_0_15 = self.distance(landmarks.landmark[0], landmarks.landmark[15])
        distance_0_19 = self.distance(landmarks.landmark[0], landmarks.landmark[19])


        # thumb_tip = landmarks[4].y
        # index_tip = landmarks[8].y

        if distance_0_8 > distance_0_7  and distance_0_12 > distance_0_11 and distance_0_16 < distance_0_15 and distance_0_20 < distance_0_19:
            return 2  # Scissors
        elif distance_0_8 >= distance_0_7 and distance_0_12 >= distance_0_11 and distance_0_16 > distance_0_15 and distance_0_20 > distance_0_19:
            return 1  # Paper
        elif distance_0_8 < distance_0_7 and distance_0_12 < distance_0_11 and distance_0_16 < distance_0_15 and distance_0_20 < distance_0_19:
            return 0  # Rock
        else:
            return 3 # NONE
    def hand_control_func(self):
        while True:
            if self.isrunning == False:
                break
            print(self.shared_resource)
            gesture_label = self.shared_resource
            #print('ok')
            if gesture_label == 'Rock': # 石头
                time.sleep(0.1)
                #print(self.paper_pose_msg.position)
                self.hand_pub.publish(self.paper_pose_msg)
                time.sleep(0.1)
                #self.shared_resource = 'NONE'
            elif gesture_label == 'Paper': # 布
                time.sleep(0.1)
                #print(self.scissors_pose_msg.position)
                self.hand_pub.publish(self.scissors_pose_msg)
                time.sleep(0.1)
                #self.shared_resource = 'NONE'
            elif gesture_label == 'Scissors': # 剪刀
                time.sleep(0.1)
                #print(self.rock_pose_msg.position)
                self.hand_pub.publish(self.rock_pose_msg)
                time.sleep(0.1)
                #self.shared_resource = 'NONE'
            else:
                #print(self.paper_pose_msg.position)
                self.hand_pub.publish(self.paper_pose_msg)
            
    
    def main(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened() and self.isrunning:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    gesture_label = self.labels[self.classify_gesture(hand_landmarks)]
                    cv2.putText(frame, gesture_label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    self.shared_resource = gesture_label
            cv2.imshow('Hand Gesture Recognition', frame)

            if cv2.waitKey(5) & 0xFF == 27:  # 按 'ESC' 键退出
                break
        cap.release()
        cv2.destroyAllWindows()
    def shutdown(self):
        self.isrunning = False
        self.stop_event.set()
        self.hand_pub.unregister()
        rospy.signal_shutdown('shutdown')
        print('shutdown')
        sys.exit(0)
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    fg.shutdown()
    sys.exit(0)
if __name__ == '__main__':
    '''
    rosrun finger_guessing finger_guessing.py
    '''
    rospy.init_node('finger_guessing', anonymous=True)
    rospy.Rate(60)
    fg = FingerGuessing()
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # kill 命令
    #fg.main()
    rospy.spin()