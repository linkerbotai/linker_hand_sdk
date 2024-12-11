
#!/bin/bash


while true; do

#cebai-wanqu-init
rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint9'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


#max-open

rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint9'],
    position: [150, 255, 255, 255, 255, 128, 200, 200, 200, 200, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
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
    name: ['joint9'],
    position: [150, 150, 150, 150, 150, 128, 200, 200, 200, 200, 255, 0, 0, 0, 0, 255, 120, 120, 120, 120],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


#cebai-wabqu-init
rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint9'],
    position: [255, 255, 255, 255, 255, 128, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

#max-close


rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint9'],
    position: [150, 255, 255, 255, 255, 128, 56, 56, 56, 56, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
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
    name: ['joint9'],
    position: [150, 150, 150, 150, 150, 128, 56, 56, 56, 56, 255, 0, 0, 0, 0, 255, 120, 120, 120, 120],
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
    name: ['joint9'],
    position: [255, 255, 255, 255, 255, 128, 56, 56, 56, 56, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

  
done
