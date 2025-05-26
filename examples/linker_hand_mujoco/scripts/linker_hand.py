#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
import sys,os,rospy
import threading
import numpy as np
import mujoco, time
import mujoco.viewer
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
# hand_type = rospy.get_param('~hand_type', "right")
# hand_joint = rospy.get_param('~hand_joint', "L10")
# XML_PATH = os.path.dirname(os.path.abspath(__file__))+"/urdf/linker_hand_l7_left/linkerhand_o7_left.xml"
# if hand_type == "left":
#     if hand_joint == "L10":
#         # 左手 L10
#         XML_PATH = os.path.dirname(os.path.abspath(__file__))+"/urdf/linker_hand_l10_left/linker_hand_l10_left.xml"
#         # L7_XML_PATH = os.path.dirname(os.path.abspath(__file__))+"/urdf/linker_hand_l7_left/linkerhand_o7_left.xml"
#         pass
#     elif hand_joint == "L7":
#         # 左手 L7
#         XML_PATH = os.path.dirname(os.path.abspath(__file__))+"/urdf/linker_hand_l7_left/linkerhand_o7_left.xml"
# XML_PATH = os.path.dirname(os.path.abspath(__file__))+"/urdf/linker_hand_l10_left/linker_hand_l10_left.xml"
XML_PATH = os.path.dirname(os.path.abspath(__file__))+"/urdf/linker_hand_l7_left/linkerhand_o7_left.xml"



# --- 加载模型 ---
model = mujoco.MjModel.from_xml_path(XML_PATH)
data = mujoco.MjData(model)
data.qpos[:] = 0
data.qvel[:] = 0
model.opt.disableflags = 1
mujoco.mj_forward(model, data)

joint_count = model.nu
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
            #time.sleep(0.01)


# --- GUI 控制窗口 ---
class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Joint Controller")
        self.setGeometry(100, 100, 400, 80 + 50 * joint_count)

        layout = QVBoxLayout()
        self.sliders = []
        self.joint_names = [
            "thumb_joint0",
            "thumb_joint1",
            "thumb_joint2",
            "thumb_joint3",
            "thumb_joint4",
            "index_joint0",
            "index_joint1",
            "index_joint2",
            "index_joint3",
            "middle_joint0",
            "middle_joint1",
            "middle_joint2",
            "middle_joint3",
            "ring_joint0",
            "ring_joint1",
            "ring_joint2",
            "ring_joint3",
            "little_joint0",
            "little_joint1",
            "little_joint2",
            "little_joint3"
        ]

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

    # 启动 GUI（主线程）
    app = QApplication(sys.argv)
    window = ControlWindow()
    window.show()
    sys.exit(app.exec_())


