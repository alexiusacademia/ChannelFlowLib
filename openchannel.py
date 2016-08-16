#---------------------------------------------------------------------------#
#	Copyright (C) 2016  Alexius Academia									#
#																			#
#	This program is free software: you can redistribute it and/or modify	#
#	it under the terms of the GNU General Public License as published by	#
#	the Free Software Foundation, either version 3 of the License, or		#
#	(at your option) any later version.										#
#																			#
#	This program is distributed in the hope that it will be useful,			#
#	but WITHOUT ANY WARRANTY; without even the implied warranty of			#
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the			#
#	GNU General Public License for more details.							#
#																			#
#	You should have received a copy of the GNU General Public License		#
#	along with this program.  If not, see <http://www.gnu.org/licenses/>	#
#---------------------------------------------------------------------------#
#	File:		openchannel.py 												#
#	Author:		Alexius Academia											#
#	Email:		alexius.academia@gmail.com 									#
#---------------------------------------------------------------------------#	
#	Description:	This class is for the computation of hydraulics elements#
#			of open channels using the Manning's equation.					#
#---------------------------------------------------------------------------#

""" Open Channel Module """
metric = 'metric'                           # String metric for unit conversion
cfs_to_cms = 1/35.28755                     # Convert cubic feet per second to cubic meter per second
ft_to_meter = 1/3.28                        # Convert feet to meter
cms_to_cfs = 3.28 ** 3                      # Convert cms to cfs
meter_to_feet = 3.28                        # Convert meter to feet
mps_to_fps = 3.28                           # Convert meter/s to feet/s
sqm_to_sq_ft = 3.28 ** 2                    # Convert square meter to square feet


class Rectangular:
    #####################################
    #   Variables and default values    #
    #####################################
    unknown = dict()                    # Unknown (e.g. unknown='discharge')
    unknown['unit'] = metric            # Default unit (metric)
    unknown['unknown'] = 'water_depth'  # Default unknown
    water_depth = 0.0                   # Water depth in meters
    channel_base = 0.0                  # Channel base, in meters
    velocity = 0.0                      # Average velocity in m/s
    wetted_perimeter = 0.0              # Wetted perimeter in m
    wetted_area = 0.0                   # Wetted area in sq.m.
    hydraulic_radius = 0.0              # Hydraulic radius in m
    channel_slope = 0.0                 # Bed slope
    roughness = 0.0                     # Manning's roughness coefficient
    discharge = 0.0                     # Discharge in cms

    def __init__(self, **unknown):
        if 'unknown' in unknown.keys():
            self.unknown['unknown'] = unknown['unknown']        # Get the unknown

    # Check if unit is set to metric
    def ismetric(self):
        if self.unknown['unit'] == metric:
            return True
        else:
            return False

    #####################
    #   Get Methods     #
    #####################
    def get_discharge(self):
        if self.unknown['unit'] == metric:
            return round(self.discharge, 3)
        else:
            return round(self.discharge * cms_to_cfs, 3)

    def get_channel_slope(self):
        return round(self.channel_slope, 5)

    def get_roughness(self):
        return self.roughness

    def get_channel_base(self):
        if self.unknown['unit'] == metric:
            return round(self.channel_base, 2)
        else:
            return round(self.channel_base * meter_to_feet, 2)

    def get_water_depth(self):
        if self.unknown['unit'] == metric:
            return round(self.water_depth, 2)
        else:
            return round(self.water_depth * meter_to_feet, 2)

    def get_velocity(self):
        if self.unknown['unit'] == metric:
            return round(self.velocity, 3)
        else:
            return round(self.velocity * mps_to_fps, 3)

    def get_wettedarea(self):
        if self.unknown['unit'] == metric:
            return round(self.wetted_area, 3)
        else:
            return round(self.wetted_area * sqm_to_sq_ft, 3)

    def get_wettedperimeter(self):
        if self.unknown['unit'] == metric:
            return round(self.wetted_perimeter, 3)
        else:
            return round(self.wetted_perimeter * meter_to_feet, 3)

    def get_hydraulicradius(self):
        if self.unknown['unit'] == metric:
            return round(self.hydraulic_radius, 3)
        else:
            return round(self.hydraulic_radius * meter_to_feet, 3)

    #################
    # Set Methods   #
    #################
    def set_discharge(self, discharge):
        if self.unknown['unit'] == metric:
            self.discharge = discharge
        else:
            self.discharge = discharge * cfs_to_cms

    def set_channel_slope(self, channel_slope):
        self.channel_slope = channel_slope

    def set_roughness(self, roughness):
        self.roughness = roughness

    def set_channel_base(self, channel_base):
        if self.unknown['unit'] == metric:
            self.channel_base = channel_base
        else:
            self.channel_base = channel_base * ft_to_meter

    def set_water_depth(self, water_depth):
        if self.unknown['unit'] == metric:
            self.water_depth = water_depth
        else:
            self.water_depth = water_depth * ft_to_meter

    #################
    #   Methods     #
    #################
    def analyze(self):

        # Check the unknown
        if self.unknown['unknown'] == 'water_depth':
            q = self.discharge
            s = self.channel_slope
            n = self.roughness
            b = self.channel_base

            q_trial = 0.0
            d = 0.0
            v = 0.0
            if q > 0:
                while q_trial < q:
                    d += 0.00001
                    a = d * b
                    p = b + 2*d
                    r = a / p
                    v = (1/n) * s**.5 * r**(2/3)
                    q_trial = a * v
            self.velocity = v
            self.water_depth = d
            self.wetted_area = a
            self.wetted_perimeter = p
            self.hydraulic_radius = r

        elif self.unknown['unknown'] == 'discharge':
            d = self.water_depth
            b = self.channel_base
            s = self.channel_slope
            n = self.roughness

            a = b * d
            p = b + 2*d
            r = a / p
            v = (1/n) * s**.5 * r**(2.0/3)
            q = v * a

            self.discharge = q
            self.velocity = v
            self.wetted_area = a
            self.wetted_perimeter = p
            self.hydraulic_radius = r

        elif self.unknown['unknown'] == 'channel_slope':
            q = self.discharge
            d = self.water_depth
            n = self.roughness
            b = self.channel_base

            a = b * d
            p = b + 2*d
            r = a / p
            v = 0.0

            if q > 0:
                s = 0.0
                q_trial = 0.0
                while q_trial < q:
                    s += 0.0000001
                    v = (1/n) * s**0.5 * r**(2.0/3)
                    q_trial = v * a
                # Pass to global variable
                self.channel_slope = s
                self.velocity = v
                self.wetted_area = a
                self.wetted_perimeter = p
                self.hydraulic_radius = r

        elif self.unknown['unknown'] == 'channel_base':
            q = self.discharge
            d = self.water_depth
            s = self.channel_slope
            n = self.roughness

            q_trial = 0.0
            b = 0.0
            a = 0.0
            p = 0.0
            r = 0.0

            while q_trial < q:
                if q > 0:
                    b += 0.0001
                    a = b * d
                    p = b + 2 * d
                    r = a / p
                    v = (1/n) * s ** 0.5 * r ** (2.0/3)
                    q_trial = v * a
            self.channel_base = b
            self.velocity = v
            self.wetted_area = a
            self.wetted_perimeter = p
            self.hydraulic_radius = r
        else:
            self.channel_base       = 0.0
            self.velocity           = 0.0
            self.wetted_area        = 0.0
            self.wetted_perimeter   = 0.0
            self.hydraulic_radius   = 0.0

