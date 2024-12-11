
#!/bin/bash


while true; do
  

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [255, 1, 1, 1, 1, 200, 128, 128, 128, 128, 50, 0, 0, 0, 0, 255, 1, 1, 1, 1],
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
    position: [20, 1, 1, 1, 1, 200, 128, 128, 128, 128, 50, 0, 0, 0, 0, 150, 1, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

sleep 20
  
done
