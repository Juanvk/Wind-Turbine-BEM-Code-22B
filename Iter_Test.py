##### Import modules #####
import numpy as np
import matplotlib.pyplot as plt
from Classes import Airfoil, Segment, Blade
import Inputs as c

##### Testing #####
foil = Airfoil(c.foil_name, c.Cl, c.Cd, c.AoA_opt)

seg_list = np.arange(1, 500, 1)
Cp_list = []

for no_segments in seg_list:
    Test_blade = Blade(c.radius, no_segments, c.no_blades, airfoil=foil)
    Test_blade.make_segment(c.TSR)

    # print(Test_blade)
    _, _, Cp, _, = Test_blade.calc_power(c.TSR, c.windspeed, c.air_density)
    Cp_list.append(Cp * 100)

plt.plot(seg_list, Cp_list)
plt.xlabel('No. of Segments [-]')
plt.ylabel('Coefficient of Power [-]')
plt.grid()
plt.show()