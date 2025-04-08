import time,rospkg,rospy
import pybullet as p
import pybullet_data
from std_msgs.msg import String, Header
from sensor_msgs.msg import JointState

class L10SimController:
    def __init__(self):
        self.left_hand_state_pub = rospy.Publisher("/cb_left_hand_state_sim",JointState,queue_size=10)
        self.right_hand_state_pub = rospy.Publisher("/cb_right_hand_state_sim",JointState,queue_size=10)
        rospack = rospkg.RosPack()
        urdf_path_left = rospack.get_path('linker_hand_pybullet') + "/urdf/linker_hand_l10_6_left.urdf"
        urdf_path_right = rospack.get_path('linker_hand_pybullet') + "/urdf/linker_hand_l10_6_right.urdf"
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
            # 索引映射表
            # index_map = {
            #     0: 0, 7: 1, 12: 2, 17: 3, 22: 4,
            #     1: 5, 6: 6, 11: 7, 16: 8, 21: 9,
            #     2: 10, 3: 15, 8: 16, 13: 17, 18: 18, 23: 19
            # }
            index_map = {
                0:9, 1: 1, 3:0,
                7:2, 10:3, 14: 4,

            }
            tmp_left = {
                "position":[0.0] * 20,
                "velocity":[0.0] * 20,
                "effort":[0.0] * 20
            }
            tmp_right = {
                "position":[0.0] * 20,
                "velocity":[0.0] * 20,
                "effort":[0.0] * 20
            }

            # 遍历所有关节并获取数据
            for joint_index in range(self.left_hand_num_joints):
                joint_info = p.getJointInfo(self.left_hand_id, joint_index)
                joint_name = joint_info[1].decode()  # 获取关节名称并解码为字符串
                print(joint_name)
                joint_state = p.getJointState(self.left_hand_id, joint_index)
                # 检查当前关节是否在映射表中
                # if joint_index in index_map:
                #     mapped_index = index_map[joint_index]
                #     tmp_left["position"][mapped_index] = round(joint_state[0],3)
                #     tmp_left["velocity"][mapped_index] = round(joint_state[1], 3)
                #     tmp_left["effort"][mapped_index] = round(joint_state[3], 3)
            # for index in range(self.right_hand_num_joints):
            #     joint_state = p.getJointState(self.right_hand_id, index)
            #     # 检查当前关节是否在映射表中
            #     if index in index_map:
            #         mapped_index = index_map[index]
            #         tmp_right["position"][mapped_index] = round(joint_state[0],3)
            #         tmp_right["velocity"][mapped_index] = round(joint_state[1], 3)
            #         tmp_right["effort"][mapped_index] = round(joint_state[3], 3)
            left_msg = self.joint_msg(hand="left",position=tmp_left["position"], velocity=tmp_left["velocity"], effort=tmp_left["effort"])
            self.left_hand_state_pub.publish(left_msg)
            self.set_joint(self.left_hand_id,self.left_position)
            right_msg = self.joint_msg(hand="right",position=tmp_right["position"], velocity=tmp_right["velocity"], effort=tmp_right["effort"])
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
            joint_state_msg.name = ["joint41","joint42","joint43","joint44","joint45","joint46","joint47","joint48",
"joint49","joint50","joint51","joint52","joint53","joint54","joint55","joint56","joint57","joint58","joint59","joint60"]  # 关节名称
        elif hand == "right":
            joint_state_msg.name = ["joint71","joint72","joint73","joint77","joint75","joint76","joint77","joint78","joint79","joint80","joint81","joint82","joint83","joint84","joint88","joint86","joint87","joint88","joint89","joint90"]  # 关节名称
        joint_state_msg.position = position  # 关节位置（弧度）
        joint_state_msg.velocity = velocity  # 关节速度
        joint_state_msg.effort = effort  # 关节力矩
        return joint_state_msg