
#!/bin/bash


while true; do
  

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3','joint4'],
    position: [70, 110, 100, 120, 60, 60, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0],
    velocity: [200, 128, 128, 128, 128, 128, 128, 128, 128, 128, 0, 0, 0, 0, 0, 0],
    effort: [0]
  }"


  sleep 10

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