class Trapezoidal:
    #########################
    #   Declare variables   #
    #########################
    unknown = dict()                    # Dictionary for the unknown (e.g. unknown='water_depth')
    unknown['unit'] = metric            # Default unit, metric
    unknown['unknown'] = 'water_depth'  # Default unknown
    discharge = 0.0                     # Discharge in cms
    channel_slope = 0.0                 # Channel slope
    side_slope = 0.0                    # Side slope (e.g. 1:1 or 1.5:1)
    roughness = 0.0                     # Manning's roughness coefficient
    channel_base = 0.0                  # Channel bottom width in meter
    water_depth = 0.0                   # Water depth in meter
    velocity = 0.0                      # Mean velocity in m/s
    wetted_area = 0.0                   # Wetted area in sq.m.
    wetted_perimeter = 0.0              # Wetted perimeter in meter
    hydraulic_radius = 0.0              # Hydraulic radius in meter
    critical_depth = 0.0                # Critical depth in meter

    # Constructor, tells the unknown
    def __init__(self, **unknown):
        if 'unknown' in unknown.keys():
            self.unknown['unknown'] = unknown['unknown']

    # Check if unit is set to metric
    def ismetric(self):
        if self.unknown['unit'] == metric:
            return True
        else:
            return False

    #################
    #   Setters     #
    #################
    def set_discharge(self, discharge):
        if self.unknown['unit'] == metric:
            self.discharge = discharge
        else:
            self.discharge = discharge * cfs_to_cms

    def set_channel_slope(self, channel_slope):
        self.channel_slope = channel_slope

    def set_sideslope(self, side_slope):
        self.side_slope = side_slope

    def set_roughness(self, roughness):
        self.roughness = roughness

    def set_channel_base(self, channel_base):
        if self.unknown['unit'] == metric:
            self.channel_base = channel_base
        else:
            self.channel_base = channel_base * ft_to_meter

    def set_water_depth(self, water_depth):
        if self.unknown['unit'] == metric:
            self.water_depth = water_depth
        else:
            self.water_depth = water_depth * ft_to_meter

    #################
    #   Getters     #
    #################
    def get_discharge(self):
        if self.unknown['unit'] == metric:
            return self.discharge
        else:
            return self.discharge * cms_to_cfs

    def get_channel_slope(self):
        return self.channel_slope

    def get_side_slope(self):
        return self.side_slope

    def get_roughness(self):
        return self.roughness

    def get_channel_base(self):
        if self.unknown['unit'] == metric:
            return self.channel_base
        else:
            return self.channel_base * meter_to_feet

    def get_velocity(self):
        if self.unknown['unit'] == metric:
            return self.velocity
        else:
            return self.velocity * mps_to_fps

    def get_wetted_area(self):
        if self.unknown['unit'] == metric:
            return self.wetted_area
        else:
            return self.wetted_area * sqm_to_sq_ft

    def get_wetted_perimeter(self):
        if self.unknown['unit'] == metric:
            return self.wetted_perimeter
        else:
            return self.wetted_perimeter * meter_to_feet

    def get_hydraulic_radius(self):
        if self.unknown['unit'] == metric:
            return self.hydraulic_radius
        else:
            return self.hydraulic_radius * meter_to_feet

    def get_water_depth(self):
        if self.unknown['unit'] == metric:
            return self.water_depth
        else:
            return self.water_depth * meter_to_feet

    def get_critical_depth(self):
        if self.unknown['unit'] == metric:
            return self.critical_depth
        else:
            return self.critical_depth * meter_to_feet

    #############################
    #   Method for analysis     #
    #############################
    def analyze(self):
        # If unknown is water depth
        if self.unknown['unknown'] == 'water_depth':
            # Get the values of inputs
            q = self.discharge
            s = self.channel_slope
            ss = self.side_slope
            n = self.roughness
            b = self.channel_base

            q_trial = 0.0
            d = 0.0
            a = 0.0
            p = 0.0
            r = 0.0
            v = 0.0

            while q_trial < q:
                d += 0.0001
                a = (b + d * ss) * d
                p = 2 * d * (ss**2 + 1)**0.5 + b
                r = a / p
                v = (1/n) * r ** (2.0/3) * s ** 0.5
                q_trial = v * a

            self.velocity = v
            self.wetted_area = a
            self.wetted_perimeter = p
            self.hydraulic_radius = r
            self.water_depth = d

        # If unknown is discharge
        elif self.unknown['unknown'] == 'discharge':
            s = self.channel_slope
            ss = self.side_slope
            d = self.water_depth
            b = self.channel_base
            n = self.roughness

            a = (b + d * ss) * d
            p = 2 * d * (ss**2 + 1)**0.5 + b
            r = a / p
            v = (1/n) * s ** 0.5 * r ** (2.0/3)
            q = v * a

            self.discharge = q
            self.velocity = v
            self.wetted_area = a
            self.wetted_perimeter = p
            self.hydraulic_radius = r

        # If unknown is bed slope
        elif self.unknown['unknown'] == 'channel_slope':
            q = self.discharge
            ss = self.side_slope
            d = self.water_depth
            b = self.channel_base
            n = self.roughness

            q_trial = 0.0
            v = 0.0
            a = 0.0
            p = 0.0
            r = 0.0
            s = 0.0

            if q > 0:
                while q_trial < q:
                    s += 0.000001
                    a = (b + d * ss) * d
                    p = 2 * d * (ss**2 + 1)**0.5 + b
                    r = a / p
                    v = (1/n) * s ** 0.5 * r ** (2.0/3)
                    q_trial = v * a

                # Pass to global variable
                self.channel_slope = s
                self.velocity = v
                self.wetted_area = a
                self.wetted_perimeter = p
                self.hydraulic_radius = r

        # If unknown is bottom width
        elif self.unknown['unknown'] == 'channel_base':
            q = self.discharge
            s = self.channel_slope
            ss = self.side_slope
            d = self.water_depth
            n = self.roughness

            q_trial = 0.0
            b = 0.0
            a = 0.0
            p = 0.0
            r = 0.0
            v = 0.0

            if q > 0:
                while q_trial < q:
                    b += 0.0001
                    a = (b + d * ss) * d
                    p = 2 * d * (ss**2 + 1)**0.5 + b
                    r = a / p
                    v = (1/n) * s ** 0.5 * r ** (2.0/3)
                    q_trial = v * a

                self.channel_base = b
                self.wetted_area = a
                self.wetted_perimeter = p
                self.hydraulic_radius = r
                self.velocity = v

