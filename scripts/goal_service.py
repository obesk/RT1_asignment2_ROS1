#! /usr/bin/env python

import rospy 
import sys

from ass2_ros1.srv import Goal, GoalResponse

def main():
    rospy.init_node("service_node")
    service = rospy.Service("/last_goal", Goal, retrieve_last_target)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rate.sleep()

def send_last_goal(req):
    pos_x = float(rospy.get_param("/des_pos_x"))
    pos_y = float(rospy.get_param("/des_pos_y"))
    return GoalResponse(pos_x, pos_y)


if __name__ == '__main__':
    main()