# LinkerHand灵巧手ROS SDK

## 概述
LinkerHand灵巧手ROS SDK 是灵心巧手(北京)科技有限公司开发，用于L10、L20、L25等LinkerHand灵巧手的驱动软件和功能示例源码。可用于真机与仿真器使用。
LinkerHandROS SDK当前支持Ubuntu20.04 ROS noetic Python3.8环境

## 警告
- 
- 
- 

## 安装
&ensp;&ensp;确保当前系统环境为Ubuntu20.04 ROS为Noetic Python3.8.10版本
- 下载

  ```bash
  $ mkdir -p Linker_Hand_SDK_ROS/src
  $ cd Linker_Hand_SDK_ROS/src
  $ git clone https://github.com/linkerbotai/linker_hand_sdk.git
  ```

- 编译

  ```bash
  $ cd Linker_Hand_SDK_ROS
  $ pip install -r requirements.txt
  $ catkin_make
  ```

## 使用
&ensp;&ensp; __使用前请先将 [setting.yaml](linker_hand_sdk_ros/config/setting.yaml) 配置文件根据实际需求进行相应修改该.__

- 启动SDK&ensp;&ensp;&ensp;&ensp;将linker_hand灵巧手的USB转CAN设备插入Ubuntu设备上
    ```bash
    # 开启CAN端口
    $ sudo /usr/sbin/ip link set can0 up type can bitrate 1000000 #USB转CAN设备蓝色灯常亮状态
    $ cd ~/Linker_Hand_SDK_ROS/
    $ source ./devel/setup.bash
    $ roslaunch linker_hand_sdk_ros linker_hand.launch
    ```

- 启动PyBullet仿真器&ensp;&ensp;&ensp;&ensp;开启一个新终端
    ```bash
    $ cd Linker_Hand_SDK_ROS
    $ source ./devel/setup.bash
    $ rosrun linker_hand_pybullet linker_hand_pybullet.py _hand_type:=L20
    ```


## 相关文档
- #### [Ubuntu设备配置说明文档](doc/hardware_settings.md)
- #### [(examples)示例说明文档](examples/README_CN.md)


<<<<<<< HEAD
## 版本更新
- > ### 1.3.1
  - examples新增LinkerHand灵巧手状态值(弧度与范围)的获取
  - 新增PyBullet仿真环境
  - 新增GUI控制界面
=======

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

索引10：大拇指切向压力方向值 0~255
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
>>>>>>> d684a04d8404e9e758adb15ae3fc86d1ffdbdcc7


## [示例](example/)

&ensp;&ensp; __使用前请先将 [setting.yaml](linker_hand_sdk_ros/config/setting.yaml) 配置文件根据实际需求进行相应修改该.__

- #### [0000-get_linker_hand_state 获取LinkerHand灵巧手当前状态](examples/L20_get_linker_hand_state/)

- ##### [0001-gui_control图形界面控制](example/gui_control/)

- ##### [0002-linker_hand_pybullet仿真器](example/linker_hand_pybullet)

