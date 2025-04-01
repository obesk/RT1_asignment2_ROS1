#! /usr/bin/env python

"""
This is an action client node to allows the user to interact with the goals. 
Specifically the user can:

- Update the goal
- Get status of the current goal retrieving mission

This node also publishes a custom message with the current robot velocity and position


.. module:: action_client
   :platform: Unix
   :synopsis: Action client, robot velocity and position publisher 

.. moduleauthor:: Roberto Bertelli <s7289118@studenti.unige.it>
"""

from assignment_2_2024.msg import PlanningAction, PlanningGoal

import rospy
import actionlib

import time

from nav_msgs.msg import Odometry

from ass2_ros1.msg import RobotVelocity

client = None
goal = None
latest_feedback = None

new_goal = False
target_reached = False

vel_pub = None
 
def main():
    """
    Main function
    """
    rospy.sleep(2)
    global client, vel_pub

    rospy.init_node('action_client')

    vel_pub = rospy.Publisher("/robot_status", RobotVelocity, queue_size = 10)
    rospy.Subscriber("/odom", Odometry, publish_robot_velocity)

    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)

    choices = {"New/Update goal": update_goal, "Get status": print_status, "Quit": exit}
    choice_list = list(choices.keys())

    rate = rospy.Rate(10)
    while True:
        choice = get_choiche("Select what you want to do: ", choice_list)
        choices[choice_list[choice]]()
        rate.sleep()

def read_feedback(feedback):
    """
    Manages the feedback provided by the action server relative to the current goal

    :param feeback: the feedback provided by the action server
    :type feedback: PlanningFeedback
    """

    global target_reached, new_goal, latest_feedback
    latest_feedback = feedback;

    if (new_goal and feedback.stat == 'Target reached!'):
        rospy.print("Target reached !")
        target_reached = True
        new_goal = False;

def publish_robot_velocity(msg):
    """
    Publishes the robot velocity custom message starting from the odometry message received

    :param msg: the message from the Odom
    :type msg: Odometry
    """

    vel = RobotVelocity()
    vel.x = msg.pose.pose.position.x
    vel.y = msg.pose.pose.position.y
    vel.vel_x = msg.twist.twist.linear.x
    vel.vel_z = msg.twist.twist.angular.z

    vel_pub.publish(vel)

def update_goal():
    """
    Prompts the user for the new goal and communicates it to the action server
    """
    global goal
    goal = PlanningGoal()
    goal.target_pose.header.frame_id = "map"
    #TODO: inputcheck 
    goal.target_pose.pose.position.x = float(input("insert the x for the goal: "))
    goal.target_pose.pose.position.y = float(input("insert the y for the goal: "))
    client.send_goal(goal, feedback_cb=read_feedback)

def get_choiche(prompt, choice_list):
    """
    Prompts the user to make a choice between the options provided in the choice_list list

    :param prompt: the message to prompt initally before printing the choices
    :type prompt: string

    :param choice_list: the lsit of choices the user can choose from
    :type choice_list: list

    :returns: the index of the choice made by the user
    :rtype: string
    """
    user_input = 0
    input_ok = False

    while not input_ok:
        print(prompt)
        for i, choice in enumerate(choice_list):
            print(f"{i+1}. {choice}")
        
        try:
            user_input = int(input("> ")) - 1
            if user_input >=0 and user_input < len(choice_list):
                input_ok = True
        except:
            pass
        else:
            input_ok = True
        
        if not input_ok:
            print(f"Please input a valid integer between {1} and {len(choice_list)}!")
    
    return user_input

#TODO: better status print
def print_status():
    """
    Prints the status of the current goal
    """
    if (not goal):
        print("No goal set yet")
        return 
    
    print(goal)
    
    if (not latest_feedback):
        print("No feedacks received from the server yet!")
        return
    print(latest_feedback)


if __name__ == '__main__':
    main()