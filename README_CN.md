# 1. **概述**

灵心巧手，创造万物。

LinkerHand 灵巧手 ROS SDK 是由灵心巧手（北京）科技有限公司开发的一款软件工具，用于驱动其灵巧手系列产品，并提供功能示例。它支持多种设备（如笔记本、台式机、树莓派、Jetson 等），主要服务于人型机器人、工业自动化和科研院所等领域，适用于人型机器人、柔性化生产线、具身大模型训练和数据采集等场景。

**警告**

1. 请保持远离灵巧手活动范围，避免造成人身伤害或设备损坏。

2. 执行动作前请务必进行安全评估，以防止发生碰撞。

3. 请保护好灵巧手。

# 2. **版本说明**

V1.3.4

1. 波形图由单手显示改为单/双手配置显示，通过修改该配置文件压感是否存在来控制

2. 解决接近感应波形图数据同行错误

3. 改变关闭CAN口逻辑，避免第二次启动后灵巧手部分传感器数据读取不出来

V1.3.3

1. GUI新增了压力传感器波形图

2. L10支持了设置速度和设置扭矩

V1.3.2

1. 新增了T24版本灵巧手的支持

V1.3.1

1. examples新增LinkerHand灵巧手状态值(弧度与范围)的获取

2. 新增PyBullet仿真环境

3. 新增GUI控制界面

# 3. 准备工作

## 3.1 系统与硬件需求

* 操作系统：Ubuntu20.04

* ROS版本：Noetic

* Python版本：V3.8.10

* 硬件接口：5v标准USB接口

## 3.2 下载

```python
$ mkdir -p Linker_Hand_SDK_ROS/src    #创建目录
$ cd Linker_Hand_SDK_ROS/src    #进入目录
$ git clone https://github.com/linkerbotai/linker_hand_sdk.git    #获取SDK
```

## 3.3 安装依赖与编译

```python
$ cd Linker_Hand_SDK_ROS/src/linker_hand_sdk    #进入目录
$ pip install -r requirements.txt    #安装所需依赖
$ catkin_make    #编译和构建ROS包
```

## 3.4 配置ROS主从通讯

支持分布式计算和模块化开发，只在本终端生效，如不需要则忽略。树莓派设备已默认配置完成。

```shell
$ source /opt/ros/noetic/setup.bash
$ export ROS_MASTER_URI=http://<ROS Master IP>:11311
$ export ROS_IP=<本机IP>
$ export ROS_HOSTNAME=<本机IP>
```

# 4. 使用

## 4.1 修改setting.yaml配置文件

无论是真机运行还是仿真模拟，均需要先修改配置参数文件。

目前，ROS开发的图形界面控制示例，只能单独控制一只LinkerHand灵巧手。

```python
$ cd Linker_Hand_SDK_ROS/src/linker_hand_sdk/linker_hand_sdk_ros/config
$ sudo vim setting.yaml    #编辑配置文件
```

setting.yaml描述

```yaml
VERSION: 1.3.5 # 版本号，L7 O7支持
LINKER_HAND:  # 手部配置信息
  LEFT_HAND:
    EXISTS: True # 是否存在左手，如果不存在，请修改为False
    TOUCH: True  # 是否有压力传感器，如果不存在，请修改为False
    JOINT: L7 # 左手关节数  L7 \ L10 \ L20 \ L25
    NAME: # 无论l10还是l20 joint name都是20个
      - joint41
      - joint42
      - joint43
      - joint44
      - joint45
      - joint46
      - joint47
      - joint48
      - joint49
      - joint50
      - joint51
      - joint52
      - joint53
      - joint54
      - joint55
      - joint56
      - joint57
      - joint58
      - joint59
      - joint60
  RIGHT_HAND:
    EXISTS: False # 是否存在右手
    TOUCH: True # 是否有压力传感器
    JOINT: L10 # 右手关节数量   L7 \ L10 \ L20 \ L25
    NAME:  # 无论l10还是l20 joint name都是20个
      - joint71
      - joint72
      - joint73
      - joint77
      - joint75
      - joint76
      - joint77
      - joint78
      - joint79
      - joint80
      - joint81
      - joint82
      - joint83
      - joint84
      - joint88
      - joint86
      - joint87
      - joint88
      - joint89
      - joint90
PASSWORD: "12345678" # 由于与can通讯，需要激活通讯接口用到系统管理员密码
```

## 4.2 LinkerHand灵巧手与电脑硬件连接

