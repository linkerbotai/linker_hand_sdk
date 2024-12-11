
#!/bin/bash


while true; do
  

    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
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
    name: ['joint3'],
    position: [255, 200, 200, 200, 200, 80, 128, 128, 128, 128, 120, 0, 0, 0, 0, 255, 90, 90, 90, 90],
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
    name: ['joint3'],
    position: [255, 80, 80, 80, 80, 80, 128, 128, 128, 128, 120, 0, 0, 0, 0, 255, 90, 90, 90, 90],
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
    name: ['joint3'],
    position: [45,  80, 80, 80, 80, 80, 128, 128, 128, 128, 120, 0, 0, 0, 0, 150, 90, 90, 90, 90],
    velocity: [0],
    effort: [0]
  }"

  sleep 30

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
