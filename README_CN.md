# linker_hand_sdk_ros 灵心巧手 L10&L20 SDK for ROS Noetic
- linker_hand_sdk_ros V1.2.2
- 环境支持
linker_hand_sdk_ros SDK 支持 ROS Noetic 

灵心巧手L10 & L20 机械手
# 远程连接灵巧手控制板
- 启动脚本
使用ssh连接到控制板linker/pi5
- Windows 10 or 11
```bash
ssh linker@192.168.11.101
# 提示输入密码
# linker@192.168.11.101's password:
# 输入密码
12345678
```
- Linux
```bash
sudo ssh linker@192.168.11.101
# 提示输入密码
# linker@192.168.11.101's password:
# 输入密码
12345678
```
# 使用方法
- 修改配置文件
```bash
cd Linker_Hand_SDK_ROS/src/linker_hand_sdk_ros/config
sudo vim setting.yaml
# 按照文件内说明修改相关配置信息
# 将最下面PASSWORD: "xxxxxx" 参数改为本机sudo用户的密码 以便自动启动can端口调用权限
```

- 将ip命令改为NOPASSWORD模式
```bash
sudo vim /etc/sudoers
#添加以下内容
pi4 ALL=(ALL) NOPASSWD: /sbin/ip
pi4 ALL=(ALL) NOPASSWD: /usr/sbin/ip link set can0 up type can bitrate 1000000
# 保存退出
```

- 编译SDK
```bash
cd Linker_Hand_SDK_ROS/

catkin_make
```
- 启动SKD 注:将IP地址192.168.11.101替换为自己本机IP地址
```bash
source /opt/ros/noetic/setup.bash

export ROS_MASTER_URI=http://192.168.11.101:11311

export ROS_IP=192.168.11.101

export ROS_HOSTNAME=192.168.11.101

cd /home/linker/ROS/Linker_Hand_SDK_ROS

catkin_make

source ./devel/setup.bash

roslaunch linker_hand_sdk_ros linker_hand.launch # 开启后手会有张开动作
```
# 动捕手套遥操方法
- 首先在本机启动ROS2 to ROS1桥接
```bash
# 本机安装好ros2 foxy后，新开终端输入以下命令
source /opt/ros/foxy/setup.bash
export ROS_DOMAIN_ID=11
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
```
- 以上开启后即可收到动捕手套遥操数据 miniPC有接路由器标签网口ip:192.168.11.222  没有标签网口ip:192.168.11.221



## 快速使用
- 灵巧手topic说明
```bash
# 连接到控制板后再终端输入rostopic list即可显示灵巧手相关话题
linker@linker:~$ rostopic list
/cb_hand_setting_cmd # 设置灵巧手相关参数
/cb_left_hand_control_cmd # 控制左手运动
/cb_left_hand_state # 获取左手当前状态
/cb_left_hand_touch # 获取左手压力传感器
/cb_right_hand_control_cmd # 控制右手运动
/cb_right_hand_state # 获取右手当前状态
/cb_right_hand_touch # 获取右手压力传感器
```
- 压力传感器数据说明
```bash
rostopic echo /cb_left_hand_touch
data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 255.0, 255.0, 255.0, 255.0, 255.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```
- 数组格式说明
索引0：大拇指法相压力值 0~255
索引1：食指法相压力值 0~255
索引2：中指法相压力值 0~255
索引3：无名指法相压力值 0~255
索引4：小拇指法相压力值 0~255

索引5：大拇指切向压力值 0~255
索引6：食指切向压力值 0~255
索引7：中指切向压力值 0~255
索引8：无名指切向压力值 0~255
索引9：小拇指切向压力值 0~255

索引10：大拇指切向压力方向值 0~255 # 无压力方向则为255
索引11：食指切向压力方向值 0~255
索引12：中指切向压力方向值 0~255
索引13：无名指切向压力方向值 0~255
索引14：小拇指切向压力方向值 0~255

索引15：大拇指接近感应值 0~255
索引16：食指切接近感应值 0~255
索引17：中指切接近感应值 0~255
索引18：无名指接近感应值 0~255
索引19：小拇指接近感应值 0~255

## L10
- 机械手握拳 数据格式 sensor_msgs/JointState
```bash
# 左手
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [80,80,80,80,80,80,80,80,80,80], velocity: [], effort: []}"
# 右手
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [80,80,80,80,80,80,80,80,80,80], velocity: [], effort: []}"
```

- 机械手张开 数据格式 sensor_msgs/JointState
```bash
# 左手
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [255, 128, 255, 255, 255, 255, 128, 128, 128, 128], velocity: [], effort: []}"
# 右手
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [255, 128, 255, 255, 255, 255, 128, 128, 128, 128], velocity: [], effort: []}"
```
- 设置机械手最大扭矩 数据格式 std_msgs/msg/String
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_max_torque_limits\",\"params\":{\"hand_type\":\"left\",\"torque\":180}}"}'   参数说明：hand_type:left | right
```


## L20

- 机械手握拳 数据格式 sensor_msgs/JointState
```bash
# 左手
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], velocity: [], effort: []}"
# 右手
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], velocity: [], effort: []}"
```

- 机械手张开 数据格式 sensor_msgs/JointState
```bash
# 左手
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255], velocity: [], effort: []}"

rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180], velocity: [], effort: []}"

# 右手
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180], velocity: [], effort: []}"

ros2 topic pub /cb_right_hand_control_cmd sensor_msgs/msg/JointState "{header: {stamp: {sec: $(date +%s), nanosec: 0}, frame_id: ''}, name: [], position: [255,255,255,255,255,255,10,100,180,240,245,255,255,255,255,255,255,255,255,255], velocity: [], effort: []}"

ros2 topic pub /cb_right_hand_control_cmd sensor_msgs/msg/JointState "{header: {stamp: {sec: $(date +%s), nanosec: 0}, frame_id: ''}, name: [], position: [180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180,180], velocity: [], effort: []}"

```



rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [0.49,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], velocity: [], effort: []}"


- 设置机械手最大速度 数据格式 std_msgs/msg/String
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_speed\",\"params\":{\"hand_type\":\"right\",\"speed\":20}}"}'   参数说明：hand_type: left | right  speed:0~255
```

- 设置机械手电流 数据格式 std_msgs/msg/String
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_electric_current\",\"params\":{\"hand_type\":\"left\",\"electric_current\":250}}"}' 参数说明：  hand_type: left | right electric_current:0~255
```

- 清除故障
```bash

rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"clear_faults\",\"params\":{\"hand_type\":\"left\"}}"}'
```




rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [255,255,255,255,255,255,10,100,180,240,245,0,0,0,0,255,255,255,255,255], velocity: [], effort: []}"

# 大拇指摆动弯曲
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [30,255,255,255,255,255,10,100,180,240,10,0,0,0,0,30,255,255,255,255], velocity: [], effort: []}"

# 大拇指无名指对指
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [161.8642382139701, 218.1573760125045, 36.16105276385748, 167.10878438888602, 219.54548115394056, 83.76211173215952, 135.44131861688197, 161.23652644839794, 161.62745699159706, 165.79550042709272, 56.71436640239237, 34.22552064000002, 34.22552064000002, 34.22552064000002, 34.22552064000002, 170.56635487606925, 216.305519751478, 105.05931653691715, 218.02046880932423, 216.50660039474312], velocity: [], effort: []}"


