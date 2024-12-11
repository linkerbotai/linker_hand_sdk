
#!/bin/bash


while true; do


  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [110, 250, 250, 250, 130, 120, 128, 128, 128, 128, 70, 0, 0, 0, 0, 150, 250, 250, 250, 70],
    velocity: [0],
    effort: [0]
  }"

  sleep 5


  
done
