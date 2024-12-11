import sys,os,time,subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from color_msg import ColorMsg
class OpenCan:
    def __init__(self):
        pass

    def open_can0(self):
        try:
            # 检查 can0 接口是否已存在并处于 up 状态
            result = subprocess.run(
                ["ip", "link", "show", "can0"],
                check=True,
                text=True,
                capture_output=True
            )
            if "state UP" in result.stdout:
                ColorMsg(msg="CAN接口已经是 UP 状态")
                return 
            # 如果没有处于 UP 状态，则配置接口
            subprocess.run(
                ["sudo", "-S", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "1000000"],
                input=f"{self.password}\n",
                check=True,
                text=True,
                capture_output=True
            )
            
        except subprocess.CalledProcessError as e:
            pass
        except Exception as e:
            pass
            

    def is_can_up_sysfs(self, interface="can0"):
    # 检查接口目录是否存在
        if not os.path.exists(f"/sys/class/net/{interface}"):
            return False
        # 读取接口状态
        try:
            with open(f"/sys/class/net/{interface}/operstate", "r") as f:
                state = f.read().strip()
            if state == "up":
                return True
        except Exception as e:
            print(f"Error reading CAN interface state: {e}")
            return False