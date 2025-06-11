#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import sys,os,rospy
import threading
from sensor_msgs.msg import JointState
import numpy as np
import mujoco, time
import mujoco.viewer
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from utils.mapping import *
rospy.init_node('linker_hand_mujoco')
hand_type = rospy.get_param('~hand_type', "right")
hand_joint = rospy.get_param('~hand_joint', "L10")


JOINT_CONFIG = {
    "L7": {
        "map": L7_JOINT_MAP,
        "arc": L7_JOINT_ARC
    },
    "L10": {
        "map": L10_JOINT_MAP,
        "arc": L10_JOINT_ARC
    },
    "L20": {
        "map": L20_JOINT_MAP,
        "arc": L20_JOINT_ARC
    },
    "L21": {
        "map": L21_JOINT_MAP,
        "arc": L21_JOINT_ARC,
    }
}

# 直接通过字典获取配置
joint_config = JOINT_CONFIG.get(hand_joint)
if joint_config:
    joint_map = joint_config["map"]
    joint_arc = joint_config["arc"]
else:
    # 处理未匹配的情况（可选）
    joint_map = None
    joint_arc = None
XML_PATH = os.path.dirname(os.path.abspath(__file__))+f"/urdf/{hand_joint.upper()}/linker_hand_{hand_joint.lower()}_{hand_type}/linker_hand_{hand_joint.lower()}_{hand_type}.xml"

# --- 加载模型 ---
model = mujoco.MjModel.from_xml_path(XML_PATH)
model.dof_damping[:] = 0.8  # 所有关节都设置为 1.0 阻尼
data = mujoco.MjData(model)


print("=" * 20)
print(mujoco.mj_versionString())  # 查看MuJoCo版本
print("=" * 20)
data.qpos[:] = 0
data.qvel[:] = 0
model.opt.disableflags = 1
mujoco.mj_forward(model, data)

joint_count = model.nu
joint_names = []
for i in range(model.njnt):
    joint_name = model.joint(i).name  # 获取第i个关节的名称
    joint_names.append(joint_name)
    print(f"Joint {i}: {joint_name}")
ctrl_values = np.zeros(joint_count)

# 获取 actuator 控制范围（注意：actuator 不是 joint 本体）
ctrl_ranges = model.actuator_ctrlrange.copy()


# --- MuJoCo 模拟线程 ---
def mujoco_thread():
    with mujoco.viewer.launch_passive(model, data) as viewer:
        print("MuJoCo viewer running...")
        while viewer.is_running():
            data.ctrl[:] = ctrl_values
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(0.01)

def topic_cmd():
    rospy.Subscriber(f"/cb_{hand_type}_hand_control_cmd",JointState,hand_cb,queue_size=10)

def hand_cb(data):
    position = data.position

    if joint_map is not None:
        for map_idx, pose_idx in joint_map.items():
            if pose_idx is not None:
                j_min,j_max = joint_arc[map_idx]
                # 仿真为0张开，而真机是255为张开，这里需要转化
                if hand_joint == "L10":
                    if map_idx == 0 or map_idx == 2 or map_idx == 3 or map_idx == 4 or map_idx == 5:
                        p = position[pose_idx]
                    else:
                        p = (255 - position[pose_idx])
                elif hand_joint == "L20" or hand_joint == "L21":
                    p = (255 - position[pose_idx])
                # 将range值转为arc值
                tmp = map_range_to_joint(p,joint_min=j_min,joint_max=j_max)
                ctrl_values[map_idx] = tmp
                print(tmp)

def map_range_to_joint(r_value, joint_min, joint_max):
    """将  (0-255) 动态映射到  (joint_min, joint_max)"""
    normalized_b = r_value / 255
    return joint_min + normalized_b * (joint_max - joint_min)

# --- GUI 控制窗口 ---
class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joint Controller")
        self.setGeometry(100, 100, 400, 80 + 50 * joint_count)

        layout = QVBoxLayout()
        self.sliders = []
        self.joint_names = joint_names

        for i in range(joint_count):
            min_val, max_val = ctrl_ranges[i]
            label = QLabel(f"{self.joint_names[i]}  [{min_val:.2f}, {max_val:.2f}]")
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(min_val * 100))
            slider.setMaximum(int(max_val * 100))
            slider.setValue(0)

            slider.valueChanged.connect(self.make_slider_callback(i, min_val, max_val))
            layout.addWidget(label)
            layout.addWidget(slider)
            self.sliders.append(slider)

        self.setLayout(layout)

    def make_slider_callback(self, index, min_val, max_val):
        def callback(value):
            # 将 slider 整数值映射为 float 控制值
            ctrl_values[index] = value / 100.0
        return callback


# --- 主函数 ---
if __name__ == "__main__":
    # 启动 MuJoCo 模拟线程
    sim_thread = threading.Thread(target=mujoco_thread)
    sim_thread.start()
    topic_cmd()
    
    # 启动 GUI（主线程）
    # app = QApplication(sys.argv)
    # window = ControlWindow()
    # window.show()
    # sys.exit(app.exec_())


