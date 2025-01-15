# LinkerHand灵巧手ROS SDK在台式机(笔记本)树莓派或Jetson等设备上使用

## 说明
LinkerHand灵巧手硬件和ROS SDK软件可使用在x86和arm64的大部分设备上。
- __硬件设备系统必须为Ubuntu20.04 ROS Noetic Python3.8__
- __硬件设备必须拥有5v标准USB接口__ 


## 使用方法
&ensp;&ensp; __使用前请先将 [setting.yaml](../linker_hand_sdk_ros/config/setting.yaml) 配置文件根据实际需求进行相应修改该.__

&ensp;&ensp;__将linker_hand灵巧手的USB转CAN设备插入Ubuntu设备上__

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
- 将ip命令改为NOPASSWORD模式
    ```bash
    $ sudo visudo
    #添加以下内容
    你的用户名 ALL=(ALL) NOPASSWD: /sbin/ip
    你的用户名 ALL=(ALL) NOPASSWD: /usr/sbin/ip link set can0 up type $ $ can bitrate 1000000
    # 保存退出
    ```
- 配置ROS主从，只在本终端生效。如不需要ROS主从通讯则忽略
    ```bash
    $ source /opt/ros/noetic/setup.bash

    $ export ROS_MASTER_URI=http://<ROS Master IP>:11311

    $ export ROS_IP=<本机IP>

    $ export ROS_HOSTNAME=<本机IP>
    ```
- 启动SDK
    ```bash
    # 开启CAN端口
    $ sudo /usr/sbin/ip link set can0 up type can bitrate 1000000 #USB转CAN设备蓝色灯常亮状态
    $ cd ~/Linker_Hand_SDK_ROS/
    $ source ./devel/setup.bash
    $ roslaunch linker_hand_sdk_ros linker_hand.launch
    ```
## 动捕手套遥操方法
- 首先在本机启动ROS2 to ROS1桥接
    ```bash
    # 本机安装好ros2 foxy后，新开终端输入以下命令
    $ source /opt/ros/foxy/setup.bash
    $ export ROS_DOMAIN_ID=11
    $ ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
    ```
- 以上开启后即可收到动捕手套遥操数据 miniPC有接路由器标签网口ip:192.168.11.222  没有标签网口ip:192.168.11.221