### 4.2.1 将LinkerHand灵巧手的USB转CAN设备接口，插入Ubuntu设备上，蓝灯亮起

![](https://lkaeimso7m.feishu.cn/space/api/box/stream/download/asynccode/?code=YzkzNzI4YmE1MzdmMzMzOGFhNmUyMDQ4YjViMDk0N2JfZGxnTHZMaU9Ec2dqdkZKOERBeTcxU3BScDN1QTdPcXJfVG9rZW46RkNZYWIxNWllb0NlMW94SkR5aGNhcEs0bm9oXzE3NDM1ODU1MDk6MTc0MzU4OTEwOV9WNA)

灯光闪烁：蓝色灯闪烁代表通讯成功。

~~通讯模式：如何通过CAN模块连接的时候，区分是CAN还是485？ CAN接口和485接口完全不同。连接方式也不同 ~~

## 4.3 启动SDK

启动LinkerHand L10、L20灵巧手SDK，启动成功后会有SDK版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。&#x20;

```python
# 开启CAN端口
$ sudo /usr/sbin/ip link set can0 up type can bitrate 1000000 #USB转CAN设备蓝色灯常亮状态
$ cd ~/Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

启动LinkerHand O7灵巧手SDK

```python
# 开启CAN端口
$ sudo /usr/sbin/ip link set can0 up type can bitrate 1000000 #USB转CAN设备蓝色灯常亮状态
$ cd ~/Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand_l7.launch # 启动 O7 灵巧手
```

启动LinkerHand L25灵巧手SDK

```python
# 开启CAN端口
$ sudo /usr/sbin/ip link set can0 up type can bitrate 1000000 #USB转CAN设备蓝色灯常亮状态
$ cd ~/Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand_l25.launch # 启动 L25 灵巧手
```

# 5. **功能包介绍**

## 5.1 linker\_hand\_sdk\_ros

控制灵巧手关节角度、获取灵巧手的各种状态信息。

## 5.2 range\_to\_arc

获取L10、L20的弧度值

## 5.3 examples

包含了各个产品的使用案例

## 5.4 doc

文档附件目录

# 6. ROS开发示例

## 6.1 PyBullet仿真

已支持的LinkerHand灵巧手产品：L10、L20、L25

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动PyBullet仿真

```python
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun linker_hand_pybullet linker_hand_pybullet.py _hand_type:=L20
```

**&#x20;参数说明**

"\_hand\_type"数值，无默认，必须根据产品型号选择，例如：\_hand\_type:=L20

**输出结果示例**

无

## 6.2 **图形界面控制**

已支持的LinkerHand灵巧手产品：L10、L20

图形界面控制可以通过滑动块控制LinkerHand灵巧手L10、L20各个关节独立运动。也可以通过添加按钮记录当前所有滑动块的数值，保存LinkerHand灵巧手当前各个关节运动状态。通过功能性按钮进行动作复现。

使用gui\_control控制LinkerHand灵巧手: gui\_control界面控制灵巧手需要启动linker\_hand\_sdk\_ros，以topic的形式对LinkerHand灵巧手进行操作。

1. 开启一个新终端，启动ROS

```python
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动图形界面控制

```python
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun gui_control gui_control.py
```

开启后会弹出UI界面。通过滑动条可控制相应LinkerHand灵巧手关节运动。并可通过右侧添加按钮对当前滑动条数据进行保存，以便用于复现使用。

**参数说明**

无

**输出结果示例**

无

## 6.3 获取设备状态与信息

### 6.3.1 **获取当前状态**

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，获取当前状态

  1. 针对L20，开启一个新终端，获取当前状态

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun L20_get_linker_hand_state L20_get_linker_hand_state.py _loop:=True
```

**&#x20;参数说明**

状态数值包括：范围值与弧度值。&#x20;

“ \_loop” 参数，需要填写，如果为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值。例如：\_loop:=True

**输出结果示例**

稍后更新

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun L10_get_linker_hand_state L10_get_linker_hand_state.py _loop:=True
```

**&#x20;参数说明**

状态数值包括：范围值与弧度值。&#x20;

“ \_loop” 参数，需要填写，如果为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值。例如：\_loop:=True

**输出结果示例**

```bash
header:
  seq: 83
  stamp:
    secs: 1743409242
    nsecs: 193927526
  frame_id: ''
name: []
position: [1.03, -1.57, 1.3, 1.3, 1.3, 1.3, 0.26, -0.26, -0.26, 1.57]
velocity: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
effort: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```

### 6.3.2 **获取力传感器数据**

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```bash
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，获取力传感器数据

```bash
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun get_linker_hand_force get_linker_hand_force.py _loop:=False
```

**参数说明**

“ \_loop” 参数，需要填写，如果为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值。例如：\_loop:=True

**输出结果示例**

* 右手五指法相力: \[0.0, 0.0, 0.0, 0.0, 0.0] 范围0\~255，压力越大值越大

* 右手五指切向力: \[0.0, 0.0, 0.0, 0.0, 0.0] 范围0\~255，压力越大值越大

* 右手五指切向力方向: \[255.0, 255.0, 255.0, 255.0, 255.0] 范围255\~0，压力越大值越小

* 右手五指接近感应: \[0.0, 0.0, 0.0, 0.0, 0.0] 范围0\~255，压力越大值越大

### 6.3.3 **获取当前速度**

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，获取力当前速度

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun get_linker_hand_speed get_linker_hand_speed.py _loop:=False
```

**参数说明**

“ \_loop” 参数，需要填写，如果为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值。例如：\_loop:=True 参数必带

**输出结果示例**

右手五指速度为: \[180, 250, 250, 250, 250]，顺序：大拇指、食指、中指、无名指、小拇指。

### 6.3.4 **获取当前电流**

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，获取力当前电流

```python
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun get_linker_hand_current get_linker_hand_current.py _loop:=False
```

**参数说明**

“ \_loop” 参数，需要填写，如果为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值。例如：\_loop:=True

**输出结果示例**

右手五指电流为: \[42, 42, 42, 42, 42]，顺序：大拇指、食指、中指、无名指、小拇指。

### 6.3.5 获取故障码

```python
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"get_faults\",\"params\":{\"hand_type\":\"left\"}}"}'
```

**参数说明**

setting\_cmd ：命令参数

get\_faults： 命令类型 string

**输出结果示例**

右手五指电流为: \[0, 1, 0, 0, 0] ，0 代表正常，1代表故障。

## 6.4 设置

### 6.4.1 设置速度

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，设置速度

```python
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun set_linker_hand_speed set_linker_hand_speed.py _hand_type:=left _speed:=[180,250,250,250,250] # L7为7个值，其他为5个值
```

**参数说明**

L10、L20：5个手指统一的速度

speed:=\[180,250,250,250,250]

L7：7个电机速度

speed:=\[180,250,250,250,250,250,250]&#x20;

**输出结果示例**

speed:\[180,250,250,250,250]

### 6.4.2 设置当前电流

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，设置当前电流

```python
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun set_linker_hand_current set_linker_hand_current.py _hand_type:=left _current:=42 #暂不支持L7
```

**参数说明**

参数：hand\_type: left | right 左手还是右手    current:0\~255 设置最大电流值

**输出结果示例**

current:\[180,250,250,250,250]

### 6.4.3 设置扭矩

已支持的LinkerHand灵巧手产品：L10、L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，设置扭矩

```python
$ cd Linker_Hand_SDK_ROS
$ source ./devel/setup.bash
$ rosrun set_linker_hand_torque set_linker_hand_torque.py _hand_type:=left _torque:=[180,250,250,250,250] # L7为7个值，其他为5个值
```

**参数说明**

参数：hand\_type: left | right 左手还是右手    torque:=\[180,250,250,250,250]  0\~255 L7为7个电机最大值，其他为5个手指最大值&#x20;

**输出结果示例**

torque:\[180,250,250,250,250]

### 6.4.4 **设置为失能模式&#x20;**

已支持的LinkerHand灵巧手产品：L25

使灵巧手电机失能，可随意拖动各个关节活动

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand_l25.launch # 启动L25
```

* 开启一个新终端，启动设置为失能模式

```python
$ Linker_Hand_SDK_ROS/src/linker_hand_sdk/examples/L25
$ python set_disability.py
```

**参数说明**

无

**输出结果示例**

无

### 6.4.5 **设置为使能模式**

已支持的LinkerHand灵巧手产品：L25

使灵巧手电机使能，使能后，可用控制程序控制

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand_l25.launch # 启动 L25
```

* 开启一个新终端，启动设置为使能模式

```python
$ Linker_Hand_SDK_ROS/src/linker_hand_sdk/examples/L25
$ python set_enable.py
```

**参数说明**

无

**输出结果示例**

无

### 6.4.6 **设置为遥操模式**

已支持的LinkerHand灵巧手产品：L25

如果拥有多只相同版本L25灵巧手，可使用本示例完成：一只失能的灵巧手控制另一只使能的灵巧手

首先需要启动LinkerHand SDK ROS 以下为被控制L25灵巧手配置方式，以下以右手为例 首先确保两台Ubuntu在同一网络内，并且配置好主从，两台Ubuntu可同时进行ROS通讯，可参考[ROS官方文档](https://wiki.ros.org/)&#x20;

**控制方-A灵巧手配置**

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand_l25.launch # 启动 L25
```

* 开启一个新终端，启动执行遥控

```python
$ Linker_Hand_SDK_ROS/src/linker_hand_sdk/examples/L25
$ python set_remote_control.py
```

**被控制方-B灵巧手配置**

1. 开启一个新终端，启动ROS

```python
# 新开终端 启动ros
$ roscore
```

* 开启一个新终端

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand_l25.launch
```

此时，手动拖拽A机器的失能L25灵巧手即可控制B机器的使能L25灵巧手。

## 6.5 **应用演示**

### 6.5.1 **猜拳游戏**

已支持的LinkerHand灵巧手产品：L10、L20

注：需要有RGB摄像头

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动猜拳游戏

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun finger_guessing finger_guessing.py
```

**参数说明**

无

**输出结果示例**

无

### 6.5.2 **捏取操作**

已支持的LinkerHand灵巧手产品：L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动捏取演示

```python
python ./<你的文件路径>/lipcontroller.py
```

如终端打印出“**开始演示**”即为正常运行，此时手设置如果正确，应开始使用食指和中指进行捏的动作，捏到物品会停止，拿走物品后会继续尝试捏，直到捏到物品或运动到极限。

**lipcontroller.py** 是基于产品O7的第7版进行开发的演示demo，应用在其他版本的演示时，需要调整拇指和食指的对合姿态，否则无法实现“**食指和拇指捏合在一起**”的动作。

**参数说明**

无

**输出结果示例**

无

## 6.6 **模仿学习**

### 6.6.1 **模仿学习训练**

使用本例硬件为LinkerRobot人形机器人，也可以使用其他机械臂或机器人进行模仿学习训练，只要修改该相应数据话题即可， [详细使用说明请参考human-dex项目README.md](https://github.com/linkerbotai/human-dex)

1. 配置环境

```css
cd human-dex
conda create -n human-dex python=3.8.10
conda activate human-dex
pip install torchvision
pip install torch
pip install -r requirements.txt
```

* 安装

```css
mkdir -p your_ws/src
cd your_ws/src
git clone https://github.com/linkerbotai/human-dex.git
cd ..
catkin_make
source ./devel/setup.bash
```

* 运行

```solidity
# 数据采集
 roslaunch record_hdf5 record_hdf5.launch
# 新开终端发送采集命令
rostopic pub /record_hdf5 std_msgs/String "data: '{\"method\":\"start\",\"type\":\"humanplus\"}'"
```

* 训练

```solidity
cd humanplus/scripts/utils/HIT
python3 imitate_episodes_h1_train.py --task_name data_cb_grasp --ckpt_dir cb_grasp/ --policy_class HIT --chunk_size 50 --hidden_dim 512 --batch_size 48 --dim_feedforward 512 --lr 1e-5 --seed 0 --num_steps 100000 --eval_every 1000 --validate_every 1000 --save_every 1000 --no_encoder --backbone resnet18 --same_backbones --use_pos_embd_image 1 --use_pos_embd_action 1 --dec_layers 6 --gpu_id 0 --feature_loss_weight 0.005 --use_mask --data_aug
```

* 复现/评估

```css
cd humanplus/scripts
python3 cb.py
```

**参数说明**

无

**输出结果示例**

无

### 6.6.2 **Unidexgrasp抓取算法**

原Unidexgrasp算法采用shadowhand，以下提供在linkerhand上开发Unidexgrasp算法的相关代码。 [详细过程参考linker\_unidexgrasp项目](https://github.com/linkerbotai/linker_unidexgrasp)

**抓取姿态生成部分**

抓取姿态部分采取映射方案，将模型输出的shadowhand手姿，映射为linkerHand L20手姿态，为后续开发使用。

1. 配置环境

```bash
conda create -n unidexgrasp python=3.8
conda activate unidexgrasp
conda install -y pytorch==1.10.0 torchvision==0.11.0 torchaudio==0.10.0 cudatoolkit=11.3 -c pytorch -c conda-forge
conda install -y https://mirrors.bfsu.edu.cn/anaconda/cloud/pytorch3d/linux-64/pytorch3d-0.6.2-py38_cu113_pyt1100.tar.bz2
pip install -r requirements.txt
cd thirdparty/pytorch_kinematics
pip install -e .
cd ../nflows
pip install -e .
cd ../
git clone https://github.com/wrc042/CSDF.git
cd CSDF
pip install -e .
cd ../../
```

* 训练&#x20;

  1. GraspIPDF

  ```bash
  python ./network/train.py --config-name ipdf_config \
                            --exp-dir ./ipdf_train
  ```

  * GraspGlow

  ```bash
  python ./network/train.py --config-name glow_config \
                            --exp-dir ./glow_train
  python ./network/train.py --config-name glow_joint_config \
                            --exp-dir ./glow_train
  ```

  * ContactNet

  ```bash
  python ./network/train.py --config-name cm_net_config \
                            --exp-dir ./cm_net_train
  ```

* 验证

```bash
python ./network/eval.py  --config-name eval_config \
                          --exp-dir=./eval
```

* 映射，结果可视化

```bash
python ./tests/visualize_result_l20_shadow.py --exp_dir 'eval' --num 3
```

* 保存结果为后续强化学习算法开发使用

```bash
python ./tests/data_for_RL.py
```

# 7. Python开发示例

### 7.1 **手做OK手势**

已支持的LinkerHand灵巧手产品：L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动OK手势

```python
python ./<你的文件路径>/gesture-Show-OK.py
```

开始后终端会打印测试中，此时手会开始做OK手势，并弯曲中指无名指小指和伸直动作。

**参数说明**

无

**输出结果示例**

无

### 7.2 **手做旋转食指动作**

已支持的LinkerHand灵巧手产品：L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动旋转食指动作

```python
python ./<你的文件路径>/gesture-Show-Surround-Index-Finger.py
```

开始后终端会打印测试中，此时手会开始握拳并伸出食指，食指会不断重复旋转。

**参数说明**

无

**输出结果示例**

无

### 7.3 **手做波浪运动**

已支持的LinkerHand灵巧手产品：L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动波浪运动

```python
python ./<你的文件路径>/gesture-Show-Wave.p
```

开始后终端会打印测试中，此时手拇指向外舒展不动，其余四指开始做波浪运动。

**参数说明**

无

**输出结果示例**

无

### 7.4 **手做一套复杂动作**

已支持的LinkerHand灵巧手产品：L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动一套复杂动作

```python
python ./<你的文件路径>/gesture-Show-Ye.py
```

开始后终端会打印测试中，此时手会开始做一套复杂动作来展示手的灵活性。

本例是基于产品O7的第7版进行开发的演示demo，应用在其他版本的演示时，需要调整拇指和食指的对合姿态，否则无法实现“**食指和拇指捏合或对合在一起**”的动作。

**参数说明**

无

**输出结果示例**

无

### 7.5 **手做循环抓握动作**

已支持的LinkerHand灵巧手产品：L20

1. 开启一个新终端，启动ROS

```css
$ roscore
```

* 开启一个新终端，启动Linker Hand ROS SDK

```python
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch # 启动 L10 or L20 灵巧手
```

* 开启一个新终端，启动循环抓握动作

```python
$ cd Linker_Hand_SDK_ROS/src/linker_hand_sdk/examples/gesture-show
$ python gesture-Loop.py 
```

**参数说明**

无

**输出结果示例**

无

### 7.6 手指舞

已支持的LinkerHand灵巧手产品：L25

**参数说明**

无

**输出结果示例**

无

# 8. 相关GitHub资源

Human-Dex：https://github.com/linkerbotai/human-dex

Linker\_UniDexGrasp：https://github.com/linkerbotai/linker\_unidexgrasp

LinkerHand-Python-SDK：https://github.com/linkerbotai/linker\_hand\_python\_sdk

linker\_serl：https://github.com/linkerbotai/linker\_serl

# 9. 常见问题

## 9.1 安装CAN模块驱动

```python
pip install python-can
```

## 9.2 如何无需重复输入密码？

方法一

```python
$ sudo visudo
#添加以下内容
你的用户名 ALL=(ALL) NOPASSWD: /sbin/ip
你的用户名 ALL=(ALL) NOPASSWD: /usr/sbin/ip link set can0 up type $ $ can bitrate 1000000
# 保存退出
```

方法二

修改setting.yaml配置文件的密码，默认PASSWORD："12345678"



#
