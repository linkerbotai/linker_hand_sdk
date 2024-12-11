
#!/bin/bash


while true; do
#def
  

    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
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
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 100, 128, 128, 128, 128, 255, 0, 0, 0, 0, 200, 0, 0, 0, 0],
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
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 200, 0, 0, 0, 0],
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
    position: [160, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 80, 0, 0, 0, 0],
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
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 255, 0, 0, 0, 0],
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
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [0],
    effort: [0]
  }"

  sleep 1

#10

    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 100, 128, 128, 128, 128, 255, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
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
    position: [160, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 80, 0, 0, 0, 0],
    velocity: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
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
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 255, 0, 0, 0, 0],
    velocity: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    effort: [0]
  }"

  sleep 1

#100
    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 100, 128, 128, 128, 128, 255, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
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
    position: [160, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 80, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
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
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 255, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1

#255
    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 100, 128, 128, 128, 128, 255, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
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
    position: [160, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 80, 0, 0, 0, 0],
    velocity: [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
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
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 255, 0, 0, 0, 0],
    velocity: [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    effort: [0]
  }"

  sleep 1

#100
    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 100, 128, 128, 128, 128, 255, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1


    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 200, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
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
    position: [160, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 80, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
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
    position: [255, 0, 0, 0, 0, 80, 128, 128, 128, 128, 150, 0, 0, 0, 0, 255, 0, 0, 0, 0],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1

  rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [255, 255, 255, 255, 255, 200, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
    velocity: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    effort: [0]
  }"

  sleep 1
  
done
