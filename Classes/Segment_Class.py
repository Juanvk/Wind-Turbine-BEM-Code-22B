##### Import modules #####
import numpy as np
from scipy.misc import derivative
import copy
from .Airfoil_Class import Airfoil
import Inputs as c

##### Segment class #####
# Defines a 3d volume of the blade, at a specific position along the blade 
class Segment:

    ## Defines the attributes of this object
    def __init__(self, length=0, position=0, airfoil=None):
        # Inputs
        self.length = length                # how long the segment is AKA dr
        self.position = position            # in terms of r/R (length/Total Radius)

        if isinstance(airfoil, Airfoil):
            self.airfoil = airfoil
        
        else:
            raise TypeError('Argument provided is not of the Airfoil class')
    
    ## Defines the information that will be shown when this object is printed
    def __str__(self):
        return f"""
                ##### Segment Attributes #####
                Airfoil:                  {self.airfoil.name}
                Chord length:             {format(self.chord, '.2g')}
                Twist:                    {format(np.rad2deg(self.twist), '.3g')}
                Length:                   {format(self.length, '.2g')}
                Position [r/R]:           {format(self.position, '.2g')}
                Linear Induction Factor:  {format(self.a_lin, '.3g')}
                Angular Induction Factor: {format(self.a_ang, '.3g')}"""
    
    ## Calculate the dimensions and values for the segment
    def calc_dimensions(self, TSR, No_Blades, Radius, air_density=c.air_density, wind_speed=c.windspeed, viscosity=c.viscosity):
        self.tsr = TSR * self.position
        roots = np.roots([16, -24, (9-3*self.tsr**2), (-1+self.tsr**2)])

        for a_lin in roots: # remove roots that lead to impossible answers
            if np.isreal(a_lin) and 0<= a_lin <= 0.5:
                self.a_lin = a_lin
                break
        
        self.a_ang = (1 - 3*self.a_lin) / (4*self.a_lin - 1)

        self.flow = np.arctan((1-self.a_lin)/((1+self.a_ang) * self.tsr))
        rel_velocity = wind_speed * (1-self.a_lin) / np.sin(self.flow)
        self.twist = self.flow - self.airfoil.AoA_opt

        self.C_a = self.airfoil.Cl * np.cos(self.flow) + self.airfoil.Cd * np.sin(self.flow)
        self.C_m = self.airfoil.Cl * np.sin(self.flow) - self.airfoil.Cd * np.cos(self.flow)

        self.chord = (8 * np.pi * self.a_lin * self.tsr * np.sin(self.flow)**2 * Radius) / ((1-self.a_lin) * No_Blades * self.C_a * TSR)

        # tip_loss = 2/np.pi*np.arccos(np.e**(-1*(No_Blades*(1 - self.position))/(2*self.position*np.sin(self.flow))))

        self.dM = 0.5 * air_density * rel_velocity**2 * self.C_m * self.chord * self.length * No_Blades # * tip_loss
        self.dT = 0.5 * air_density * rel_velocity**2 * self.C_a * self.chord * self.length * No_Blades # * tip_loss

        self.re = air_density * rel_velocity * self.chord / viscosity

    # Calculate the properties of the segment given a specific chord
    def calc_properties(self, chord, TSR, No_Blades, Radius, tip, air_density=c.air_density, wind_speed=c.windspeed, viscosity=c.viscosity):
        try:
            self.chord = chord    
            self.tsr = TSR * self.position
            self.a_lin = self.find_induction(chord, TSR, No_Blades, Radius)
            
            self.a_ang = (1 - 3 * self.a_lin) / (4 * self.a_lin - 1)

            self.flow = np.arctan((1 - self.a_lin) / ((1 + self.a_ang) * self.tsr))
            rel_velocity = wind_speed * (1 - self.a_lin) / np.sin(self.flow)
            self.twist = self.flow - self.airfoil.AoA_opt

            self.C_a = self.airfoil.Cl * np.cos(self.flow) + self.airfoil.Cd * np.sin(self.flow)
            self.C_m = self.airfoil.Cl * np.sin(self.flow) - self.airfoil.Cd * np.cos(self.flow)

            if tip:
                tip_loss = 2 / np.pi * np.arccos(np.e**(-1 * (No_Blades * (1 - self.position)) / (2 * self.position * np.sin(self.flow))))
            else:
                tip_loss = 1

            self.dM = 0.5 * air_density * rel_velocity**2 * self.C_m * self.chord * self.length * No_Blades * tip_loss
            self.dT = 0.5 * air_density * rel_velocity**2 * self.C_a * self.chord * self.length * No_Blades * tip_loss

            self.re = air_density * rel_velocity * self.chord / viscosity
            
        except Exception as e:
            # If there is an exception, set all the outputs to NaN
            self.a_lin = np.nan
            self.a_ang = np.nan
            self.flow = np.nan
            self.twist = np.nan
            self.C_a = np.nan
            self.C_m = np.nan
            self.dM = np.nan
            self.dT = np.nan
            self.re = np.nan
            print(f"Error in calc_properties: {e}")

    # Method to calculate the new linear induction factor, given a chord length
    def find_induction(self, chord, TSR, No_Blades, Radius, wind_speed=c.windspeed, viscosity=c.viscosity):
        def f(a):
            return (No_Blades * ((wind_speed * (1 - a)) / 
                    np.sin(np.arctan((1 - a) / (TSR * self.position * (1 + (1 - 3 * a) / (4 * a - 1))))))**2 *
                    (self.airfoil.Cl * np.cos(np.arctan((1 - a) / (TSR * self.position * (1 + (1 - 3 * a) / (4 * a - 1))))) +
                    self.airfoil.Cd * np.sin(np.arctan((1 - a) / (TSR * self.position * (1 + (1 - 3 * a) / (4 * a - 1)))))) * 
                    chord * self.length - wind_speed**2 * 4 * a * (1 - a) * np.pi * self.position * Radius * self.length)

        diff = 1
        a_lin = 1 / 3
        i = 0
        while diff >= 0.01:  # Newton method for solving non-linear equations (max 100 iterations)
            i += 1
            a_new = a_lin - f(a_lin) / derivative(f, a_lin, dx=1e-6)
            diff = abs(a_lin - a_new)
            a_lin = a_new
            if i >= 100:  # If iterations don't converge
                raise Exception(f"Failed to converge after 100 iterations. Linear induction factor: {a_lin}, tip speed ratio: {TSR}")
        
        return a_lin
    
    ## Method to check if the shape of the airfoil fits into the production constraints (True = fits, False = not a fit)
    def check_shape(self, Lc, width, height):
        x_coords, y_coords = self.scaled_shape()

        if self.chord <= Lc or self.chord*c.max_thickness <= c.t_min:
            return 'Other'

        for x in x_coords:
            if x >= width/2 or x <= -width/2:
                return False
        
        for y in y_coords:
            if y >= height/2 or y <= -height/2:
                return False
        
        return True

    ## Method to reduce the chord size by 1% till it fits the constraints
    def iter_chord(self, Lc, width, height):
        self_copy = copy.deepcopy(self)

        check = self_copy.check_shape(Lc, width, height)
        while check == 'Other':
            self_copy.chord = self_copy.chord * 1.01
            check = self_copy.check_shape(Lc, width, height)
            if check == True:
                return self_copy.chord
            
        while check == False:
            self_copy.chord = self_copy.chord * 0.99
            check = self_copy.check_shape(Lc, width, height)
            if check == True:
                return self_copy.chord
    
    ## Method to reduce the twist angle by 1% till it fits the constraints
    def iter_twist(self, Lc, width, height):
        self_copy = copy.deepcopy(self)

        check = self_copy.check_shape(Lc, width, height)
        while check == False:
            self_copy.twist = self_copy.twist - np.deg2rad(1)
            check = self_copy.check_shape(Lc, width, height)

            if self_copy.twist == self.twist: # Break if it does a 360 without improvement
                return self.twist

        return self_copy.twist

    ## Method to scale and rotate the airfoil coords against the chord and twist angle
    def scaled_shape(self):
        x_coords, y_coords = self.airfoil.shape()

        # Scale the coordinates using the chord
        scaled_x_coords = np.array([self.chord * x for x in x_coords])
        scaled_y_coords = np.array([self.chord * y for y in y_coords])

        # Rotate coords
        x_rotated = scaled_x_coords * np.cos(self.twist) - scaled_y_coords * np.sin(self.twist)
        y_rotated = scaled_x_coords * np.sin(self.twist) + scaled_y_coords * np.cos(self.twist)
        x_rotated = x_rotated.tolist()
        y_rotated = y_rotated.tolist()

        return [x_rotated, y_rotated]