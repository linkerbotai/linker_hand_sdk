import rospkg, yaml, os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


global package_path
# 创建 rospkg.RosPack 对象
rospack = rospkg.RosPack()
# 获取指定包的路径
package_sdk = "linker_hand_sdk_ros"
package_gui = "gui_control"
sdk_path = rospack.get_path(package_sdk)
gui_path = rospack.get_path(package_gui)

class LoadWriteYaml():
    def __init__(self):
        # self.hand_joint = hand_joint
        # self.hand_type = hand_type
        self.setting_yaml_path = sdk_path + "/config/setting.yaml"
        self.action_path = gui_path + "/config/"

    def load_setting_yaml(self):
        try:
            with open(self.setting_yaml_path, 'r', encoding='utf-8') as file:
                setting = yaml.safe_load(file)
                self.sdk_version = setting["VERSION"]
                self.left_hand_exists = setting['LINKER_HAND']['LEFT_HAND']['EXISTS']
                self.left_hand_names = setting['LINKER_HAND']['LEFT_HAND']['NAME']
                self.left_hand_joint = setting['LINKER_HAND']['LEFT_HAND']['JOINT']
                self.left_hand_force = setting['LINKER_HAND']['LEFT_HAND']['TOUCH']
                self.right_hand_exists = setting['LINKER_HAND']['RIGHT_HAND']['EXISTS']
                self.right_hand_names = setting['LINKER_HAND']['RIGHT_HAND']['NAME']
                self.right_hand_joint = setting['LINKER_HAND']['RIGHT_HAND']['JOINT']
                self.right_hand_force = setting['LINKER_HAND']['RIGHT_HAND']['TOUCH']
                self.password = setting['PASSWORD']
        except Exception as e:
            setting = None
            print(f"Error reading setting.yaml: {e}")
        self.setting = setting
        return self.setting

    def load_action_yaml(self,hand_joint="",hand_type=""):
        action_path = gui_path + "/config/"
        if hand_joint == "L20":
            action_path = action_path + "L20_action.yaml"
        elif hand_joint == "L10":
            action_path = action_path + "L10_action.yaml"
        elif hand_joint == "L25":
            action_path = action_path + "L25_action.yaml"
        elif hand_joint == "L7":
            action_path = action_path + "L7_action.yaml"
        
        try:
            with open(action_path, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                if hand_type == "left":
                    self.action_yaml = yaml_data["LEFT_HAND"]
                else:
                    self.action_yaml = yaml_data["RIGHT_HAND"]
        except Exception as e:
            self.action_yaml = None
            print(f"yaml配置文件不存在: {e}")
        return self.action_yaml 

    def write_to_yaml(self, action_name, action_pos,hand_joint="",hand_type=""):
        a = False
        action_path = gui_path + "/config/"
        print(action_path)
        if hand_joint == "L20":
            action_path = action_path + "L20_action.yaml"
        elif hand_joint == "L10":
            action_path = action_path + "L10_action.yaml"
        elif hand_joint == "L25":
            action_path = action_path + "L25_action.yaml"
        elif hand_joint == "L7":
            action_path = action_path + "L7_action.yaml"
        try:
            with open(action_path, 'r', encoding='utf-8') as file:
                yaml_data = yaml.safe_load(file)
                print(yaml_data)
            if hand_type == "left":
                if yaml_data["LEFT_HAND"] == None:
                    yaml_data["LEFT_HAND"] = []
                yaml_data["LEFT_HAND"].append({"ACTION_NAME": action_name, "ACTION_POS": action_pos})
            elif hand_type == "right":
                if yaml_data["RIGHT_HAND"] == None:
                    yaml_data["RIGHT_HAND"] = []
                yaml_data["RIGHT_HAND"].append({"ACTION_NAME": action_name, "ACTION_POS": action_pos})
            with open(action_path, 'w', encoding='utf-8') as file:
                yaml.safe_dump(yaml_data, file, allow_unicode=True)
            a = True
        except Exception as e:
            a = False
            print(f"Error writing to yaml file: {e}")
        return a