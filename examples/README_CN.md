# 1. LinkerHand灵巧手示例100
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
(1)获取LinkerHand灵巧手当前状态，状态数值包括范围值与弧度值
新开终端
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
# _loop参数为True则终端循环打印当前LinkerHand灵巧手的状态数值，如果为False则终端只打印一次当前LinkerHand灵巧手状态数值
$ rosrun L20_get_linker_hand_state L20_get_linker_hand_state.py _loop:=True
```


# 2. 图形界面控制
图形界面控制可以通过滑动块控制LinkerHand灵巧手L10、L20各个关节独立运动。也可以通过添加按钮记录当前所有滑动块的数值，保存LinkerHand灵巧手当前各个关节运动状态。通过功能性按钮进行动作复现。    

(1) 修改配置文件,针对LinkerHand灵巧手实物进行配置:
```bash
$ cd Linker_Hand_SDK_ROS/src/linker_hand_sdk/linker_hand_sdk_ros/config
$ sudo vim setting.yaml
```
![SETTING](../../doc/setting.png) 
由于图形界面只能单独控制一只LinkerHand灵巧手。需要在配置文件中进行相应配置需与LinkerHand灵巧手实物匹配

(2) 使用gui_control控制LinkerHand灵巧手:
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
![START_SDK](../../doc/start_sdk.png) 
启动成功后会有sdk版本、CAN接口状态、灵巧手配置信息和当前灵巧手关节速度等提示信息。
新开终端启动gui控制
```bash
$ cd Linker_Hand_SDK_ROS/
$ source ./devel/setup.bash
$ rosrun gui_control gui_control.py
```
开启后会弹出UI界面。通过滑动条可控制相应LinkerHand灵巧手关节运动。并可通过右侧添加按钮对当前滑动条数据进行保存，以便用于复现使用
# 2. Servo_Cartesian (streamed Cartesian trajectory)

**PLEASE NOTE:** If you are already using **Moveit** to control the real robot arm, move_servoj and move_servo_cart **can not be used concurrently**, since they use the same mode(1) to control and may interfere with each other!  

Now with xArm controller **Firmware Version >= 1.4.1**, user can send streamed Cartesian poses to continuously control the xArm, through ros service, this is a wrap of the same xarm sdk(api) function. The actual speed depends on the sending frequency and step distance. Users are encouraged to send the path points in a fixed frequency(20Hz~100Hz) and step distance(**MUST** <10mm).   
(1) To start, bring up the xarm server. [use xArm 7 as example]
```bash
$  roslaunch xarm_bringup xarm7_server.launch robot_ip:=192.168.1.233
```
(2) In another terminal, do initial configurations, servo cartesian has to operate in **Mode 1**:
```bash
$ rosservice call /xarm/motion_ctrl 8 1
$ rosservice call /xarm/set_mode 1
$ rosservice call /xarm/set_state 0
```
(3) Call the servo_cartesian service. Please note:  
**(1) the Cartesian pose representation is the same with xarm SDK here. which is [X(mm), Y(mm), Z(mm), Roll(rad), Pitch(rad), Yaw(rad)]**  
**(2) the path must start from current tool center point(TCP) position and the command can not be too far away, or the execution will fail or act strange. PLEASE CHECK the correctness of command before sending it.**  
**(3) service argument format is like: "pose: [214, 0, 121, 3.1416, 0, 0]	mvvelo: 0.0	mvacc: 0.0	mvtime: 0.0	mvradii: 0.0"**    
**(4) For Base Coordinate motion, the arguments mvvelo, mvacc, mvtime, and mvradii are not effective now, so just give them all 0.**  
  
Suppose current TCP position is at [206, 0, 121, 3.1416, 0, 0]
```bash
$ rosservice call /xarm/move_servo_cart [210,0,121,3.1416,0,0] 0.0 0.0 0.0 0.0
```
Now please check the current TCP position, it will execute this target immediately if success. If you want continuous motion alone X axis, you can give the following pose like:
```bash
$ rosservice call /xarm/move_servo_cart [214,0,121,3.1416,0,0] 0.0 0.0 0.0 0.0
```
And you can program this service calling procedure in a loop with proper intervals inbetween, the final execution will become smooth.   

**Notice: Servo_cartisian in TOOL coordinate:**
Please update the controller Firmware to version >= 1.5.0. If servo_cartesian in Tool Coordinate is needed, **put 1 to the previous "mvtime" argument**, the resulted motion will base on current Tool coordinate. For example:  
```bash
$ rosservice call /xarm/move_servo_cart [0,0,2,0,0,0] 0.0 0.0 1 0.0
```
This will make tool to move 2 mm immediately along +Z Axis in **TOOL Coordinate**.  
There is also **example code** implementing continuous servo_cartesian() in tool coordinate: [c++ version](../xarm_api/test/servo_cartesian_test.cpp) and [python version](../xarm_api/scripts/servo_cartesian_test.py).


# 3. Servo_Joint (streamed joint-space trajectory)
There is also a similar service called "**/xarm/move_servoj**", you can use this service to control joint motion in the **same mode (1)** with Servo_Cartesian. It receives **absolute** joint positions as command.  Before calling it, please check the current joint position in "/xarm/joint_states" topic, and increase the target joint position **little by little** just like calling /xarm/move_servo_cart.

For example, if /xarm/joint_state says current joint positions are:  [0.25,-0.47,0.0,-0.28,0.0,0.76,0.24], you can call:  
```bash
$ rosservice call /xarm/move_servoj [0.25,-0.47,0.0,-0.28,0.0,0.76,0.25] 0.0 0.0 0.0 0.0
```
Which will move joint7 by 0.01 rad **immediately**. Keep calling it and increase the joint positions a small step each time, it will move smoothly. **Be careful not to give a target too far away in one single update**.  

# 4. Dual xArm6 controlled with one moveGroup node:
Unlike example 1, This example will bring up only one Rviz and move_group node to control 2 xArm6 arms, which can be used for a dual-arm application.  
To launch the application, run the following with your correct xArm controller IP addresses: 
```bash
$ roslaunch dual_xarm6_moveit_config realMove_exec.launch robot_ip_1:=192.168.1.xxx robot_ip_2:=192.168.1.xxx
```  
![DUAL_CONFIG](../doc/dual_config.png) 
If successfully launched, you will see two xArm6 separated by 1 meter, their relative position to each other can be re-configured in /xarm_description/urdf/dual_xarm6_robot.urdf.xacro, just edit the "xyz" and "rpy" values. You may also add your base to hold the two arms.  

For example, to make the two arms stand face-to-face:  
![URDF_EDIT](../doc/urdf_edit.png) 

1. After Modification to the correct configuration, please run moveit_setup_assistant again to update the collision matrix.
```bash
$ roslaunch moveit_setup_assistant setup_assistant.launch 
```  
2. Click "Edit Existing Moveit Configuration Package" and browse to navigate to the location of "dual_xarm6_moveit_config" package:    
![SETUP1](../doc/setup1.png) 

3. Then click "Load Files". You can see the robot location has already been changed face-to-face.   
![SETUP2](../doc/setup2.png) 

4. Go to first tag "Self-Collisions" and click on "Generate Collision Matrix" to update the Self-collision information.  
![SETUP3](../doc/setup3.png) 

5. Then **Skip the rest and go straight to the last tag** "Configuration files", since other settings are already taken care of and can not be over-written. Watch out for the choices! **ONLY** leave the "config/","config/xarm6.srdf", "launch/" and ".setup_assistant" checked, and others unchecked! Such that only the collision matrix will be updated this time. **If other files checked and overwritten by setup assistant, driving of the real arms may be affected**.
![SETUP4](../doc/setup4.png) 

6. Make sure the above step is correct and click "Generate Package" and "OK" if asked for confirmation. Then the reconfiguration of your own dual-arm is done. 
![SETUP5](../doc/setup5.png) 

7. You can first check in simulation by: 
```bash
$ roslaunch dual_xarm6_moveit_config demo.launch
```
![CHECK_DEMO](../doc/check_demo.png) 

8. If everything looks OK, you can move on to control the real dual-arm:
```bash
$ roslaunch dual_xarm6_moveit_config realMove_exec.launch robot_ip_1:=192.168.1.xxx robot_ip_2:=192.168.1.xxx
```  

# 5. Run Recorded Trajectory (Beta):
To record a new trajectory (no longer than 5 min):
```bash
$ rosservice call /xarm/set_state 0 (DO NOT set STOP state(4) during recording or saving process)

