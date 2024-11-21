Welcome to Group 22B's python code for the Design of a Wind Turbine course TEP4175!!!

This file will summarize how this code works. Firstly, the code was approached through an object oriented programming style, through the use of classes. These are found in the classes folder, and define three classes:
Airfoil, saves the aerodynamic information of the airfoil being used, as well as it's shape
Segment, represents the blade element, and calculates its properties
Blade, adds the segments together and unifies it all

Inputs.py is where the inputs used in the blade design are given
The python file Design_Blade.py is where the classes were used together to create the blade
Iterate_Re.py was used to iterate the reynolds number for a specific airfoil, used in conjunction with Ashes xfoil solver to find the CL/CD of each airfoil
Optim_TSR.py was used to iterate over various TSR values to find the optimal one to design for
