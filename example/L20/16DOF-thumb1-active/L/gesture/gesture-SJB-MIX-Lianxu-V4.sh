#!/bin/bash


while true; do
#init

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [60, 200, 200, 200, 200, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 150, 40, 40, 40, 40],
    velocity: [0],
    effort: [0]
  }"

  sleep 1



#shitou

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [60, 1, 1, 1, 1, 0, 128, 128, 128, 128, 120, 0, 0, 0, 0, 80, 1, 1, 1, 1],
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
    name: ['joint6'],
    position: [60, 200, 200, 200, 200, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 160, 40, 40, 40, 40],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

#jiandao

 rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [20, 255, 255, 1, 1, 0, 0, 255, 128, 128, 120, 0, 0, 0, 0, 100, 255, 255, 1, 1],
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
    name: ['joint6'],
    position: [40, 200, 200, 200, 200, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 160, 40, 40, 40, 40],
    velocity: [0],
    effort: [0]
  }"

  sleep 2
  

#bu

  rostopic pub -1 /cb_left_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 128, 0, 128, 180, 255, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
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
    name: ['joint6'],
    position: [40, 200, 200, 200, 200, 150, 128, 128, 128, 128, 120, 0, 0, 0, 0, 150, 40, 40, 40, 40],
    velocity: [0],
    effort: [0]
  }"

  sleep 1
  
  
done
