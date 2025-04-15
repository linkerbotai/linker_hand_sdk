"""
Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.

Joint Monkey
------------
- Animates degree-of-freedom ranges for a given asset.
- Demonstrates usage of DOF properties and states.
- Demonstrates line drawing utilities to visualize DOF frames (origin and axis).
"""

import math
import numpy as np
from isaacgym import gymapi, gymutil
import rospy
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState

# 初始化 ROS 节点（必须在 Isaac Gym 主线程中）
rospy.init_node('isaac_arm_controller', anonymous=True)
rate = rospy.Rate(10)

# 全局变量存储 ROS 接收到的目标位置
arm_target_positions = JointState()
default_position = [255,255,255,255,255,255,128,128,128,128,255,0,0,0,0,255,255,255,255,255]
arm_target_positions.position = default_position
current_positions = arm_target_positions.position
def arm_control_callback(data):
    global arm_target_positions
    # print(f"topic data :{data}")
    arm_target_positions = data

# 订阅 Topic
rospy.Subscriber('/arm_control', JointState, arm_control_callback)

def clamp(x, min_value, max_value):
    return max(min(x, max_value), min_value)


def enhanced_mapping(input_val, min_limit, max_limit, input_range=(0,255)):
    """
    增强版映射函数（支持自定义输入范围）
    
    参数：
    input_range : 输入值范围元组（默认(0,255)）
    """
    # 解包输入范围
    in_min, in_max = input_range
    # 计算标准化输入（带范围限制）
    clamped = max(in_min, min(in_max, input_val))
    normalized = (clamped - in_min) / (in_max - in_min)
    # 反向映射
    return max_limit - (max_limit - min_limit) * normalized
#将0-255数据根据高低限制位转换成rad
def transformPosition(input_value, output_min_mapped, output_max_mapped):
    print(f" input:{input_value}  min:{output_min_mapped}   max:{output_max_mapped}")
    temp=0.0
    if(output_max_mapped<0.1):  #这里因为最小值是0.26 所以比0.1小就视为0
        print("a")
        if(input_value>255):
            input_value=255
        elif(input_value<0):
            input_value=0
        input_min = 0
        input_max = 255
        output_value = output_min_mapped + (input_value - input_min) * (output_max_mapped - output_min_mapped) / (input_max - input_min)
        temp =  round(output_value, 2)  # 四舍五入到小数点后2位
    else:
        temp = round(enhanced_mapping(input_value,output_min_mapped,output_max_mapped),2)
    if(temp>output_max_mapped):
        return output_max_mapped
    elif(temp<output_min_mapped):
        return output_min_mapped
    return temp

def transArray(array):
    tempArray =[]
    for i in range(len(array)):
        tempArray.append(transformPosition(array[i],lower_limits[i],upper_limits[i]))
    return tempArray

def reorderList(array):
    temp= np.zeros(21)
    #  joint12-joint15 预留参数
    temp[0]= array[6]   #dof1 index_joint0          joint7 食指侧摆
    temp[1]= array[1]   #dof2 index_joint1          joint2 食指根部弯曲
    temp[2]= array[16]   #dof3 index_joint2          joint17 食指弯曲
    temp[3]= array[16]   #dof4 index_joint3          joint17 食指末端弯曲 从动
    temp[4]= array[9]   #dof5 little_joint0         joint10 小指侧摆
    temp[5]= array[4]   #dof6 little_joint1         joint5 小指根部弯曲
    temp[6]= array[19]   #dof7 little_joint2         joint20 小指弯曲
    temp[7]= array[19]   #dof8 little_joint3         joint20 小指根部弯曲 从动
    temp[8]= array[7]   #dof9 middle_joint0         joint8 中指侧摆
    temp[9]= array[2]   #dof10 middle_joint1        joint3 中指根部弯曲
    temp[10]= array[17]   #dof11 middle_joint2        joint18 中指弯曲
    temp[11]= array[17]   #dof12 middle_joint3        joint18 中指末端弯曲 从动
    temp[12]= array[8]   #dof13 ring_joint0          joint9 无名指侧摆
    temp[13]= array[3]   #dof14 ring_joint1          joint4  无名指根部弯曲
    temp[14]= array[18]   #dof15 ring_joint2          joint19 无名指弯曲
    temp[15]= array[18]   #dof16 ring_joint3          joint19 无名指末端弯曲 从动
    temp[16]= array[0]   #dof17 thumb_joint0         joint1 拇指根部弯曲
    temp[17]= array[5]   #dof18 thumb_joint1         joint6  拇指侧摆
    temp[18]= array[10]   #dof19 thumb_joint2         joint11 拇指旋转
    temp[19]= array[15]   #dof20 thumb_joint3         joint16 拇指弯曲
    temp[20]= array[15]   #dof21 thumb_joint4         joint16 拇指末端弯曲 这是从动关节


    # print(f"temp:{temp}  array:{array}")
    return temp
