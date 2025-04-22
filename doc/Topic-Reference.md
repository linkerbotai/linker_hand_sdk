
---

# Linker Hand ROS SDK Topic Documentation

## Topic Overview

This document provides a detailed overview of the ROS Topic for the Linker Hand, including functions for controlling the hand's movements, retrieving sensor data, and setting operational parameters.

## Topic List
```bash
/cb_hand_setting_cmd # 设置linkerhand命令话题
/cb_left_hand_control_cmd # 控制左手运动话题 by range 0~255 (范围)
/cb_left_hand_control_cmd_arc # 控制左手运动话题 by arc -3.14~3.14 (弧度)
/cb_left_hand_force # 左手压感数据显示话题
/cb_left_hand_info  # 左手配置信息显示话题
/cb_left_hand_state # 左手状态显示话题 范围
/cb_left_hand_state_arc # 左手状态显示话题 弧度
/cb_right_hand_control_cmd # 控制右手运动话题 by range 0~255 (范围)
/cb_right_hand_control_cmd_arc # 控制右手运动话题 by arc -3.14~3.14 (弧度)
/cb_right_hand_force # 右手压感数据显示话题
/cb_right_hand_info # 右手配置信息显示话题
/cb_right_hand_state # 右手状态显示话题 范围
/cb_right_hand_state_arc # 右手状态显示话题 弧度
```

### 设置Topic /cb_hand_setting_cmd

### 设置最大扭矩
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_max_torque_limits\",\"params\":{\"hand_type\":\"right\",\"torque\":180}}"}'
```
**Description**: 
设置机械手最大扭矩 数据格式 std_msgs/msg/String
**Parameters**:
- `hand_type`: left or right 
- `torque`: int or list(int) 长度5  值范围0~255

---

### 设置速度
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_speed\",\"params\":{\"hand_type\":\"right\",\"speed\":200}}"}'
```
**Description**: 
设置机械手最大速度 数据格式 std_msgs/msg/String
**Parameters**:
- `hand_type`: left or right 
- `speed`: int or list(int) 长度5  值范围0~255

---

### 设置电流
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"set_electric_current\",\"params\":{\"hand_type\":\"left\",\"electric_current\":250}}"}'
```
**Description**: 
设置机械手最大电流 数据格式 std_msgs/msg/String
**Parameters**:
- `hand_type`: left or right 
- `electric_current`: int or list(int) 长度5  值范围0~255

---

### 清除故障
```bash
rostopic pub /cb_hand_setting_cmd std_msgs/String '{data: "{\"setting_cmd\":\"clear_faults\",\"params\":{\"hand_type\":\"left\"}}"}'
```
**Description**: 
清除故障 数据格式 std_msgs/msg/String 当前只支持L20
**Parameters**:
- `hand_type`: left or right 

---

### 控制LinkerHand Topic /cb_left_hand_control_cmd or /cb_right_hand_control_cmd

### LinkerHand手指运动指定位置

# L10
```bash
# 左手
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [80,80,80,80,80,80,80,80,80,80], velocity: [], effort: []}"
# 右手
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [80,80,80,80,80,80,80,80,80,80], velocity: [], effort: []}"
```
# L20
```bash
# 左手
rostopic pub /cb_left_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], velocity: [], effort: []}"
# 右手
rostopic pub /cb_right_hand_control_cmd sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10], velocity: [], effort: []}"
```
**Description**: 
手指运动指定位置 数据格式 sensor_msgs/JointState 
**Parameters**:
- `position`: 手指运动数值 list(float) L7长度:7 L10长度:10 L20长度:20 L25长度:25 每个元素范围0~255 

---

### 获取手状态 Topic /cb_left_hand_state or /cb_right_hand_state
```bash

header: 
  seq: 211345
  stamp: 
    secs: 1744703535
    nsecs: 722361087
  frame_id: ''
name: 
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
position: [255.0, 132.0, 255.0, 255.0, 255.0, 255.0, 131.0, 127.0, 129.0, 127.0]
velocity: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
effort: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```
**Description**: 
手指运动指定位置 数据格式 sensor_msgs/JointState 
**Parameters**:
- `position`: 手指joint当前状态 list(float) L7长度:7 L10长度:10 L20长度:20 L25长度:25 每个元素范围0~255 
---

### 获取压感数据 Topic /cb_left_hand_force or /cb_right_hand_force
```bash
rostopic echo /cb_left_hand_touch
data: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 255.0, 255.0, 255.0, 255.0, 255.0, 0.0, 0.0, 0.0, 0.0, 0.0]
```
**Description**: 
获取手指压感数据 数据格式 std_msgs/Float32MultiArray
**Parameters**:
- `data`:
```bash
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
```
---

### 获取LinkerHand配置信息 Topic /cb_left_hand_info or /cb_right_hand_info
```bash
rostopic echo /cb_right_hand_info
data: "{\"right_hand\": {\"version\": [10, 6, 22, 82, 20, 17, 0], \"hand_joint\": \"L10\"\
  , \"speed\": [250, 250, 250, 250, 250], \"max_press_rco\": [0.0, 0.0, 0.0, 0.0,\
  \ 0.0], \"fault\": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \"motor_temperature\": [43, 65,\
  \ 38, 37, 45, 38, 37, 41, 38, 51]}}"
