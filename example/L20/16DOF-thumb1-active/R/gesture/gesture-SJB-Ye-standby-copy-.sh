
#!/bin/bash


while true; do

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [40, 200, 200, 200, 200, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 150, 40, 40, 40, 40],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
