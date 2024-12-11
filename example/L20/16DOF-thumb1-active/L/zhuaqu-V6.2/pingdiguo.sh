
#!/bin/bash


while true; do
  

    rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [255, 100, 100, 100, 100, 255, 128, 128, 128, 128, 120, 0, 0, 0, 0, 255, 20, 20, 20, 20],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [255, 20, 20, 20, 20, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 255, 20, 20, 20, 20],
    velocity: [0],
    effort: [0]
  }"

  sleep 1
  

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [90, 20, 20, 20, 20, 150, 128, 118, 128, 128, 120, 0, 0, 0, 0, 130, 20, 20, 20, 20],
    velocity: [0],
    effort: [0]
  }"

  sleep 30

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
