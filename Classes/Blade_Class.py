##### Import modules #####
import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
import Inputs as c
from copy import deepcopy
from .Segment_Class import Segment
from .Airfoil_Class import Airfoil
from itertools import zip_longest

##### Blade Class #####
# Defines the total dimensions of the wind turbine blade 
class Blade:

    ## Defines the attributes of this object
    def __init__(self, radius=1, no_segments=1, No_Blades=2, airfoil=None):
        self.radius = radius
        self.no_segments = no_segments
        self.segments = []
        self.airfoil = airfoil
        self.no_blades = No_Blades
    
    ## Defines the information that will be shown when this object is printed
    def __str__(self):
        _, chord_list, _, _, _, _, _, _ = self.read_segments()
        chord_min = min(chord_list)
        chord_max = max(chord_list)
        return f"""
              ##### Blade Attributes #####
              Radius [m]:      {format(self.radius, '.2g')}
              Tip twist [°]:   {format(np.rad2deg(self.segments[-1].twist), '.3g')}
              Root twist [°]:  {format(np.rad2deg(self.segments[0].twist), '.3g')}
              Tip chord [cm]:  {round(self.segments[-1].chord * 100, 1)}
              Root chord [cm]: {round(self.segments[0].chord * 100, 1)}
              Max chord [cm]:  {round(chord_max * 100, 1)}
              Min chord [cm]:  {round(chord_min * 100, 1)}
              """
    
    ## Create the segments for the blade
    def design_blade(self, TSR):
        self.tsr = TSR

        if isinstance(self.airfoil, Airfoil):
            dr = self.radius / self.no_segments

            for i in range(self.no_segments):
                part = Segment(dr, dr*(i+0.5)/self.radius, airfoil=self.airfoil)
                part.calc_dimensions(TSR, self.no_blades, self.radius)
                self.segments.append(part)
        
        else:
            raise TypeError('Argument provided is not of the Airfoil class')
    
    ## Method to fix the blade properties to fit within production constraints
    def fix_blade(self, Lc_min, width, height, tip):
        for segment in self.segments: # Check if within production constraints
            if segment.check_shape(Lc_min, width, height) == False or segment.check_shape(Lc_min, width, height) == 'Other':
                segment.calc_properties(segment.iter_chord(Lc_min, width, height), self.tsr, self.no_blades, self.radius, tip)

    ## Method to prepare the design for implementation into ashes (e.g. add cylinder)
    def prepare_blade(self, TSR, circ_name, Cl_circ, Cd_circ, AoA_circ, L_circ):
        for segment in self.segments: # Remove any segment less than 30mm from the center
            if segment.position * self.radius <=0.03:
                self.segments.remove(segment)

        # Add the cylinder
        circ_foil = Airfoil(circ_name, Cl_circ, Cd_circ, AoA_circ)
        cylinder = Segment(0.03, 0.03/self.radius, circ_foil)
        cylinder.calc_dimensions(TSR, self.no_blades, self.radius)
        cylinder.chord = L_circ
        self.segments.insert(0, cylinder)

        # Add extra segment to the tip, same properties as before
        tip_seg = deepcopy(self.segments[-1])
        tip_seg.position = 1
        tip_seg.length = self.radius * (1-self.segments[-1].position)
        tip_seg.dM = tip_seg.length/self.segments[-1].length * tip_seg.dM # scale the forces to the new area (don't recalculate things)
        tip_seg.dT = tip_seg.length/self.segments[-1].length * tip_seg.dT
        self.segments.insert(len(self.segments), tip_seg)

    ## Calculate the Power generation capabilities of the turbine
    def calc_power(self, wind_speed, air_density):
        pos_ratio, _, _, _, _, dT_list, dM_list, _ = np.array(self.read_segments())
        pos_list = pos_ratio * self.radius # unmake the ratio, actual positions
        ang_vel = self.tsr * wind_speed / self.radius # find the angular velocity
        
        # Integrate and calculate total force
        T_total = sum(dT_list)
        P_gen = ang_vel * np.dot(dM_list, pos_list)
        P_avail = 0.5 * air_density * wind_speed**3 * np.pi * self.radius**2

        # Calculate coefficients
        Cp = P_gen / P_avail
        Ct = T_total / (0.5 * air_density * wind_speed**2 * np.pi * self.radius**2)

        # Print results
        print(f"""
              ##### Power Characteristics #####
              Available Power [W]:     {round(P_avail,2)}
              Generated Power [W]:     {round(P_gen, 2)}
              Power Coefficient [%]:   {round(Cp*100, 2)}
              Thrust Coefficient [%]:  {round(Ct*100, 2)}
              """)
        return P_avail, P_gen, Cp, Ct
    
    ## Method to import the data from a saved .csv, and therefore recreate the blade
    def import_blade(self, file_name):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(f'{file_name}.csv')

        # Extract columns as lists
        pos_list   = df['r/R'].tolist()
        chord_list = df['Lc [m]'].tolist()
        twist_list = df['Twist [deg]'].tolist()
        lina_list  = df['a'].tolist()
        anga_list  = df['a\''].tolist()
        dT_list    = df['dT'].tolist()
        dM_list    = df['dM'].tolist()
        Re_list    = df['Re No.'].tolist()
        In_list    = df['Inputs'].tolist()
        tsr, radius, no_seg, airfoil, cl, cd, aoa = In_list[:7]
        tsr, radius, cl, cd, aoa = map(float, [tsr, radius, cl, cd, aoa])
        no_seg = int(no_seg)

        self.segments = []
        foil = Airfoil(airfoil, cl, cd, aoa)
        self.tsr = tsr
        for i in range(no_seg):
            segment = Segment(radius/no_seg, pos_list[i], foil)
            segment.chord = chord_list[i]
            segment.twist = twist_list[i]
            segment.a_lin = lina_list[i]
            segment.a_ang = anga_list[i]
            segment.dT = dT_list[i]
            segment.dM = dM_list[i]
            segment.re = Re_list[i]
            self.segments.append(segment)

    ## Method to collect the positional attributes of the blade along it's entire length
    def read_segments(self):
        pos_list    = []
        chord_list  = []
        twist_list  = []
        lina_list   = []
        anga_list   = []
        dT_list     = []
        dM_list     = []
        Re_list     = []

        for segment in self.segments:
            pos_list.append(segment.position)
            chord_list.append(segment.chord)
            twist_list.append(np.rad2deg(segment.twist))
            lina_list.append(segment.a_lin)
            anga_list.append(segment.a_ang)
            dT_list.append(segment.dT)
            dM_list.append(segment.dM)
            Re_list.append(segment.re)

        return pos_list, chord_list, twist_list, lina_list, anga_list, dT_list, dM_list, Re_list
    
    ## Method to collect the scaled airfoil coordinates for each segment
    def read_airfoils(self):
        airfoils_list = []

        for segment in self.segments:
            airfoils_list.append(segment.scaled_shape())
        
        return airfoils_list

    ## Method to save the positional data of the blade as a .csv file
    def save_csv(self, filename = 'Blade_Data'):
        
        pos_list, chord_list, twist_list, lina_list, anga_list, dT_list, dM_list, Re_list = self.read_segments()
        in_name_list = ['TSR [-]', 'Radius [m]', 'No. Segments [-]', 'Airfoil [-]', 'Cl [-]', 'Cd [-]', 'AoA_opt [deg]']
        in_list = [self.tsr, self.radius, self.no_segments, self.airfoil.name, self.airfoil.Cl, self.airfoil.Cd, np.rad2deg(self.airfoil.AoA_opt)]
        array = zip_longest(pos_list, chord_list, twist_list, lina_list, anga_list, dT_list, dM_list, Re_list, in_name_list, in_list)

        with open(f"{filename}.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['r/R', 'Lc [m]', 'Twist [deg]', 'a', 'a\'', 'dT', 'dM', 'Re No.', ' ', 'Inputs'])
            writer.writerows(array)
        
        print('Blade design data saved')

    ## Method to graph the blade design in 3D
    def display(self):
        pos_list, _, _, _, _, _, _, _ = self.read_segments()

        shapes = self.read_airfoils()
        x_coords = []
        y_coords = []
        z_coords = []

        # Find the maximum length of any entry in shapes
        max_length = max(len(shape[0]) for shape in shapes)
        
        i = -1
        for shape in shapes:
            i += 1
            # Pad the shorter lists in x_coords and y_coords with NaN to match the longest list
            x_coords.append(np.pad(shape[0], (0, max_length - len(shape[0])), constant_values=np.nan))
            y_coords.append(np.pad(shape[1], (0, max_length - len(shape[1])), constant_values=np.nan))

            # Append corresponding z_coords for each shape, repeating the z-coordinate to match max_length
            z_coords.append([pos_list[i] * self.radius] * max_length)

        # Convert lists to numpy arrays and flatten them to 1D
        x_coords = np.array(x_coords).flatten()
        y_coords = np.array(y_coords).flatten()
        z_coords = np.array(z_coords).flatten()

        # Remove any NaN entries to avoid broadcasting errors in the plot
        mask = ~np.isnan(x_coords) & ~np.isnan(y_coords)
        x_coords = x_coords[mask]
        y_coords = y_coords[mask]
        z_coords = z_coords[mask]

        # Determine the range for each axis using min/max on valid coordinates
        x_min, x_max = np.min(x_coords), np.max(x_coords)
        y_min, y_max = np.min(y_coords), np.max(y_coords)
        z_min, z_max = np.min(z_coords), np.max(z_coords)

        # Get the global range for equal scaling
        all_min = min(x_min, y_min, z_min)
        all_max = max(x_max, y_max, z_max)
        
        # Create padding for all axes
        padding = 0.1 * (all_max - all_min)
        all_min -= padding
        all_max += padding

        # Graphing
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x_coords, y_coords, z_coords, c=z_coords, cmap='viridis')  # Use scatter for point clouds
        
        # Set equal scaling for all axes
        ax.set_xlim([all_min, all_max])
        ax.set_ylim([all_min, all_max])
        ax.set_zlim([all_min, all_max])

        # Set labels
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()
