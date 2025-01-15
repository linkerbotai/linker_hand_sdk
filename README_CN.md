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

- [0000-get_linker_hand_state 获取LinkerHand灵巧手当前状态](examples/README_CN.md#获取linkerhand灵巧手当前状态状态数值包括范围值与弧度值)
- ##### [0001-gui_control图形界面控制](examples/gui_control/)

- ##### [0002-linker_hand_pybullet仿真器](examples/linker_hand_pybullet)

