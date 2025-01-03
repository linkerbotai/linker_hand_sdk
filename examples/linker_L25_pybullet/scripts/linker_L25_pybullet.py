#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy, rospkg, time, os, sys
import pybullet as p
import pybullet_data
from urdf_parser_py.urdf import URDF
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class LinkerL25Pybullet:
    def __init__(self):
        rospy.init_node('linker_L25_pybullet', anonymous=True)
        rospack = rospkg.RosPack()
        self.rate = rospy.Rate(100)

        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        plane_id = p.loadURDF("plane.urdf")
        package_path = rospack.get_path('linker_L25_pybullet')
        urdf_path = os.path.join(package_path, 'urdf', 'steering_1_1.urdf')
        self.robot = URDF.from_xml_file(urdf_path)
        orientation = p.getQuaternionFromEuler([0, 0, -1.0708])
        self.hand_id = p.loadURDF(urdf_path, basePosition=[0, 0, 0.02], baseOrientation=orientation, useFixedBase=True)
        self.hand_joints = p.getNumJoints(self.hand_id)

    def run(self):
        while not rospy.is_shutdown():
            self.set_joint(self.hand_id)
            p.setSimulation()
            self.rate.sleep()

    def set_joint(self, hand_id, pos=[0.0] * 21):
        for index, item in enumerate(pos):
            joint_info = p.getJointInfo(hand_id, index)
            joint_name = joint_info[1].decode('utf-8')
            p.setJointMotorControl2(hand_id, index, p.POSITION_CONTROL, targetPosition=item, force=500)


if __name__ == '__main__':
    try:
        LinkerL25Pybullet().run()
    except rospy.ROSInterruptException:
        pass
    finally:
        p.disconnect()
