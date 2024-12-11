
#!/bin/bash


while true; do
  
  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [255, 255, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [100, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [180, 150, 200, 120, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [100, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [180, 150, 70, 120, 110, 110, 128, 0, 0, 0, 80, 0, 0, 0, 0, 0],
    velocity: [100, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"



  sleep 3

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [180, 150, 200, 120, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [100, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [180, 150, 70, 120, 110, 110, 128, 0, 0, 0, 80, 0, 0, 0, 0, 0],
    velocity: [100, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [180, 150, 200, 120, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [100, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

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
