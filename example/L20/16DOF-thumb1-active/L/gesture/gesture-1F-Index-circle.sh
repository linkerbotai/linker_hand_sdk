
#!/bin/bash


while true; do
  
  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"


  usleep 1
  

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 10, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 180, 1, 1, 1, 255, 10, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 150, 1, 1, 1, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 180, 1, 1, 1, 255, 220, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 220, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1


  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 10, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 180, 1, 1, 1, 255, 10, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 150, 1, 1, 1, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 180, 1, 1, 1, 255, 220, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 220, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [180, 255, 1, 1, 1, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 1, 1, 1],
    velocity: [0],
    effort: [0]
  }"

  usleep 1

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"


  usleep 1

  
done
