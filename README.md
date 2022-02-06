Final assignment - Research Track 1
================================

Some parts of respiratory was retrived from https://github.com/CarmineD8/final_assignment and https://github.com/CarmineD8/slam_gmapping

Tasks
--------------------
-Building the software for recieving the co-ordinate and nagivate robot

-Building the software to control the robot via keyboard with/without assistance to avoid collisions

Installing and running
----------------------
Require package: ros navigation stack and teleop_twist_keyboard and also required xterm in ubuntu.

```Shell
sudo apt update
sudo apt-get install ros-<your_ros_distro>-navigation
sudo apt-get install ros-noetic-teleop-twist-keyboard
sudo apt install xterm
```

To run you need to build/complie first using

```Shell
catkin_make
```
Then you can run the code by using

```Shell
roscore
rosluanch final_assignment final_assignment.launch
```

or in case of having trobles with x-term

```Shell
roscore
rosluanch final_assignment simulation_gmapping.launch
rosluanch final_assignment move_base.launch
rosrun final_assignment ui_rt3.py
rosrun final_assignment goto_rt3.py
rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=cmd_vel_kb
```

Once the program run correctly there are 5 consoles: User input node, keyboard control node, navigation node, move_base node and simulation node.

Pseudocode
--------------------
This pseudocode consist of 2 programs.

ui_rt3.py

```python
main:
  init Publisher(pub to cmd_vel)
  init Subscriber(Sub to laser scanner and cmd_vel_kb)
  init service(to toggle goto_rt3.py)
  While(true){
    usr_input = recieve_user_input()
    if usr_input == 1:
      toggle_goto_rt3.py(True)
      x, y  = recieve_user_input()
      assign_val_to_parameter(x,y)
    if usr_input == 2: #without assistance
      toggle_goto_rt3.py(False)
    if usr_input == 3: #turn on assistance
      toggle_goto_rt3.py(False)


callback_function_for_laser_scanner:
  recive msg
  split_data_into_5_section   #(left, front-left, front, front-right, right)
  check_are_there_any_obstacles
  if mode == 3: #turn on assistance
    for i in (left, front-left, front, front-right, right)
      if there is obstacle:
        reduce the vel of that direction to 0
    pub_cmd_vel_.publish(vel_msg)

call_back_function_for_cmd_vel_kb: #(this function will recieve the msg fron twist keyboard)
   if mode == 2: #without assistance
      pub_cmd_vel_.publish(vel_msg)
   if mode == 3: #turn on assistance
     for i in (left, front-left, front, front-right, right)
       if there is obstacle:
         reduce the vel of that direction to 0
     pub_cmd_vel_.publish(vel_msg)
```
goto_rt3.py

```python
main:
  init action (move_base)
  init service (recieve the toggle from ui_rt3,py)
  While(true){
    if active == false:
      continue
    else:
      active = false
      read desired coordinatr #using ros_get_param
      set_the_goal_pos(x, y) with callback function with it done (done_cb)

service:
  activate = req
  cancel goal

done_cb:
  print(read_return_data_from_move_base)

```


Implemented code
--------------------
The ui_rt3.py aka. main code will use to switch modes of robots between autonomously reach a x,y coordinate inserted by the user and  let the user drive the robot with the keyboard with/without assistance.

The goto_rt.py take the coordinate from ui_rt3 then using action to set the goal of move_base node.

For more details please refer to comments in codes.

For the teleop_twist_keyboard please refer to https://github.com/ros-teleop/teleop_twist_keyboard.
