.. Final assignment documentation master file, created by
   sphinx-quickstart on Fri Feb 25 16:42:41 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Final assignment's documentation!
********************************************
This is a Final assignment of Research track 1. The program consists of 2 nodes including :mod:`ui_rt3` and :mod:`goto_rt3`

Tasks
==========================================
- Building the software for receiving the co-ordinate and navigate robot
- Building the software to control the robot via keyboard with/without assistance to avoid collisions

Running
======================
.. code-block:: bash

   $ roscore
   $ rosluanch final_assignment final_assignment.launch

Once the program run correctly there are 5 consoles: User input node, keyboard control node, navigation node, move_base node and simulation node.

Documentation for the code
**************************
.. toctree::
   :maxdepth: 2
   :caption: Contents:




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


goto_rt3 Module
=====================
.. automodule:: scripts.goto_rt3
    :members:

ui_rt3 Module
=====================
.. automodule:: scripts.ui_rt3
    :members:
