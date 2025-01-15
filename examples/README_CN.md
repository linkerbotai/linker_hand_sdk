# LinkerHandROS SDK源码目录
<!-- TOC --> 
[examples (示例)](#)
- [0001-get_linker_hand_state (获取LinkerHand灵巧手当前状态)](L20_get_linker_hand_state/)
- [0002-gui_control(图形界面控制)](gui_control/)
- [0003-get_linker_hand_force (获取LinkerHand灵巧手力传感器数据)](get_linker_hand_force/)
- [0004-get_linker_hand_speed (获取LinkerHand灵巧手力当前速度)](get_linker_hand_speed/)
- [0005-get_linker_hand_current (获取LinkerHand灵巧手力当前电流)](get_linker_hand_current)
---
- [0101-lipcontroller (触觉传感器配合灵巧手进行捏取操作)](gesture-show/lipcontroller.py)
- [0102-gesture-Show-OK (使用python控制手比OK动作)](gesture-show/gesture-Show-OK.py)
- [0103-gesture-Show-Surround-Index-Finger (使用python控制手做旋转食指动作)](gesture-show/gesture-Show-Surround-Index-Finger.py)
- [0104-gesture-Show-Wave (使用python控制手做波浪运动)](gesture-show/gesture-Show-Wave.py)
- [0105-gesture-Show-Ye (使用python控制手做一套复杂的展示动作)](gesture-show/gesture-Show-Ye.py)


## LinkerHand灵巧手配置文件说明
LinkerHand灵巧手无论是真机还是仿真，均需要先配置参数文件。根据实际需求修改相应配置参数。

(1) 修改配置文件,针对LinkerHand灵巧手实物或仿真环境进行配置:
```bash
$ cd Linker_Hand_SDK_ROS/src/linker_hand_sdk/linker_hand_sdk_ros/config
$ sudo vim setting.yaml
```
![SETTING](../doc/setting.png) 


由于图形界面只能单独控制一只LinkerHand灵巧手。需要在配置文件中进行相应配置需与LinkerHand灵巧手实物匹配


## LinkerHand灵巧手示例100
LinkerHand灵巧是示例100，提供了丰富的实例案例与源码。充分展示了LinkerHand灵巧手的功能
- 准备
启动SDK
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
- #### 0001-获取LinkerHand灵巧手当前状态，状态数值包括范围值与弧度值
新开终端
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
# _loop参数为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值
$ rosrun L20_get_linker_hand_state L20_get_linker_hand_state.py _loop:=True
```
![STATE](../doc/state.png)


- #### 0002-图形界面控制
图形界面控制可以通过滑动块控制LinkerHand灵巧手L10、L20各个关节独立运动。也可以通过添加按钮记录当前所有滑动块的数值，保存LinkerHand灵巧手当前各个关节运动状态。通过功能性按钮进行动作复现。    

使用gui_control控制LinkerHand灵巧手:
gui_control界面控制灵巧手需要启动linker_hand_sdk_ros，以topic的形式对LinkerHand灵巧手进行操作
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
#![START_SDK](../doc/start_sdk.png) 

启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端启动gui控制
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun gui_control gui_control.py
```
开启后会弹出UI界面。通过滑动条可控制相应LinkerHand灵巧手关节运动。并可通过右侧添加按钮对当前滑动条数据进行保存，以便用于复现使用


- #### 0003-获取LinkerHand灵巧手力传感器数据
新开终端
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
# _loop参数为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值
$ rosrun get_linker_hand_force get_linker_hand_force.py _loop:=False
#2025-01-15 15:43:16  左手没有数据
#2025-01-15 15:43:16  右手五指法相力: [0.0, 0.0, 0.0, 0.0, 0.0]
#2025-01-15 15:43:16  右手五指切向力: [0.0, 0.0, 0.0, 0.0, 0.0]
#2025-01-15 15:43:16  右手五指切向力方向: [255.0, 255.0, 255.0, 255.0, 255.0]
#2025-01-15 15:43:16  右手五指接近感应: [0.0, 0.0, 0.0, 0.0, 0.0]
```

- #### 0004-获取LinkerHand灵巧手力当前速度
新开终端
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
# _loop参数为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值
$ rosrun get_linker_hand_speed get_linker_hand_speed.py _loop:=False
#2025-01-15 15:57:17  左手没有数据
#2025-01-15 15:57:17  当前右手五指速度为: [180, 250, 250, 250, 250]
```


- #### 0005-获取LinkerHand灵巧手力当前电流
新开终端
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
# _loop参数为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值
$ rosrun get_linker_hand_current get_linker_hand_current.py _loop:=False
#2025-01-15 16:25:29  左手没有数据
#2025-01-15 16:25:29  当前右手五指电流为: [42, 42, 42, 42, 42]
```
---

- #### 0101-触觉传感器配合灵巧手进行捏取操作
使用本例需要启动linker_hand_sdk_ros
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
![START_SDK](../doc/start_sdk.png) 
启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端来使用演示例子
```bash
python ./<你的文件路径>/lipcontroller.py
```
![开始演示](../doc/开始演示.png)
- 如终端打印出“__开始演示__”即为正常运行，此时手设置如果正确，应开始使用食指和中指进行捏的动作，捏到物品会停止，拿走物品后会继续尝试捏，直到捏到物品或运动到极限，极限状态如下图
![极限位置](../doc/极限位置.png)

-  __lipcontroller.py__ 是基于7版手进行开发的演示demo，应用在其他版本的演示时，需要调整拇指和食指的对合姿态，否则无法实现“__食指和拇指捏合在一起__”的动作

- #### 0102-使用python控制手比OK动作
使用本例需要启动linker_hand_sdk_ros
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
![START_SDK](../doc/start_sdk.png) 
启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端来使用演示例子
```bash
python ./<你的文件路径>/gesture-Show-OK.py
#开始后终端会打印测试中，此时手会开始做OK的手势，并弯曲中指无名指小指和伸直动作
```

- #### 0103-使用python控制手做旋转食指动作
使用本例需要启动linker_hand_sdk_ros
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
![START_SDK](../doc/start_sdk.png) 
启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端来使用演示例子
```bash
python ./<你的文件路径>/gesture-Show-Surround-Index-Finger.py
#开始后终端会打印测试中，此时手会开始握拳并伸出食指，食指会不断重复旋转
```

- #### 0104-使用python控制手做波浪运动
使用本例需要启动linker_hand_sdk_ros
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
![START_SDK](../doc/start_sdk.png) 
启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端来使用演示例子
```bash
python ./<你的文件路径>/gesture-Show-Wave.py
#开始后终端会打印测试中，此时手拇指向外舒展不动，其余四指开始做波浪运动
```

- #### 0105-使用python控制手做一套复杂的展示动作
使用本例需要启动linker_hand_sdk_ros
```bash
# 新开终端 启动ros
$ roscore
```
新开终端启动ROS SDK
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ roslaunch linker_hand_sdk_ros linker_hand.launch
```
![START_SDK](../doc/start_sdk.png) 
启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端来使用演示例子
```bash
python ./<你的文件路径>/gesture-Show-Ye.py
#开始后终端会打印测试中，此时手会开始做一套复杂的动作来展示手的灵活性
```
-本例是基于7版手进行开发的演示demo，应用在其他版本的演示时，需要调整拇指和食指的对合姿态，否则无法实现“__食指和拇指捏合或对合在一起__”的动作

