##### Import modules #####
import numpy as np
import matplotlib.pyplot as plt
import copy
from Classes import Airfoil, Segment, Blade

##### Inputs #####
TSR = 5.67
radius = 0.45
no_segments = 10
no_blades = 2
tol = 0.05 # 5% tolerance for iterations

##### Prepare for Iterations #####
diff = 100
Re = float(input('Reynolds Number:'))
Re_list = [Re]

##### Iterations #####
while diff >= tol:
    AoA = float(input('\nAoA_opt of the airfoil:'))
    Cl = float(input('Cl of the airfoil:'))
    Cd = float(input('Cd of the airfoil:'))

    foil = Airfoil(None, Cl, Cd, AoA)
    piece = Segment(0, 0.7, TSR, no_blades, radius, airfoil=foil)
    Re_new = piece.re

    diff = abs(Re - Re_new)/Re
    Re_list.append(Re_new)
    Re = Re_new

    if diff < tol:
        print(f"""##### Iterations completed!! #####
        Final Re:      {Re_list[-1]}
        Final Cl:      {Cl}
        Final Cd:      {Cd}
        Final Cl/Cd:   {Cl/Cd}
        Final AoA_opt: {AoA}""")
        break

    else:
        print(f"New Re: {Re * 10**-6}")