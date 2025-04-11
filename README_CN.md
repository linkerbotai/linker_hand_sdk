# LinkerHand灵巧手ROS SDK

## 概述
LinkerHand灵巧手ROS SDK 是灵心巧手(北京)科技有限公司开发，用于L10、L20、T24等LinkerHand灵巧手的驱动软件和功能示例源码。可用于真机与仿真器使用。
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
  $ cd Linker_Hand_SDK_ROS/src/linker_hand_sdk
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
    # linker_hand.launch支持L10和L20，linker_hand_l25.launch支持L25版本灵巧手,linker_hand_l7.launch支持L7版本灵巧手
    $ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动L10 or L20 灵巧手
    $ # roslaunch linker_hand_sdk_ros linker_hand_l7.launch # 启动L7 灵巧手
    $ # roslaunch linker_hand_sdk_ros linker_hand_l25.launch # 启动L25 灵巧手
    ```

- 启动PyBullet仿真器&ensp;&ensp;&ensp;&ensp;开启一个新终端
    ```bash
    $ cd Linker_Hand_SDK_ROS
    $ source ./devel/setup.bash
    $ rosrun linker_hand_pybullet linker_hand_pybullet.py _hand_type:=L20
    ```
- position与手指关节对照表
  ```bash
  $ rostopic echo /cb_left_hand_control_cmd
  ```
  ---
  header: 
    seq: 256
    stamp: 
      secs: 1744343699
      nsecs: 232647418
    frame_id: ''
  name: []
  position: [155.0, 162.0, 176.0, 125.0, 255.0, 255.0, 180.0, 179.0, 181.0, 68.0]
  velocity: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  effort: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  ---
  L7:  ["大拇指弯曲", "大拇指横摆","食指弯曲", "中指弯曲", "无名指弯曲","小拇指弯曲","拇指旋转"]

  L10: ["拇指根部", "拇指侧摆","食指根部", "中指根部", "无名指根部","小指根部","食指侧摆","无名指侧摆","小指侧摆","拇指旋转"]

  L20: ["拇指根部", "食指根部", "中指根部", "无名指根部","小指根部","拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","小指侧摆","拇指横摆","预留","预留","预留","预留","拇指尖部","食指末端","中指末端","无名指末端","小指末端"]

  L25: ["大拇指根部", "食指根部", "中指根部","无名指根部","小拇指根部","大拇指侧摆","食指侧摆","中指侧摆","无名指侧摆","小拇指侧摆","大拇指横滚","预留","预留","预留","预留","大拇指中部","食指中部","中指中部","无名指中部","小拇指中部","大拇指指尖","食指指尖","中指指尖","无名指指尖","小拇指指尖"]

## 相关文档
- #### [Ubuntu设备配置说明文档](doc/hardware_settings.md)
- #### [(examples)示例说明文档](examples/README_CN.md)


## 版本更新
- > ### release_1.3.4
  - 1、波形图由单手显示改为单/双手配置显示，通过修改该配置文件压感是否存在来控制
  - 2、解决接近感应波形图数据同行错误
  - 3、改变关闭CAN口逻辑，避免第二次启动后灵巧手部分传感器数据读取不出来
  
- > ### 1.3.3
  - GUI新增了压力传感器波形图
  - L10支持了设置速度和设置扭矩
- > ### 1.3.2
  - 新增了T24版本灵巧手的支持

- > ### 1.3.1
  - examples新增LinkerHand灵巧手状态值(弧度与范围)的获取
  - 新增PyBullet仿真环境
  - 新增GUI控制界面


## [示例](examples/)

&ensp;&ensp; __使用前请先将 [setting.yaml](linker_hand_sdk_ros/config/setting.yaml) 配置文件根据实际需求进行相应修改后启动SDK__
# L10/L20/L7

- [0000-linker_hand_pybullet (PyBullet仿真示例)](examples/README_CN.md#0000-PyBullet仿真示例) # 暂不支持L7
```bash
# 0000 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun linker_hand_pybullet linker_hand_pybullet.py
```

- [0001-get_linker_hand_state (获取LinkerHand灵巧手当前状态)](examples/README_CN.md#0001-获取linkerhand灵巧手当前状态状态数值包括范围值与弧度值) # 暂不支持L7

- [0002-gui_control(图形界面控制)](examples/README_CN.md#0002-图形界面控制)
```bash
# 0002 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun gui_control gui_control.py
```
- [0003-get_linker_hand_force (获取LinkerHand灵巧手力传感器数据)](examples/README_CN.md#0003-获取LinkerHand灵巧手力传感器数据)
```bash
# 0003 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun get_linker_hand_force get_linker_hand_force.py
```
- [0004-get_linker_hand_speed (获取LinkerHand灵巧手当前速度)](examples/README_CN.md#0004-获取LinkerHand灵巧手当前速度)
```bash
# 0004 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun get_linker_hand_speed get_linker_hand_speed.py
```
- [0005-get_linker_hand_current (获取LinkerHand灵巧手当前电流)](examples/README_CN.md#0005-获取LinkerHand灵巧手当前电流)
```bash
# 0005 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun get_linker_hand_current get_linker_hand_current.py
```
- [0006-set_linker_hand_speed (设置LinkerHand灵巧手速度)](examples/README_CN.md#0006-设置LinkerHand灵巧手当前速度)
```bash
# 0006 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun set_linker_hand_speed set_linker_hand_speed.py _hand_type:=left _speed:=[180,250,250,250,250] # L7为7个值，其他为5个值
```
- [0007-set_linker_hand_current (设置LinkerHand灵巧手当前电流)](examples/README_CN.md#0007-设置LinkerHand灵巧手当前电流) # 暂不支持L7
```bash
# 0007 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun set_linker_hand_current set_linker_hand_current.py _hand_type:=left _current:=42 #暂不支持L7
```
- [0008-set_linker_hand_torque (设置LinkerHand灵巧手扭矩)](examples/README_CN.md#0008-设置LinkerHand灵巧手扭矩)
```bash
# 0007 SDK启动后新开终端执行
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun set_linker_hand_torque set_linker_hand_torque.py _hand_type:=left _torque:=[180,250,250,250,250] # L7为7个值，其他为5个值
```
- [0009-finger_guessing (互动示例，猜拳游戏)](examples/README_CN.md#0009-互动示例，猜拳游戏) 注:需要有RGB摄像头 # 暂不支持L7
---
- [0101-lipcontroller (触觉传感器配合灵巧手进行捏取操作)](examples/README_CN.md#0101-触觉传感器配合灵巧手进行捏取操作)
- [0102-gesture-Show-OK (使用python控制手比OK动作)](examples/README_CN.md#0102-使用python控制手比OK动作)
- [0103-gesture-Show-Surround-Index-Finger (使用python控制手做旋转食指动作)](examples/README_CN.md#0103-使用python控制手做旋转食指动作)
- [0104-gesture-Show-Wave (使用python控制手做波浪运动)](examples/README_CN.md#0104-使用python控制手做波浪运动)
- [0105-gesture-Show-Ye (使用python控制手做一套复杂的展示动作)](examples/README_CN.md#0105-使用python控制手做一套复杂的展示动作)
- [0106-gesture-Loop (使用python控制手循环抓握动作)](examples/README_CN.md#0106-使用python控制手循环抓握动作)
- [0107-action_group_l25 (使用python控制L25手指舞)](examples/README_CN.md#0107-使用python控制L25手指舞)
- [0108-action-group-show-ti (使用python控制L7手指舞)](examples/README_CN.md#0107-使用python控制L7手指舞)
---
# L25
- [0200-linker_hand_pybullet (PyBullet仿真示例)](examples/README_CN.md#0000-PyBullet仿真示例)
- [0201-set_disability (设置L25灵巧手为失能模式)](examples/README_CN.md#0201-设置L25灵巧手为失能模式)
- [0202-set_enable (设置L25灵巧手为使能模式)](examples/README_CN.md#0202-设置L25灵巧手为使能模式)
- [0203-set_remote_control (设置L25灵巧手为遥操模式)](examples/README_CN.md#0203-设置L25灵巧手为遥操模式)

---
- [1001-human-dex (使用LinkerHand灵巧手进行模仿学习训练并且实现自主抓取物品)](https://github.com/linkerbotai/human-dex)
- [1002-linker_unidexgrasp (基于LinkerHand的Unidexgrasp灵巧手抓取算法)](https://github.com/linkerbotai/linker_unidexgrasp)

## [TOPIC_CMD] # 通过topic pub 相关命令 注: 发送命令后，会在SDK终端打印相关信息
- 获取当前灵巧手电机故障码
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"get_faults\",\"params\":{\"hand_type\":\"left\"}}"}'
```