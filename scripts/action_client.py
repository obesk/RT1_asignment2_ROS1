#! /usr/bin/env python

from assignment_2_2024.msg import PlanningAction, PlanningGoal

import rospy
import actionlib

import time

from nav_msgs.msg import Odometry

from ass2_ros1.msg import RobotVelocity
from ass2_ros1.srv import RunInfo, RunInfoResponse

MS_TO_KMH = 3.6

client = None
goal = None
latest_feedback = None

goals_reached = 0;
goals_canceled = 0;

new_goal = False
target_reached = False

vel_pub = None
 
def main():
    rospy.sleep(2)
    global client, vel_pub

    service = rospy.Service("/run_info", RunInfo, run_info)

    rospy.init_node('action_client')

    vel_pub = rospy.Publisher("/robot_status", RobotVelocity, queue_size = 10)
    vel_pub = rospy.Publisher("/robot_actual_velocity", RobotVelocity, queue_size = 10)
    rospy.Subscriber("/odom", Odometry, publish_robot_velocity)

    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)

    choices = {"New/Update goal": update_goal, "Get status": print_status, "Quit": exit}
    choice_list = list(choices.keys())

    rate = rospy.Rate(10)
    while True:
        choice = get_choiche("Select what you want to do: ", choice_list)
        choices[choice_list[choice]]()
        rate.sleep()

def run_info(req):
    return RunInfoResponse(goals_reached, goals_canceled)

def read_feedback(feedback):
    global target_reached, new_goal, latest_feedback, goals_reached
    latest_feedback = feedback;

    if (new_goal and feedback.stat == 'Target reached!'):
        rospy.print("Target reached !")
        target_reached = True
        new_goal = False
        goals_reached = goals_reached + 1

def publish_robot_velocity(msg):
    vel = RobotVelocity()
    vel.x = msg.pose.pose.position.x
    vel.y = msg.pose.pose.position.y
    vel.vel_x = msg.twist.twist.linear.x
    vel.vel_z = msg.twist.twist.angular.z
    vel_pub.publish(vel)

    actual_velocity = RobotVelocity()
    actual_velocity.x = msg.twist.twist.linear.x * MS_TO_KMH;
    actual_velocity.y = msg.twist.twist.linear.y * MS_TO_KMH;
    vel_pub.publish(actual_velocity)


def update_goal():
    global goal, new_goal, goals_canceled

    if (goal): # if there was a goal before we consider the first goal canceled
        goals_canceled = goals_canceled + 1

    new_goal = True
    goal = PlanningGoal()
    goal.target_pose.header.frame_id = "map"
    #TODO: inputcheck 
    goal.target_pose.pose.position.x = float(input("insert the x for the goal: "))
    goal.target_pose.pose.position.y = float(input("insert the y for the goal: "))
    client.send_goal(goal, feedback_cb=read_feedback)

    

def get_choiche(prompt, choice_list):
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