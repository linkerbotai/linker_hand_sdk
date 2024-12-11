
#!/bin/bash


while true; do
  
#hengbai

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 50, 0, 0, 0, 0, 200, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 200, 0, 0, 0, 0, 200, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
