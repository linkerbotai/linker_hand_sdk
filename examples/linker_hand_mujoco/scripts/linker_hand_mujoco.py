import mujoco,sys,os,time
import mujoco.viewer
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.color_msg import ColorMsg
from utils.mj_control import MJControlWrapper
class MujocoSim:
    def __init__(self, model_path):
        # Load Mujoco model
        self.mj = MJControlWrapper(model_path=model_path)
        # timer for simulation
        self.start_time = time.time()
        #self.sim_timer = self.create_timer(0.01, self.forward_sim)
        self.mj.launch_viewer(viewer_type="active")


    def forward_sim(self):
        """Forward the simulator until the current time."""
        current_time = time.time() - self.start_time
        # Step the simulation to apply the control
        self.mj.step(until=current_time)

if __name__ == "__main__":
    model_path = '/home/hjx/ROS/Linker_Hand_SDK_ROS/src/linker_hand_sdk/examples/linker_hand_mujoco/urdf/linker_hand_l20_8_right.xml'  # 替换为您的模型文件路径
    sim = MujocoSim(model_path)
    # sim.simulate()
    # sim.close()