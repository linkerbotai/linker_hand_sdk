#!/usr/bin/env python3
import rospy,json
from std_msgs.msg import String

if __name__ == '__main__':
    '''
    L7:
    rosrun set_linker_hand_speed set_linker_hand_speed.py _hand_type:=right _speed:="[255,255,255,255,255,255,255]"

    other:
    rosrun set_linker_hand_speed set_linker_hand_speed.py _hand_type:=right _speed:="[100,100,100,100,100]"
    '''
    rospy.init_node('get_linker_hand_speed', anonymous=True)
    hand_type = rospy.get_param("~hand_type",default="left") # 设置哪只手的速度
    speed = rospy.get_param('~speed', default=[255,255,255,255,255])  # 默认获取全局参数  O6为6个值，L7为7个值，其他为5个值

    pub = rospy.Publisher("/cb_hand_setting_cmd",String,queue_size=10)
    msg = String()  #创建 msg 对象
    count = 0  #计数器 
    # 设置循环频率
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        # 由于ROS1 单发topic有可能丢失，这里循环发3次避免丢失
        dic = {
            "setting_cmd":"set_speed",
            "params":{
                "hand_type": hand_type,
                "speed":speed
            }
        }
        #拼接字符串
        msg.data = json.dumps(dic)

        pub.publish(msg)
        rate.sleep()
        rospy.loginfo("写出的数据:%s",msg.data)
        count += 1
        if count > 2:
            break
    
