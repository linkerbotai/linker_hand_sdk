import time,rospkg,rospy
import pybullet as p
import pybullet_data
from std_msgs.msg import String, Header
from sensor_msgs.msg import JointState
from .mapping import arc_to_range_left, arc_to_range_right


class L7SimController:
    def __init__(self):
        self.left_hand_state_pub = rospy.Publisher("/cb_left_hand_state_sim",JointState,queue_size=10)
        self.right_hand_state_pub = rospy.Publisher("/cb_right_hand_state_sim",JointState,queue_size=10)
        rospack = rospkg.RosPack()
        urdf_path_left = rospack.get_path('linker_hand_pybullet') + "/urdf/l7/left/linkerhand_l7_left.urdf"
        urdf_path_right = rospack.get_path('linker_hand_pybullet') + "/urdf/l7/right/linkerhand_l7_right.urdf"
        # 连接到仿真
        physics_client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        # 加载 URDF 左手
        self.left_hand_id = p.loadURDF(urdf_path_left, basePosition=[0, -0.1, 0.1], useFixedBase=True)
        self.right_hand_id = p.loadURDF(urdf_path_right, basePosition=[0, 0.1, 0.1], useFixedBase=True)
        # 加载地面
        plane_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[10, 10, 0.1])
        plane_id = p.createMultiBody(0, plane_collision_shape)
        p.setPhysicsEngineParameter(enableFileCaching=0)
        # 重力
        p.setGravity(0, 0, -9.81)
        self.time_step = 1.0 / 240.0
        p.setTimeStep(self.time_step)
        # 获取关节总数和信息
        self.left_hand_num_joints = p.getNumJoints(self.left_hand_id)
        self.right_hand_num_joints = p.getNumJoints(self.right_hand_id)
        self.left_position = [0] * 25
        self.right_position = [0] * 25
    def set_left_position(self, pos):
        self.left_position = pos
    def set_right_position(self, pos):
        self.right_position = pos
    def showSim(self):
        while True:
            p.stepSimulation()
            time.sleep(self.time_step)
            tmp_left = {
                "position":[0.0] * 7,
                "velocity":[0.0] * 7,
                "effort":[0.0] * 7
            }
            tmp_right = {
                "position":[0.0] * 7,
                "velocity":[0.0] * 7,
                "effort":[0.0] * 7
            }
            # 遍历所有关节并获取数据
            # for joint_index in range(self.left_hand_num_joints):
            #     joint_info = p.getJointInfo(self.left_hand_id, joint_index)
            #     joint_name = joint_info[1].decode()  # 获取关节名称并解码为字符串
            #     print(joint_name)
            #     joint_state = p.getJointState(self.left_hand_id, joint_index)
            m = [2,1,7,11,16,21,0]
            for index in range(len(m)):
                i = m[index]
                tmp_left["position"][index] = self.left_position[i]
                tmp_right["position"][index] = self.right_position[i]
            left_msg = self.joint_msg(hand="left",position=arc_to_range_left(hand_arc_l=tmp_left["position"],hand_joint="L7"), velocity=tmp_left["velocity"], effort=tmp_left["effort"])
            self.left_hand_state_pub.publish(left_msg)
            self.set_joint(self.left_hand_id,self.left_position)
            right_msg = self.joint_msg(hand="right",position=arc_to_range_right(right_arc=tmp_right["position"],hand_joint="L7"), velocity=tmp_right["velocity"], effort=tmp_right["effort"])
            self.right_hand_state_pub.publish(right_msg)
            self.set_joint(self.right_hand_id,self.right_position)
    def set_joint(self,hand_id, pos):
        for index, item in enumerate(pos):
            p.setJointMotorControl2(
                bodyUniqueId=hand_id,           # 机器人ID
                jointIndex=index,          # 关节索引
                controlMode=p.POSITION_CONTROL,  # 控制模式：位置控制
                targetPosition=item,  # 目标位置
                force=500                        # 最大力矩限制
            )

    def joint_msg(self,hand,position,velocity,effort):
        # 初始化JointState消息
        joint_state_msg = JointState()
        if hand == "left":
            joint_state_msg.name = []  # 关节名称
        elif hand == "right":
            joint_state_msg.name = []  # 关节名称
        joint_state_msg.position = position  # 关节位置（弧度）
        joint_state_msg.velocity = velocity  # 关节速度
        joint_state_msg.effort = effort  # 关节力矩
        return joint_state_msg
    