
#!/bin/bash


while true; do
  
rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint9'],
    position: [255, 255, 255, 255, 255, 128, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    name: ['joint8','joint9'],
    position: [255, 50, 50, 50, 50, 128, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint8','joint9'],
    position: [90, 50, 50, 50, 50, 128, 0, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  sleep 10

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint8','joint9'],
    position: [255, 255, 255, 255, 255, 128, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