# simple asset descriptor for selecting from a list


class AssetDesc:
    def __init__(self, file_name, flip_visual_attachments=False):
        self.file_name = file_name
        self.flip_visual_attachments = flip_visual_attachments


asset_descriptors = [
    AssetDesc("urdf/linker_hand_l20_8_right_2.urdf", False),#/home/moning/HHHHand/l20_8_urdf/mjcf/l20_8_urdf.xml

]

#怎样提供路径
# parse arguments
args = gymutil.parse_arguments(
    description="Linker Hand : Simulation for Gym",
    custom_parameters=[
        {"name": "--asset_id", "type": int, "default": 0, "help": "Asset id (0 - %d)" % (len(asset_descriptors) - 1)},
        {"name": "--speed_scale", "type": float, "default": 1.0, "help": "Animation speed scale"},
        {"name": "--show_axis", "action": "store_true", "help": "Visualize DOF axis"}])

if args.asset_id < 0 or args.asset_id >= len(asset_descriptors):
    print("*** Invalid asset_id specified.  Valid range is 0 to %d" % (len(asset_descriptors) - 1))
    quit()


# initialize gym
gym = gymapi.acquire_gym()

# configure sim
sim_params = gymapi.SimParams()
sim_params.dt = dt = 1.0 / 60.0
if args.physics_engine == gymapi.SIM_FLEX:
    pass
elif args.physics_engine == gymapi.SIM_PHYSX:
    sim_params.physx.solver_type = 1
    sim_params.physx.num_position_iterations = 6
    sim_params.physx.num_velocity_iterations = 0
    sim_params.physx.num_threads = args.num_threads
    sim_params.physx.use_gpu = args.use_gpu

sim_params.use_gpu_pipeline = False
if args.use_gpu_pipeline:
    print("WARNING: Forcing CPU pipeline.")

sim = gym.create_sim(args.compute_device_id, args.graphics_device_id, args.physics_engine, sim_params)
if sim is None:
    print("*** Failed to create sim")
    quit()

# add ground plane
plane_params = gymapi.PlaneParams()
gym.add_ground(sim, plane_params)

# create viewer
viewer = gym.create_viewer(sim, gymapi.CameraProperties())
if viewer is None:
    print("*** Failed to create viewer")
    quit()

# load asset
asset_root = "../../assets"
asset_file = asset_descriptors[args.asset_id].file_name

asset_options = gymapi.AssetOptions()
asset_options.fix_base_link = True
asset_options.flip_visual_attachments = asset_descriptors[args.asset_id].flip_visual_attachments
asset_options.use_mesh_materials = True

print("Loading asset '%s' from '%s'" % (asset_file, asset_root))
asset = gym.load_asset(sim, asset_root, asset_file, asset_options)

# get array of DOF names
dof_names = gym.get_asset_dof_names(asset)

# get array of DOF properties
dof_props = gym.get_asset_dof_properties(asset)

# create an array of DOF states that will be used to update the actors
num_dofs = gym.get_asset_dof_count(asset)
dof_states = np.zeros(num_dofs, dtype=gymapi.DofState.dtype)

# get list of DOF types
dof_types = [gym.get_asset_dof_type(asset, i) for i in range(num_dofs)]

# get the position slice of the DOF state array
dof_positions = dof_states['pos']

# get the limit-related slices of the DOF properties array
stiffnesses = dof_props['stiffness']
dampings = dof_props['damping']
armatures = dof_props['armature']
has_limits = dof_props['hasLimits']
lower_limits = dof_props['lower']
upper_limits = dof_props['upper']
print(f" dof props : {dof_props}  dof names:{dof_names}" )

