# Simple-2DFrame
*A Simple 2D Frame Analysis Solver:*

This program calculates the reaction forces and moments for a two legged 2D Frame Structure, and then plots the shear and moment diagrams for each member. The illustrated inputs shown in helper.png (P, w1, w2, l, and s) are shown only in Member 2, but for this program, the inputs can be also applied to the other members (1 & 3). The w1 will always start from the end on a member, while w2 can be moved depending on the value of 'l'. Refer to helper.png as a reference. ***Note that the inputs are in US units.*** 

Assumptions: 
- External Applied Loads are positive when pointing toward the member, and is negative when pointing away from the member. 
- Structure has a roller at one end, and is pinned at the other end (refer to image in helper.png) 

Inputs: 
- loading condtions (P, w1, w2)
- lengths of members (s, l, x); (shown in helper.png)

Outputs:
- Reactions and moment values at the supports
- Shear and Moment Diagrams for each Member (1, 2, 3). 

## Setup 
In order to use this program, curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py > python get-pip.py > pip3 install matplotlib > now open Frame2D.py file > run IDLE > insert your values > obtain outputs 


## Setup 
In order to use this program, open the terminal and download curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py > python get-pip.py. This is to install the pip package into Python.
Now with the pip installed into python, install the required libriaries for this program with matplotlib (more is shown in requirements.txt)

## How to use the Program
First, the OOP (Object Oriented Program) is initiated into the source.py with a main class called Member. 
