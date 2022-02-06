#! /usr/bin/env python

#https://answers.ros.org/question/80646/python-sending-goals-to-the-navigation-stack/

import rospy


# import ros service
from std_srvs.srv import *
from actionlib_msgs.msg import *
from move_base_msgs.msg import *
import actionlib

import math


activate_= False
client_ = None

def go_to_switch(req):
    global activate_
    activate_ = req.data
    client_.cancel_goal()
    print ("Status of node goto-rt3 = "+ str(activate_))
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def done_cb(status, result):
# Reference for terminal status values: http://docs.ros.org/diamondback/api/actionlib_msgs/html/msg/GoalStatus.html
    if status == 2:
        rospy.loginfo("Goal pose received a cancel request after it started executing, completed execution!")

    elif status == 3:
        rospy.loginfo("Goal pose  reached")
    elif status == 4:
        rospy.loginfo("Goal pose was aborted during execution by the action server due")
    elif status == 5:
        rospy.loginfo("The goal was rejected by the action server without being processed")
    else:
        rospy.loginfo("The goal can not be reached")

def main():
    global activate_, client_
    activate_ = False
    rospy.init_node('goto_pos_rt3')
    ##https://answers.ros.org/question/316592/problem-when-publishing-to-move_basegoal/
    #http://wiki.ros.org/navigation/Tutorials/SendingSimpleGoals
    client_ = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client_.wait_for_server()

    srv = rospy.Service('activate_goto', SetBool, go_to_switch)


    while not rospy.is_shutdown():

        if activate_ == False:
            continue
        else:
            activate_ = False
            goal = MoveBaseGoal()
            goal.target_pose.header.stamp = rospy.Time.now()
            goal.target_pose.pose.position.x = rospy.get_param('des_pos_x')
            goal.target_pose.pose.position.y = rospy.get_param('des_pos_y')
            goal.target_pose.header.frame_id = 'map'
            goal.target_pose.pose.orientation.w  = 1
            print ("Goal X Y = " + str(goal.target_pose.pose.position.x) + ", " + str(goal.target_pose.pose.position.y))
            state = client_.send_goal(goal, done_cb=done_cb)

        rospy.sleep(0.1)

if __name__ == "__main__":
    main()
