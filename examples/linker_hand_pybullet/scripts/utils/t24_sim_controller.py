import time,rospkg,rospy
import pybullet as p
import pybullet_data
from std_msgs.msg import String, Header
from sensor_msgs.msg import JointState
'''
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [248, 127, 107, 180, 214, 42, 137, 0.0, 30, 20, 189, 0.0, 0.0, 0.0, 0.0, 59, 47, 32, 11, 17, 170, 43, 84, 76, 81], velocity: [], effort: []}" -r 10
'''
class T24SimController:
    def __init__(self):
        rospack = rospkg.RosPack()
        urdf_path_right = rospack.get_path('linker_hand_pybullet') + "/urdf/t24/linkerhand_t24_1_right.urdf"
        urdf_path=urdf_path_right
        self.right_hand_state_pub = rospy.Publisher("/cb_right_hand_state_sim",JointState,queue_size=0)
        self.right_hand_num_joints = 26
        self.right_position = [0.0] * 26
        """
        初始化PyBullet仿真环境
        :param urdf_path: URDF文件路径
        :param start_pos: 初始位置 [x, y, z]
        :param start_ori: 初始姿态四元数 [x, y, z, w]
        """
        
        # 连接物理服务器
        self.client = p.connect(p.GUI)  # 使用图形界面
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # 添加默认资源路径
        # 初始化仿真参数
        p.setGravity(0, 0, -9.81)     # 设置重力
        p.setTimeStep(1./240.)        # 时间步长
        print("_-"*20)
        print(urdf_path)
        # 加载URDF模型
        try:
            self.right_hand_id = p.loadURDF(urdf_path, basePosition=[0, 0.1, 0.1], useFixedBase=True)
            print(f"成功加载URDF模型: {urdf_path}")
        except Exception as e:
            print(f"加载URDF失败: {str(e)}")
            p.disconnect()
            raise
        p.setPhysicsEngineParameter(enableFileCaching=0)
        # 设置摄像机视角
        self._setup_camera()

    def _setup_camera(self, distance=1.5, yaw=45, pitch=-30, target_pos=[0, 0, 0]):
        """设置初始摄像机视角"""
        p.resetDebugVisualizerCamera(
            cameraDistance=distance,
            cameraYaw=yaw,
            cameraPitch=pitch,
            cameraTargetPosition=target_pos
        )

    def step_simulation(self):
        """执行单步仿真"""
        p.stepSimulation()
        time.sleep(1./240.)  # 保持实时仿真速度
    # 添加关节控制示例（在类中添加）
    def set_joint_control(self, joint_index, target_velocity):
        """设置关节速度控制"""
        p.setJointMotorControl2(
            bodyUniqueId=self.right_hand_id,
            jointIndex=joint_index,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocity=target_velocity
        )
    def set_joint(self,hand_id, pos):
        for index, item in enumerate(pos):
            p.setJointMotorControl2(
                bodyUniqueId=hand_id,           # 机器人ID
                jointIndex=index,          # 关节索引
                controlMode=p.POSITION_CONTROL,  # 控制模式：位置控制
                targetPosition=item,  # 目标位置
                force=500                        # 最大力矩限制
            )
    def set_left_position(self, pos):
        self.left_position = pos
    def set_right_position(self, pos):
        self.right_position = pos

    # 添加状态获取示例
    def get_joint_states(self):
        """获取所有关节状态"""
        return p.getJointStates(self.right_hand_id, range(p.getNumJoints(self.right_hand_id)))
    
    def run(self):
        """运行仿真循环"""
        print("开始仿真 (关闭窗口终止程序)...")
        mapping = {
            0:10, 1:5, 2:0, 3:15, 4:20, 6:6, 7:1, 8:16, 9:21,  11:7, 12:2, 13:17, 14:22, 16:8, 17:3, 18:18, 19:23, 21:9, 22:4, 23:19, 24:24
        }
        tmp_right = {
                "position":[0.0] * 25,
                "velocity":[0.0] * 25,
                "effort":[0.0] * 25
            }
        while True:
            self.step_simulation()
            for index in range(self.right_hand_num_joints):
                joint_state = p.getJointState(self.right_hand_id, index)
                # 检查当前关节是否在映射表中
                if index in mapping:
                    mapped_index = mapping[index]
                    tmp_right["position"][mapped_index] = round(joint_state[0],3)
                    tmp_right["velocity"][mapped_index] = round(joint_state[1], 3)
                    tmp_right["effort"][mapped_index] = round(joint_state[3], 3)
            right_msg = self.joint_msg(hand="right",position=tmp_right["position"], velocity=tmp_right["velocity"], effort=tmp_right["effort"])
            self.right_hand_state_pub.publish(right_msg)
            self.set_joint(self.right_hand_id,self.right_position)
            # 处理键盘输入
            keys = p.getKeyboardEvents()
            if ord('q') in keys and keys[ord('q')] & p.KEY_WAS_TRIGGERED:
                break

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
    def __del__(self):
        """析构时断开连接"""
        p.disconnect()

