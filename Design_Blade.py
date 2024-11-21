##### Import modules #####
from Classes import Airfoil, Segment, Blade
import Inputs as c

##### Calculations #####
Foil = Airfoil(c.foil_name, c.Cl, c.Cd, c.AoA_opt)

Design = Blade(c.radius, c.no_segments, c.no_blades, Foil)
Design.design_blade(c.TSR)
print(Design)
Design.calc_power(c.windspeed, c.air_density)

Design.fix_blade(c.Lc_min, c.width, c.height, tip=True) # Fix the blade twice, to ensure no mistakes
Design.fix_blade(c.Lc_min, c.width, c.height, tip=True)
Design.prepare_blade(c.TSR, c.circ_name, c.Cl_circ, c.Cd_circ, c.AoA_circ, c.L_circ)
print(Design)
_, _, cp, _ = Design.calc_power(c.windspeed, c.air_density)
Design.save_csv(f'Blade_Designs/TSR{int(c.TSR*100)}_{c.foil_name}_{int(cp*10000)}') # Naming convention: TSR{give}_{airfoil name}_{Cp w/o decimal}
Design.display()