import rospy, rospkg, yaml, os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sensor_msgs.msg import JointState
from std_msgs.msg import Header


class RosHandler():
    def __init__(self,hand_joint="L20", hand_type="left"):
        self.hand_joint = hand_joint
        self.hand_type = hand_type
        self.is_open = True
        if self.hand_type == "left":
            self.hand_pub = rospy.Publisher('/cb_left_hand_control_cmd', JointState, queue_size=10)
        elif self.hand_type == "right":
            self.hand_pub = rospy.Publisher('/cb_right_hand_control_cmd', JointState, queue_size=10)
        self.rate = rospy.Rate(100)  # 100 Hz

    def pub_msg(self, pos):
        msg = self.joint_msg(data=pos)
        self.hand_pub.publish(msg)
        self.rate.sleep()
    def pub_msg_once(self,pos):
        msg = self.joint_msg(data=pos)
        self.hand_pub.publish(msg)
    def joint_msg(self, data):
        """创建 JointState 消息"""
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.name = []
        msg.position = [float(i) for i in data.split(",")]
        return msg