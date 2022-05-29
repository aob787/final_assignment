Final assignment - Research Track 1
================================

Some parts of respiratory was retrived from https://github.com/CarmineD8/final_assignment and https://github.com/CarmineD8/slam_gmapping

For RT2
--------------------
For the documentation go to https://aob787.github.io/final_assignment/

For testing jupyter notebook

  First: Open Jupyter notebook file "Jupyter_ui.ipynb"

  Second:
  ```Shell
  roscore
  rosluanch final_assignment final_assignment_rt2.launch
  ```
*For the joystick you can you both teleop_twist_keyboard or joystick in Jupyter_ui

Further improvements (that can be improved):

  - Improve the UI e.g., put all of the graph in to the tabs like I did in switching mode for robot.

  - Improve the graph update efficiency, right now it a bit laggy. Maybe we can find the optimal solution for graph especially for the robot path since it may contains many data points to display.

  - Jupyter code is a bit messy since I tried not to touch previous code (i.e., the one that has been submitted in RT1) and they are not design to do this tasks, for example showing the success and failure in histogram, because that code isn't integrated in UI. So, I have to create a new ros params to send the data.


Tasks
--------------------
-Building the software for recieving the co-ordinate and nagivate robot

-Building the software to control the robot via keyboard with/without assistance to avoid collisions

Installing and running
----------------------
You can run the code by using

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
