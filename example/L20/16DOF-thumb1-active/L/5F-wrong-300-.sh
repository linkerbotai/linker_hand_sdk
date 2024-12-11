
#!/bin/bash


while true; do
  

#wanqu

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 0, 0, 0, 0, 300, 300, 300, 300, 300],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


done
