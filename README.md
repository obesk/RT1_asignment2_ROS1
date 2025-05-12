# Assignment 2 Research Track 1 - ROS 1

This assignment interacts with the gazebo simulation environment provided by the package https://github.com/CarmineD8/assignment_2_2024 and interacts with the robot in it.

The purpose of the assignment is to show the interaction between nodes in ROS1 

When this package is run the robot should move in a zig-zag motion.

## Prerequisites

You should have a working ROS1 installation. This package has been tested with noetic.

Be sure to add to also have installed the package https://github.com/CarmineD8/assignment_2_2024, which provides the simulation.


## How to run

You can launch the whole simulation environment and this package by using the following command:
```bash
roslaunch ass2_ros1 ass2_ros1.launch 
```

If instead you want to use the jupyter notebook interface it's sufficient to launche the simulation with:

```bah
roslaunch assignment_2_2024 assignment1.launch
```

and then interact with the jupyter notebook in the script folder

## Description

After running the simulation and the program you will be prompted with the menu, from where you can follow the instructions.

In this assignment you can see the use of custom Goal in the `goal_service.py` script.

In the `action_client.py` script you can see the use of actions and custom messages.
