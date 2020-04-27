# USAR_multirrobot
This is the implementation of a high-level behavior supervisor for coordination of multirrobots in USAR (Urban Search and Rescue) applications.

To run the world with multiple robots:
```
source devel/setup.bash
roslaunch usar_gazebo post-disaster.launch
```

To control the a robot position:
```
source devel/setup.bash
rosrun controllers robot_name x y rot
```
'robot_name' pode ser: pioneer2dx_1, pioneer2dx_2, pioneer3at_1, pioneer3at_2
x, y e rot representam a localização desejada e orientação final
