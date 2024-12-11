
#!/bin/bash


while true; do
  
  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128],
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
    name: ['joint3','joint4'],
    position: [255, 255, 0, 0, 0, 0, 128, 128, 128, 128],
    velocity: [0],
    effort: [0]
  }"

  

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [100, 255, 0, 0, 0, 0, 128, 128, 128, 128],
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
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
