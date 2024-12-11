
#!/bin/bash


while true; do
  


  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [55, 1, 1, 1, 1, 128, 128, 128, 128, 128, 120, 0, 0, 0, 0, 30, 1, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
