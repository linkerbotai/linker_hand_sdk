
#!/bin/bash


while true; do
  
  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint2'],
    position: [255, 0, 255, 255, 255, 255, 128, 128, 128, 255, 0, 0, 0, 0, 0, 0],
    velocity: [10, 5, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint2'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 255, 0, 0, 0, 0, 0, 0],
    velocity: [10, 5, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"

  sleep 1

  
done
