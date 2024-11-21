## This file is used to provide the design inputs for the rest of the programme
## Change values here, and then run any of the other files you need

##### Airfoil Inputs #####
foil_name = 'S826'          # Name of the airfoil (same as in Airfoil_Data)
Cl = 1.304                  # [-], assumed lift coefficient
Cd = 0.0172                 # [-], assumed drag coefficient
AoA_opt = 6.5               # [°], degrees
max_thickness = 0.14        # [-], thickness over chord ratio, t/c

##### Design Inputs #####
TSR = 4.91                  # [-], tip speed ratio
radius = 0.45               # [m], radius of the blade
no_blades = 2               # [-], number of blades
no_segments = 15            # [-], number of segments per blade

##### Production Constraints ######
Lc_min = 0.04               # [m], minimum allowable chord length
t_min = 0.005               # [m], minimum allowable thickness
width = 0.098               # [m], width of the manufacturing material
height = 0.048              # [m], height of the manufacturing material

circ_name = 'Circle'        # Name of the coordinates in Airfoil_Data
Cl_circ = 0                 # [-], lift coefficient of the cylinder 
Cd_circ = 0.5               # [-], drag coefficient of the cylinder
AoA_circ = 0                # [°], optimal angle of attack of the cylinder
L_circ = 0.048              # [m], chord of the cylinder

##### Physical Constants #####
windspeed = 12              # [m/s], speed of the wind
air_density = 1.225         # [kg/m^3], air density (no shit)
viscosity = 1.47*10**(-5)   # [kg/ms], viscosity of the wind
