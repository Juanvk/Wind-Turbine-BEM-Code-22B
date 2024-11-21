##### Import modules #####
import numpy as np
import matplotlib.pyplot as plt
from Classes import Airfoil, Segment, Blade
import Inputs as c

##### Testing #####
foil = Airfoil(c.foil_name, c.Cl, c.Cd, c.AoA_opt)

tsr_list = np.arange(3, 6.5, 0.01)
Cp_list = []
Lc_list = []

for TSR in tsr_list:
    Test_blade = Blade(c.radius, c.no_segments, c.no_blades, airfoil=foil)
    Test_blade.design_blade(TSR)
    Test_blade.fix_blade(c.Lc_min, c.width, c.height, tip=True)
    Test_blade.fix_blade(c.Lc_min, c.width, c.height, tip=True)

    _, _, Cp, _ = Test_blade.calc_power(c.windspeed, c.air_density)
    Cp_list.append(Cp * 100)
    _, chord_list, _, _, _, _, _, _ = Test_blade.read_segments()
    Lc_list.append(min(chord_list))

# Finding the maximum
Cp_max = max(Cp_list)
idx = Cp_list.index(Cp_max)
tsr_max = tsr_list[idx]
chord_max = Lc_list[idx]

print(f'Maximal Efficiency of {round(Cp_max, 2)}% at TSR of {tsr_max} with min chord {chord_max}')

# First plot - Cp_list vs. tsr_list
plt.plot(tsr_list, Cp_list, label='Cp vs TSR', color='b')
plt.xlabel('Tip Speed Ratio (TSR) [-]')
plt.ylabel('Coefficient of Power (Cp) [%]')
plt.grid()
plt.legend()
plt.show()