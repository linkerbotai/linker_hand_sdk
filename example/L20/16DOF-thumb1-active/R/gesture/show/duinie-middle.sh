
#!/bin/bash


while true; do


  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [35, 250, 40, 250, 250, 130, 128, 128, 128, 128, 150, 0, 0, 0, 0, 250, 110, 180, 110, 110],
    velocity: [0],
    effort: [0]
  }"

  sleep 5


  
done
