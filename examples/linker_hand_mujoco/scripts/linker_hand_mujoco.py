import mujoco
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.color_msg import ColorMsg
from utils.mj_control import MJControlWrapper

class MujocoSim:
    def __init__(self, model_path):
        # 加载模型并初始化控制器
        self.mj = MJControlWrapper(model_path=model_path)
        self.mj.model.opt.gravity[:] = [0, 0, -0.98]  # 设置重力
        
        # 初始化基座状态
        self.mj.data.qpos[:7] = [0, 0, 0.01, 1, 0, 0, 0]
        self.mj.data.qvel[:6] = [0, 0, 0, 0, 0, 0]
        
        # 启动可视化
        self.mj.launch_viewer(viewer_type="active")
        
        self.start_time = time.time()

    def get_all_joints(self):
        """获取并打印所有关节信息"""
        for joint_id in range(self.mj.model.njnt):
            joint_name = self.mj.model.joint(joint_id).name
            joint_type = self.mj.model.jnt_type[joint_id]
            joint_range = self.mj.model.jnt_range[joint_id] if joint_type != mujoco.mjtJoint.mjJNT_FREE else None
            joint_pos = self.mj.data.qpos[self.mj.model.jnt_qposadr[joint_id]]
            joint_vel = self.mj.data.qvel[self.mj.model.jnt_dofadr[joint_id]]

            print(f"关节 {joint_id}:")
            print(f"  名称: {joint_name}")
            print(f"  类型: {self._get_joint_type_name(joint_type)}")
            print(f"  范围: {joint_range}")
            print(f"  当前位置: {joint_pos}")
            print(f"  当前速度: {joint_vel}")
            print("-" * 30)

    def _get_joint_type_name(self, joint_type):
        """将关节类型转换为可读名称"""
        joint_types = {
            mujoco.mjtJoint.mjJNT_FREE: "自由关节 (6自由度)",
            mujoco.mjtJoint.mjJNT_BALL: "球关节 (3自由度)",
            mujoco.mjtJoint.mjJNT_SLIDE: "滑动关节 (1自由度)",
            mujoco.mjtJoint.mjJNT_HINGE: "旋转关节 (1自由度)",
        }
        return joint_types.get(joint_type, "未知类型")

    def simulate(self):
        """运行仿真循环"""
        try:
            while True:
                self.get_all_joints()
                # 更新仿真到当前时间
                current_time = time.time() - self.start_time
                self.mj.step(until=current_time)
        except KeyboardInterrupt:
            self.close()

    def close(self):
        """关闭仿真"""
        self.mj.close_viewer()

if __name__ == "__main__":
    model_path = '/home/hjx/ROS/Linker_Hand_SDK_ROS/src/linker_hand_sdk/examples/linker_hand_mujoco/urdf/linker_hand_l20_8_right.xml'
    sim = MujocoSim(model_path)
    sim.simulate()
    