# initialize default positions, limits, and speeds (make sure they are in reasonable ranges)
defaults = np.zeros(num_dofs)
speeds = np.zeros(num_dofs)
# print(f"lower limit before : {lower_limits}")
# print(f"upper limit before : {upper_limits}")
for i in range(num_dofs):
    if has_limits[i]:
        if dof_types[i] == gymapi.DOF_ROTATION:
            lower_limits[i] = clamp(lower_limits[i], -math.pi, math.pi)
            upper_limits[i] = clamp(upper_limits[i], -math.pi, math.pi)
        # make sure our default position is in range
        if lower_limits[i] > 0.0:
            defaults[i] = lower_limits[i]
        elif upper_limits[i] < 0.0:
            defaults[i] = upper_limits[i]
    else:
        # set reasonable animation limits for unlimited joints
        if dof_types[i] == gymapi.DOF_ROTATION:
            # unlimited revolute joint
            lower_limits[i] = -math.pi
            upper_limits[i] = math.pi
        elif dof_types[i] == gymapi.DOF_TRANSLATION:
            # unlimited prismatic joint
            lower_limits[i] = -1.0
            upper_limits[i] = 1.0
    # set DOF position to default
    dof_positions[i] = defaults[i]
    # set speed depending on DOF type and range of motion
    if dof_types[i] == gymapi.DOF_ROTATION:
        speeds[i] = args.speed_scale * clamp(2 * (upper_limits[i] - lower_limits[i]), 0.25 * math.pi, 3.0 * math.pi)
    else:
        speeds[i] = args.speed_scale * clamp(2 * (upper_limits[i] - lower_limits[i]), 0.1, 7.0)
# print(f"lower limit after : {lower_limits}")
# print(f"upper limit after : {upper_limits}")
# print(f"speed scale :{args.speed_scale}  speeds : {speeds}")
# Print DOF properties
for i in range(num_dofs):
    print("DOF %d" % i)
    print("  Name:     '%s'" % dof_names[i])
    print("  Type:     %s" % gym.get_dof_type_string(dof_types[i]))
    print("  Stiffness:  %r" % stiffnesses[i])
    print("  Damping:  %r" % dampings[i])
    print("  Armature:  %r" % armatures[i])
    print("  Limited?  %r" % has_limits[i])
    if has_limits[i]:
        print("    Lower   %f" % lower_limits[i])
        print("    Upper   %f" % upper_limits[i])

num_envs = 1
num_per_row = 1
spacing = 1
env_lower = gymapi.Vec3(-spacing, 0.0, -spacing)
env_upper = gymapi.Vec3(spacing, spacing, spacing)

# position the camera
cam_pos = gymapi.Vec3(0, 1.5, 1.2)
cam_target = gymapi.Vec3(0, 1, 0)
gym.viewer_camera_look_at(viewer, None, cam_pos, cam_target)

# cache useful handles
envs = []
actor_handles = []

print("Creating %d environments" % num_envs)
for i in range(num_envs):
    # create env
    env = gym.create_env(sim, env_lower, env_upper, num_per_row)
    envs.append(env)

    # add actor
    pose = gymapi.Transform()
    pose.p = gymapi.Vec3(0.0, 1.32, 0.0)
    # pose.r = gymapi.Quat(-0.707107, 0.0, 0.0, 0.707107)
    pose.r = gymapi.Quat.from_euler_zyx(3.14, -1.57, 1.57)

    actor_handle = gym.create_actor(env, asset, pose, "actor", i, 1)
    actor_handles.append(actor_handle)
    reorder = reorderList(current_positions)
    trans = transArray(reorder)
    dof_states["pos"] = trans
    # set default DOF positions
    gym.set_actor_dof_states(env, actor_handle, dof_states, gymapi.STATE_ALL)

while not gym.query_viewer_has_closed(viewer):

    # print(f"ros joint:{arm_target_positions}")
    # step the physics
    gym.simulate(sim)
    gym.fetch_results(sim, True)

    for i in range(len(arm_target_positions.position)):
        speed= speeds[i]
        cur_p = current_positions[i]
        tar_p = arm_target_positions.position[i]
        if(cur_p>tar_p):
            cur_p -=speed
            if(cur_p>=tar_p):
                current_positions[i]=cur_p
            else:
                current_positions[i]=tar_p
        elif(cur_p<tar_p):
            cur_p +=speed
            if(cur_p<=tar_p):
                current_positions[i]=cur_p
            else:
                current_positions[i]=tar_p
    reorder = reorderList(current_positions)               
    trans = transArray(reorder)

    dof_states["pos"] = trans
    # clone actor state in all of the environments
    for i in range(num_envs):
        gym.set_actor_dof_states(envs[i], actor_handles[i], dof_states, gymapi.STATE_POS)

 
   # update the viewer
    gym.step_graphics(sim)
    gym.draw_viewer(viewer, sim, True)
    # Wait for dt to elapse in real time.
    # This synchronizes the physics simulation with the rendering rate.
    gym.sync_frame_time(sim)

print("Done")

gym.destroy_viewer(viewer)
gym.destroy_sim(sim)

