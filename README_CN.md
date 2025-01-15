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


## 版本更新
- > ### 1.3.1
  - examples新增LinkerHand灵巧手状态值(弧度与范围)的获取
  - 新增PyBullet仿真环境
  - 新增GUI控制界面


## [示例](examples/)

&ensp;&ensp; __使用前请先将 [setting.yaml](linker_hand_sdk_ros/config/setting.yaml) 配置文件根据实际需求进行相应修改该.__

- [0000-linker_hand_pybullet (PyBullet仿真示例)](examples/README_CN.md#0000-PyBullet仿真示例)
- [0001-get_linker_hand_state (获取LinkerHand灵巧手当前状态)](examples/README_CN.md#0001-获取linkerhand灵巧手当前状态状态数值包括范围值与弧度值)
- [0002-gui_control(图形界面控制)](examples/README_CN.md#0002-图形界面控制)
- [0003-get_linker_hand_force (获取LinkerHand灵巧手力传感器数据)](examples/README_CN.md#0003-获取LinkerHand灵巧手力传感器数据)
- [0004-get_linker_hand_speed (获取LinkerHand灵巧手力当前速度)](examples/README_CN.md#0004-获取LinkerHand灵巧手力当前速度)
- [0005-get_linker_hand_current (获取LinkerHand灵巧手力当前电流)](examples/README_CN.md#0005-获取LinkerHand灵巧手力当前电流)
---
- [0101-lipcontroller (触觉传感器配合灵巧手进行捏取操作)](examples/README_CN.md#0101-触觉传感器配合灵巧手进行捏取操作)
- [0102-gesture-Show-OK (使用python控制手比OK动作)](examples/README_CN.md#0102-使用python控制手比OK动作)
- [0103-gesture-Show-Surround-Index-Finger (使用python控制手做旋转食指动作)](examples/README_CN.md#0103-使用python控制手做旋转食指动作)
- [0104-gesture-Show-Wave (使用python控制手做波浪运动)](examples/README_CN.md#0104-使用python控制手做波浪运动)
- [0105-gesture-Show-Ye (使用python控制手做一套复杂的展示动作)](examples/README_CN.md#0105-使用python控制手做一套复杂的展示动作)

