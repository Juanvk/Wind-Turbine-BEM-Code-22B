##### Import modules #####
from Classes import Airfoil, Segment, Blade
import Inputs as c
import matplotlib.pyplot as plt
import numpy as np

##### Calculations #####
Foil = Airfoil(c.foil_name, c.Cl, c.Cd, c.AoA_opt)

Design = Blade(c.radius, 15, c.no_blades, Foil)
Design.design_blade(c.TSR)

airfoil_list = Design.read_airfoils()
pos_list, chord_list, twist_list, lina_list, anga_list, dT_list, dM_list, Re_list = Design.read_segments()

seg_3 = airfoil_list[2]
x_constraint = [c.width/2, c.width/2, -c.width/2, -c.width/2, c.width/2]
y_constraint = [-c.height/2, c.height/2, c.height/2, -c.height/2, -c.height/2]

Design.fix_blade(c.Lc_min, c.width, c.height, tip=True)

airfoil1_list = Design.read_airfoils()
seg3_fix1 = airfoil1_list[2]

Design.fix_blade(c.Lc_min, c.width, c.height, tip=True)

airfoil2_list = Design.read_airfoils()
seg3_fix = airfoil2_list[2]
posfix_list, chordfix_list, twistfix_list, linafix_list, angafix_list, dTfix_list, dMfix_list, Refix_list = Design.read_segments()

# plt.plot(seg_3[0], seg_3[1], label='Original segment')
# plt.plot(seg3_fix1[0], seg3_fix1[1], label='1st iteration')
# plt.plot(seg3_fix[0], seg3_fix[1], label='2nd iteration')
# plt.plot(x_constraint, y_constraint, color="black", linewidth=2)
# plt.legend()
# plt.grid()
# plt.show()

plt.plot(pos_list, chord_list, label='Unmodified design')
plt.plot(posfix_list, chordfix_list, label='Modified design')
plt.xlabel('Position r/R [-]')
plt.ylabel('Chord length [m]')
plt.legend()
plt.grid()
plt.show()

plt.plot(pos_list, twist_list, label='Unmodified design')
plt.plot(posfix_list, twistfix_list, label='Modified design')
plt.xlabel('Position r/R [-]')
plt.ylabel('Twist angle [°]')
plt.legend()
plt.grid()
plt.show()