```
**Description**: 
获取LinkerHand配置信息 数据格式 std_msgs/String for Json
**Parameters**:
- `version`: 手版本号 version[0]:表示L10 version[1]:表示版本 version[2]:表示批号 version[3]:76为左手82为右手 其他未内部编号
- `hand_joint`: L10 or L20 or L25等
- `speed`: 手指速度
- `max_press_rco`: 最大电流
- `fault`: 电机故障 0 为正常 其他为故障
- `motor_temperature`: 当前电机温度

---





















### 设置关节位置
```python
def finger_move(self,pose=[])
```
**Description**:  
设置关节的目标位置，用于控制手指的运动。  
**Parameters**:  
- `pose`: 一个包含目标位置数据的 float类型的list，L7长度为7个元素，L10长度为10个元素，L20长度为20个元素，L25长度为25个元素。

---

### 设置电机电流值
```python
def set_current(self, current=[])
```
**Description**:  
设置电机的电流值。  
**Parameters**:  
- `current`: 一个包含目标电流数据的 int类型list，长度为5个元素，当前只支持L20版本。

---

### 获取速度
```python
def get_speed(self)
return [180, 200, 200, 200, 200]
```
**Description**:  
获取当前设置的速度值。提示：需设置关节位置后才能获取到速度值。

**Returns**:  
- 返回一个 list，包含当前的手指速度设置值。

---

### 获取当前关节状态
```python
def get_state(self)
return [81, 79, 79, 79, 79, 79, 83, 76, 80, 78]
```
**Description**:  
获取当前关节的状态float类型的list信息。提示：需要设置关节位置后才能获取到状态信息，L7长度为7个元素，L10长度为10个元素，L20长度为20个元素，L25长度为25个元素。

**Returns**:  
- 返回一个 float类型的list，包含当前关节的状态数据。

---

### 获取法向压力、切向压力、切向方向、接近感应
```python
def get_force(self)
return [[255.0, 0.0, 0.0, 77.0, 192.0], [82.0, 0.0, 0.0, 230.0, 223.0], [107.0, 255.0, 255.0, 31.0, 110.0], [255.0, 0.0, 20.0, 255.0, 255.0]]
```
**Description**:  
获取手部传感器的综合数据，包括法向压力、切向压力、切向方向和接近感应。  
**Returns**:  
- 返回一个二维list，其中每个子list包含不同类别的list压力数据[[法向压力],[切向压力],[切向压力方向],[接近感应]]。类别每一个元素对应拇指、食指、中指、无名指、小拇指

---

### 获取版本号
```python
def get_version(self)
return [10, 6, 22, 82, 20, 17, 0]
```
**Description**:  
获取当前软件或硬件的版本号。  
**Returns**:  
- 返回一个字符串，表示当前的版本号。list元素依次表示:自由度\版本号\序号\左手76右手82\内部序列号

---
--------------------------------------------------------------
### 获取扭矩
```python
def get_torque(self)
return [200, 200, 200, 200, 200]
```
**Description**:  
获取当前手指扭矩list信息。表示每根手指当前电机扭矩，支持L20、L25。

**Returns**:  
- 返回一个 float类型的list。

---

### 获取电机温度
```python
def get_temperature(self)
return [41, 71, 45, 40, 50, 47, 58, 50, 63, 70]
```
**Description**:  
获取当前关节的电机温度。

**Returns**:  
- 返回一个 list数据，包含当前关节的电机温度。

---

### 获取电机故障码
```python
def get_fault(self)
return [0, 4, 0, 0, 0, 0, 0, 0, 0, 0]
```
**Description**:  
获取当前关节电机故障，0表示正常 数字1电流过载 数字2温度过高 数字3编码错误 数字4过压/欠压。

**Returns**:  
- 返回一个 float类型的list，包含当前关节电机故障。

---

### 清除电机故障码
```python
def clear_faults(self)
```
**Description**:  
尝试清除电机故障，无返回值。只支持L20
**Returns**:  

---

## Example Usage

以下是一个完整的示例代码，展示如何使用上述 API：

```python

from LinkerHand.linker_hand_api import LinkerHandApi
def main():
    # 初始化API hand_type:left or right   hand_joint:L7 or L10 or L20 or L25
    linker_hand = LinkerHandApi(hand_type="left", hand_joint="L10")
    # 设置手指速度
    linker_hand.set_speed(speed=[120,200,200,200,200])
    # 设置手扭矩
    linker_hand.set_torque(torque=[200,200,200,200,200])
    # 获取手当前状态
    hand_state = linker_hand.get_state()
    # 打印状态值
    print(hand_state)

```

---

## Notes
- 在使用 API 之前，请确保手部设备已正确连接并初始化。
- 参数值（如速度、力度等）的具体范围和含义请参考设备的技术手册。

---

## Contact
- 如果有任何问题或需要进一步支持，请联系 [support@linkerhand.com](mailto:support@linkerhand.com)。

---