#! /usr/bin/env python
## rosrun final_assignment ui-rt3.py
## rosrun final_assignment goto-rt3.py
##rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=cmd_vel_kb


import rospy
from std_srvs.srv import *
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

#Parameters
obstacle_detection_range = 1

srv_activate_goto_ = None
mode_ = 0
sub_laser_ = None
sub_cmd_vel_kb_ = None
pub_cmd_vel_ =None
able_to_move_ = [0, 0, 0, 0, 0] #% array including right fringht front fleft and left
vel_msg = Twist()

def check_obstruc(regions, key, index):
    global able_to_move_
    if regions[key] > obstacle_detection_range :
        able_to_move_[index] = 1
    else :
        able_to_move_[index] = 0

def clbk_laser(msg): #this part of function was obtianed from obstacle_avoidance.py
    global vel_msg
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }
    check_obstruc(regions, 'right', 0)
    check_obstruc(regions, 'fright', 1)
    check_obstruc(regions, 'front', 2)
    check_obstruc(regions, 'fleft', 3)
    check_obstruc(regions, 'left', 4)

    ## If there is any obstacle in the direction that robot heading to it's going to stop
    if able_to_move_[0] == 0 and vel_msg.angular.z < 0 :
        vel_msg.angular.z = 0
    if able_to_move_[1] == 0 and vel_msg.linear.x > 0 and vel_msg.angular.z < 0 :
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
    if able_to_move_[2] == 0 and vel_msg.linear.x > 0 :
        vel_msg.linear.x = 0
    if able_to_move_[3] == 0 and vel_msg.linear.x > 0  and vel_msg.angular.z > 0:
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
    if able_to_move_[4] == 0 and vel_msg.angular.z > 0:
        vel_msg.angular.z = 0
    pub_cmd_vel_.publish(vel_msg)


def clbk_twist_kb(msg):
    global  mode_
    global sub_laser_, sub_cmd_vel_kb_, vel_msg_, pub_cmd_vel_, vel_msg
    print("recied")
    print ("Mode of robot: " + str(mode_))

    if mode_ == 2:
        rospy.loginfo("Received a /cmd_vel message!")
        rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
        rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))
        vel_msg.linear.x = msg.linear.x
        vel_msg.linear.y = msg.linear.y
        vel_msg.linear.z = msg.linear.z
        vel_msg.angular.x = msg.angular.x
        vel_msg.angular.y = msg.angular.y
        vel_msg.angular.z = msg.angular.z
        pub_cmd_vel_.publish(vel_msg)
    elif mode_ == 3:
        vel_msg.linear.x = msg.linear.x
        vel_msg.linear.y = msg.linear.y
        vel_msg.linear.z = msg.linear.z
        vel_msg.angular.x = msg.angular.x
        vel_msg.angular.y = msg.angular.y
        vel_msg.angular.z = msg.angular.z

        ##check before publish in order to avoid the issue that user hold on the direction that was obstracted
        if able_to_move_[0] == 0 and msg.angular.z < 0:
            vel_msg.angular.z = 0
        if able_to_move_[1] == 0 and msg.angular.z < 0 and msg.linear.x > 0:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
        if able_to_move_[2] == 0 and msg.linear.x > 0 :
            vel_msg.linear.x = 0
        if able_to_move_[3] == 0 and msg.linear.x > 0 and msg.angular.z > 0:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
        if able_to_move_[4] == 0 and msg.angular.z > 0:
            vel_msg.angular.z = 0
        pub_cmd_vel_.publish(vel_msg)
"""
teleop_twist_keyboard
https://github.com/ros-teleop/teleop_twist_keyboard/blob/master/teleop_twist_keyboard.py
Moving around:
   u    i    o
   j    k    l
   m    ,    .
    (x,y,z,yaw)
'i':(1,0,0,0),
'o':(1,0,0,-1),
'j':(0,0,0,1),
'l':(0,0,0,-1),
'u':(1,0,0,1),
',':(-1,0,0,0),
'.':(-1,0,0,1),
'm':(-1,0,0,-1),
"""

def main():
    global srv_activate_goto_, mode_
    global sub_laser_, sub_cmd_vel_kb_, vel_msg_, pub_cmd_vel_
    time.sleep(2)
    rospy.init_node('main_rt3')

    sub_laser_ = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    sub_cmd_vel_kb_ = rospy.Subscriber("/cmd_vel_kb", Twist, clbk_twist_kb)
    pub_cmd_vel_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    global srv_activate_goto_, srv_activate_kb_control_, srv_activate_auto_avoiding_
    srv_activate_goto_ = rospy.ServiceProxy('/activate_goto', SetBool)

    while not rospy.is_shutdown():
        try:
            mode_ = int(input("Please input the mode of robot"))
            print ("Mode of robot: " + str(mode_))
            if mode_ == int(1):
                sub_laser_.unregister()
                a = float(input("new x position:"))
                b = float(input("new y position:"))
                rospy.set_param('des_pos_x',a)
                rospy.set_param('des_pos_y',b)
                resp = srv_activate_goto_(True)
                print ("Change mode succes")
            elif mode_ == int(2):
                sub_laser_.unregister()
                resp = srv_activate_goto_(False)
                print ("Change mode succes")
            elif mode_ == int(3):
                sub_laser_ = rospy.Subscriber('/scan', LaserScan, clbk_laser)
                resp = srv_activate_goto_(False)
                print ("Change mode succes")

        except:
            print("Pleasr inpun nuber 1 2 or 3")





if __name__ == "__main__":
    main()
