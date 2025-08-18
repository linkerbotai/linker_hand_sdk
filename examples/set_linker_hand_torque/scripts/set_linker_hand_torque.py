'''
Author: HJX
Date: 2025-04-08 13:28:18
LastEditors: Please set LastEditors
LastEditTime: 2025-04-09 11:41:59
FilePath: /Linker_Hand_SDK_ROS/src/examples/set_linker_hand_torque/scripts/set_linker_hand_torque.py
Description: 
symbol_custom_string_obkorol_copyright: 
'''
#!/usr/bin/env python3
import rospy,rospkg
import time,os,sys,json
from std_msgs.msg import String,Header, Float32MultiArray
from sensor_msgs.msg import JointState

def main():
    rospy.init_node('set_linker_hand_torque', anonymous=True)
    pub = rospy.Publisher("/cb_hand_setting_cmd",String,queue_size=10)
    msg = String()
    torque = [200,200,200,200,200]  # O6为6个值，L7为7个值，其他为5个值
    #torque = ["AA","AA","AA","AA","AA"]
    dic = {
        "setting_cmd":"set_max_torque_limits",
        "params":{
            "hand_type": "left",
            "torque":torque
        }
    }
    msg.data = json.dumps(dic)
    count = 0  #计数器 
    # 设置循环频率
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()
        rospy.loginfo("写出的数据:%s",msg.data)
        count += 1
        if count > 3:
            break
    


if __name__ == '__main__':
    main()
    