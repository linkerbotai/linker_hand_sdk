
#!/bin/bash


while true; do


  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [170, 130, 250, 250, 250, 120, 128, 128, 128, 128, 200, 0, 0, 0, 0, 110, 70, 250, 250, 250],
    velocity: [0],
    effort: [0]
  }"

  sleep 5


  
done
