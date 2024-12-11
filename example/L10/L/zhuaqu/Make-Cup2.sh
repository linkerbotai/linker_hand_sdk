
#!/bin/bash


while true; do
  

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"


  
  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [255, 112, 112, 114, 87, 87, 141, 255, 255, 241, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  
  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [255, 112, 112, 114, 87, 87, 141, 24, 17, 241, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"


  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [110, 112, 112, 114, 87, 87, 141, 24, 17, 241, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  sleep 2


  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [255, 112, 112, 114, 87, 87, 141, 24, 17, 241, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [255, 112, 112, 114, 87, 87, 141, 255, 255, 241, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"


  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
