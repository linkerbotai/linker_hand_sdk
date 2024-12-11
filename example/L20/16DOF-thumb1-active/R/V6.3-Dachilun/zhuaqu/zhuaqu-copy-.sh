
#!/bin/bash


while true; do
  

    rostopic pub -1 /cb_right_hand_control_cmd sensor_msgs/JointState "{
    header: {
      seq: 0,
      stamp: {secs: 0, nsecs: 0},
      frame_id: ''
    },
    name: ['joint6'],
    position: [200, 40, 50, 60, 60, 70, 138, 138, 138, 138, 160, 0, 0, 0, 0, 80, 40, 50, 50, 50],
    velocity: [0],
    effort: [0]
  }"

  sleep 1


  
done
