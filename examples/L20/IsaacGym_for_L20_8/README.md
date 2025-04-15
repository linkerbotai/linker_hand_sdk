# 使用 IsaacGym 模拟 L20 仿真环境

> **注意**：以下教程默认你已经安装好 IsaacGym 并成功运行其示例。若未安装或运行示例失败，请查阅 [Nvidia 官网](https://developer.nvidia.com/isaac-gym)获取详细安装教程。

---

## 步骤 1：配置 URDF 文件路径
将 L20 的 URDF 文件路径填入 `AssetDesc` 中，确保仿真环境能正确加载模型。

---

## 步骤 2：启动 ROS 核心
新开终端，运行以下命令启动 ROS 核心：
```bash
roscore
```

---

## 步骤 3：启动 L20 仿真示例
运行 `l20_example.py` 启动仿真环境：
```bash
python l20_example.py
```
- **成功现象**：IsaacGym 可视化窗口启动，并展示 L20 灵巧手模型。

---

## 步骤 4：验证控制节点
新开终端，检查 `/arm_control` 节点是否存在：
```bash
rostopic list
```
- **若存在**：继续下一步。
- **若不存在**：检查 `roscore` 是否运行，或 `l20_example.py` 是否启动成功。

---

## 步骤 5：手动控制灵巧手
### 5.1 发送初始控制命令
新开终端，发送初始关节状态命令：
```bash
rostopic pub /arm_control sensor_msgs/JointState "{header: {seq: 0, stamp: {secs: 0, nsecs: 0}, frame_id: ''}, name: [], position: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], velocity: [], effort: []}"
```

### 5.2 观察并调整动作
- **观察**：在 IsaacGym 可视化窗口中观察手的动作。
- **调整**：修改 `position` 数组中的值，发送新命令以控制手的姿态。

---

## 步骤 6：通过 ROS 代码控制
在 ROS 代码中向 `/arm_control` 发送控制命令，格式与手动控制相同。示例代码如下：
```python
import rospy
from sensor_msgs.msg import JointState

rospy.init_node('l20_controller')
pub = rospy.Publisher('/arm_control', JointState, queue_size=10)

# 定义关节状态
joint_state = JointState()
joint_state.name = ['joint1', 'joint2', ..., 'joint20']  # 替换为实际关节名称
joint_state.position = [0.1, 0.2, ..., 0.0]              # 替换为目标关节角度

# 发布控制命令
pub.publish(joint_state)
```

---

⚠️ **注意事项**：
- **URDF 版本**：本教程仅支持 `l20_8` 版本的 URDF 文件。其他版本可能无法正常控制。
- **依赖项**：确保已安装 ROS 及相关依赖库（如 `sensor_msgs`）。

如有其他问题，请检查 IsaacGym 和 ROS 的日志输出以排查错误。
