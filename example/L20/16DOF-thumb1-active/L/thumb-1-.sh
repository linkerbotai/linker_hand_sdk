
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
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [1, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [128, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [128, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 1, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint1'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 200, 200, 200, 200],
    velocity: [0],
    effort: [0]
  }"

  sleep 1
 


done
