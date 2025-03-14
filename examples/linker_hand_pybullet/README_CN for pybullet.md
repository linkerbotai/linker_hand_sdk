# 启动pybullet仿真环境

- 安装环境依赖
```bash
cd Linker_Hand_SDK_ROS/
pip3 install -r requirements.txt
```

- 启动L20/L10 Sim
```bash
# hand:=L20/L10 当前支持 L20 L10
rosrun linker_hand_pybullet linker_hand_pybullet.py _hand_type:=L20
```

 # 使用
 - 左手张开
 ```bash
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255], velocity: [], effort: []}"
 ```
 - 右手张开
 ```bash
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255], velocity: [], effort: []}"
 ```