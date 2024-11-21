##### Import modules #####
import numpy as np

##### Airfoil class #####
# Defines the cross sectional section of the wind turbine blade
class Airfoil:

    ## Defines the attributes of this object
    def __init__(self, name=None, Cl=0, Cd=0, AoA_opt=0):
        self.name = name                    # String for name of airfoil being used, to provide the shape
        self.Cl = Cl                        # Lift coefficient of airfoil at required Reynolds number
        self.Cd = Cd                        # Drag coefficient of airfoil at required Reynolds number
        self.AoA_opt = np.deg2rad(AoA_opt)  # Optimal angle of attack. Input in Degrees, calculates in Radians
    
    ## Defines the information that will be shown when this object is printed
    def __str__(self):
        return f"""##### Airfoil Attributes #####
                Airfoil:     {self.name} 
                Cl:          {format(self.Cl, '.2g')}
                Cd:          {format(self.Cd, '.2g')}
                Optimal AoA: {format(np.rad2deg(self.AoA_opt), '.2g')}"""

    ## Method to take the shape coordinates of the airfoil from the Airfoil_Data folder
    def shape(self):
        with open(f'Airfoil_Data/{self.name}') as file:
            x_coords = []
            y_coords = []

            next(file)
            for line in file:
                columns = line.strip().split()

                x_coords.append(float(columns[0]))
                y_coords.append(float(columns[1]))

        # Calculate the mean of the x and y coordinates
        x_mean = sum(x_coords) / len(x_coords)
        y_mean = sum(y_coords) / len(y_coords)

        # Center the coordinates around the origin
        x_coords_centered = [x - x_mean for x in x_coords]
        y_coords_centered = [y - y_mean for y in y_coords]

        return [x_coords_centered, y_coords_centered]