
#!/bin/bash


while true; do
  

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [255, 5, 5, 5, 5, 5, 128, 128, 128, 128, 120, 0, 0, 0, 0, 250, 5, 5, 5, 5],
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
    name: ['joint3'],
    position: [120, 5, 5, 5, 5, 5, 128, 128, 128, 128, 120, 0, 0, 0, 0, 0, 5, 5, 5, 5],
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
    position: [255, 250, 250, 250, 250, 128, 128, 128, 128, 128, 250, 0, 0, 0, 0, 250, 250, 250, 250, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
