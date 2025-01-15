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

(1) 使用gui_control控制LinkerHand灵巧手:
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
![START_SDK](../doc/start_sdk.png) 

启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端启动gui控制
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun gui_control gui_control.py
```
开启后会弹出UI界面。通过滑动条可控制相应LinkerHand灵巧手关节运动。并可通过右侧添加按钮对当前滑动条数据进行保存，以便用于复现使用


