#! /usr/bin/env python

import rospy
import actionlib

import time

from assignment_2_2024.msg import PlanningAction, PlanningGoal 

client = None
goal = None
latest_feedback = None

new_goal = False
target_reached = False
 
def main():
    global client

    rospy.init_node('planning_client')
    client = actionlib.SimpleActionClient('/reaching_goal', PlanningAction)
    client.wait_for_server()

    choices = {"New/Update goal": update_goal, "Get status": print_status, "Quit": exit}
    choice_list = list(choices.keys())

    while True:
        choice = get_choiche("Select what you want to do: ", choice_list)
        choices[choice_list[choice]]()
        time.sleep(1)

def read_feedback(feedback):
    global target_reached, new_goal, latest_feedback
    latest_feedback = feedback;

    if (new_goal and feedback.stat == 'Target reached!'):
        rospy.print("Target reached !")
        target_reached = True
        new_goal = False;

def update_goal():
    global goal
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