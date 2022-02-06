#! /usr/bin/env python

import rospy
# import ros message
from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf import transformations
# import ros service
from std_srvs.srv import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseActionGoal, MoveBaseGoal
import time

import math

srv_client_go_to_point_ = None
srv_client_wall_follower_ = None
yaw_ = 0
yaw_error_allowed_ = 5 * (math.pi / 180)  # 5 degrees
position_ = Point()
desired_position_ = Point()
desired_position_.x = 0
desired_position_.y = 0
desired_position_.z = 0
activate_ = False
regions_ = None
state_desc_ = ['Go to point', 'wall following']
state_ = 0
# 0 - go to point
# 1 - wall following


def go_to_switch(req):
    global activate_
    activate_ = req.data
    if activate_ == False:
        print("Reset goal")
    print ("Status of node goto-rt3 = "+ str(activate_))
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res


def main():
    time.sleep(2)
    global activate_

    rospy.init_node('goto_pos_rt3')
    ##https://answers.ros.org/question/316592/problem-when-publishing-to-move_basegoal/
    publisher = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=1,latch=True)
    move_base_goal = MoveBaseGoal()

    srv = rospy.Service('activate_goto', SetBool, go_to_switch)


    while not rospy.is_shutdown():

        if activate_ == False:
            continue
        else:
            activate_ = False
            desired_position_ = Point()
            goal = MoveBaseActionGoal()
            move_base_goal.target_pose.pose.position.x = rospy.get_param('des_pos_x')
            move_base_goal.target_pose.pose.position.y = rospy.get_param('des_pos_y')
            move_base_goal.target_pose.header.frame_id = 'map'
            move_base_goal.target_pose.pose.orientation.w  = 1
            print ("Goal X Y = " + str(move_base_goal.target_pose.pose.position.x) + ", " + str(move_base_goal.target_pose.pose.position.y))
            goal.goal = move_base_goal
            publisher.publish(goal)
            print ("Publish sucess")
            rospy.spin()


if __name__ == "__main__":
    main()
