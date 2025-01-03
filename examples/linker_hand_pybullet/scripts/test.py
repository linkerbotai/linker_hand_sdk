import pybullet as p
import pybullet_data
import time
path = "/home/hjx/ROS/linker_hand_pybullet/src/linker_hand_pybullet/urdf/linker_hand_l20_8_left.urdf"
# 连接到仿真
physics_client = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
# 加载机器人 URDF
robot_id = p.loadURDF(path, basePosition=[0, 0, 0.1], useFixedBase=True)
plane_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[10, 10, 0.1])
plane_id = p.createMultiBody(0, plane_collision_shape)
p.setPhysicsEngineParameter(enableFileCaching=0)

p.setGravity(0, 0, -9.81)
time_step = 1.0 / 240.0
p.setTimeStep(time_step)

# 获取关节总数和信息
num_joints = p.getNumJoints(robot_id)
print(f"机器人关节总数: {num_joints}")

# 仿真循环
try:
    while True:
        p.stepSimulation()
        time.sleep(time_step)

        # 遍历所有关节并获取数据
        for joint_index in range(num_joints):
            joint_state = p.getJointState(robot_id, joint_index)
            joint_position = joint_state[0]
            joint_velocity = joint_state[1]
            motor_torque = joint_state[3]

            print(f"关节 {joint_index}: 位置={joint_position:.3f}, 速度={joint_velocity:.3f}, 力矩={motor_torque:.3f}")

except KeyboardInterrupt:
    print("仿真结束")
    p.disconnect()