$ rosservice call /xarm/set_recording  1 (to start recording trajectory)
...
$ rosservice call /xarm/set_recording  0 (to finish recording trajectory)

$ rosservice call /xarm/save_traj 'my_recording.traj' (give your desired name with the suffix '.traj')
```   
To run a saved trajectory:
```bash
$ rosservice call /xarm/set_mode 0
$ rosservice call /xarm/set_state 0
$ rosservice call /xarm/play_traj 'my_recording.traj' 1 (repeat times)  1 (speed-up factor: 1x,2x or 4x speed)
``` 

# 6. Online Target Update:
To satisfy the need for **dynamic following task**, we now provide alternative methods other than servo_joint and servo_cartesian which require high-frequency update and trajectroy planning capability at user level. Now xArm controller (after firmware **v1.11.0**) supports Online Trajectory Generation (**OTG**) for both joint space and Cartesian space. The newly genated target from sensors can be sent to the arm even when previous trajectory is not finished, upon receiving the new target, xArm will automatically move towards the latest command point(with newly specified speed and acceleration) in a smooth transition.   

1.For joint space, simply switch to **Mode 6** and give the latest joint targets whenever switching needed, the command service is still `move_joint`.

```bash
# for xArm7:
$ rosservice call /xarm/set_mode 6
$ rosservice call /xarm/set_state 0
$ rosservice call /xarm/move_joint [0,0,0,0,0,0,0] 0.2 7 0 0
# after a certain period while the last target has not been reached
$ rosservice call /xarm/move_joint [-0.2775,-0.55,-0.452,1.05,-0.23,1.55,-0.665] 0.35 10 0 0
```  
2.For Cartesian space, switch to **Mode 7** and then update the latest Cartesian target as needed, with the `move_line` service used in mode 0.

```bash
$ rosservice call /xarm/set_mode 7
$ rosservice call /xarm/set_state 0
$ rosservice call /xarm/move_line [250,100,300,3.14,0,0] 100 2000 0 0
# after a certain period while the last target has not been reached
$ rosservice call /xarm/move_line [250,-100,400,3.14,0,0] 200 5000 0 0
```  
For both modes the speed is continuous at command transition, acceleration is continuous for joint space but not for Cartesian space. Refer to [this paper](https://www-cs.stanford.edu/group/manips/publications/pdfs/Kroeger_2010_TRO.pdf) which categorize OTG methods, our joint OTG is **type IV** and Cartesian OTG is **type II**.