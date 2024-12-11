
#!/bin/bash


while true; do
  


#two finger

    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint3'],
    position: [255, 255, 255, 255, 255, 255, 128, 128, 128, 128, 255, 0, 0, 0, 0, 255, 255, 255, 255, 255],
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
    position: [255, 100, 100, 255, 255, 110, 128, 128, 128, 128, 100, 0, 0, 0, 0, 240, 200, 200, 255, 255],
    velocity: [0],
    effort: [0]
  }"


  sleep 1

  
done
