
#!/bin/bash


while true; do
  


  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [100, 255, 255, 255, 255, 100, 128, 128, 128, 128, 128, 0, 0, 0, 0, 50, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 110

  
done
