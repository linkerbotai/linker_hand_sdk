
#!/bin/bash


while true; do
  


#wanqu



  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [130, 255, 255, 255, 255, 180, 128, 128, 128, 128, 220, 0, 0, 0, 0, 255, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [130, 255, 255, 255, 255, 180, 128, 128, 128, 128, 220, 0, 0, 0, 0, 1, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1



done
