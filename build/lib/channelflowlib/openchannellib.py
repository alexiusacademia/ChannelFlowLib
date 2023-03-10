# --------------------------------------------------------------------------#
# Copyright (C) 2016  Alexius Academia                                      #
#                                                                           #
# This program is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation, either version 3 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# This program is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with this program.  If not, see <http://www.gnu.org/licenses/>      #
# --------------------------------------------------------------------------#
# File:		    openchannellib.py                                              #
# Author:		Alexius Academia                                            #
# Email:		alexius.academia@gmail.com                                  #
# --------------------------------------------------------------------------#
# Description:	This module is for the computation of hydraulics elements   #
#           of open channels using the Manning's equation.                  #
# --------------------------------------------------------------------------#
import math

from .critical_flow import (
    solve_critical_flow_rectangular,
    solve_critical_flow_trapezoidal,
    solve_critical_flow_circular
)

""" Open Channel Module """
metric = 'metric'                           # String metric for unit conversion
cfs_to_cms = 1/35.28755                     # Convert cubic feet per second to cubic meter per second
ft_to_meter = 1/3.28                        # Convert feet to meter
cms_to_cfs = 3.28 ** 3                      # Convert cms to cfs
meter_to_feet = 3.28                        # Convert meter to feet
mps_to_fps = 3.28                           # Convert meter/s to feet/s
sqm_to_sq_ft = 3.28 ** 2                    # Convert square meter to square feet


class Rectangular:
    """
    Rectangular Channel Class.
    """
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
    critical_flow = None

    def __init__(self, **unknown):
        """
        Initialize the rectangular class for rectangular open channel.
        :param unknown:
        """
        if 'unknown' in unknown.keys():
            self.unknown['unknown'] = unknown['unknown']        # Get the unknown
        if 'unit' in unknown.keys():
            self.unknown['unit'] = unknown['unit']

    # Check if unit is set to metric
    def ismetric(self):
        """
        Check if the unit set is metric.
        :return: bool
        """
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

        self.critical_flow = solve_critical_flow_rectangular(self.wetted_area,
                                                        self.channel_base,
                                                        self.velocity,
                                                        self.discharge,
                                                        self.roughness)


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
    critical_flow = None

    # Constructor, tells the unknown
    def __init__(self, **unknown):
        if 'unknown' in unknown.keys():
            self.unknown['unknown'] = unknown['unknown']
        if 'unit' in unknown.keys():
            self.unknown['unit'] = unknown['unit']

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

        self.critical_flow = solve_critical_flow_trapezoidal(discharge=self.discharge,
                                                             water_depth=self.water_depth,
                                                             channel_base=self.channel_base,
                                                             side_slope=self.side_slope,
                                                             roughness=self.roughness,
                                                             flow_area=self.wetted_area,
                                                             velocity=self.velocity)


class Circular:
    def __init__(self):
        """
        Constructor
        :return:
        """
        self.discharge = 0.0
        self.slope = 0.0
        self.roughness = 0.015      # Default for conncrete
        self.diameter = 0.0
        self.wetted_perimeter = 0.0
        self.wetted_area = 0.0
        self.hydraulic_radius = 0.0
        self.velocity = 0.0
        self.water_depth = 0.0
        self.critical_flow = None

    # Getters
    def get_discharge(self):
        """
        Get the computed discharge
        :return:
        """
        return self.discharge

    def get_velocity(self):
        """
        Get the computed average velocity
        :return:
        """
        return self.velocity

    def get_wetted_area(self):
        """
        Get the computed wetted area.
        :return:
        """
        return self.wetted_area

    def get_wetted_perimeter(self):
        """
        Get the computed wetted perimeter.
        :return:
        """
        return self.wetted_perimeter

    def get_hydraulic_radius(self):
        """
        Get the computed hydraulic radius.
        :return:
        """
        return self.hydraulic_radius

    # Setters
    def set_slope(self, slope):
        """
        Set the channel slope
        :param slope:
        :return:
        """
        self.slope = slope

    def set_diameter(self, diameter):
        """
        Set the pipe diameter in meters
        :param diameter:
        :return:
        """
        self.diameter = diameter

    def set_roughness(self, n):
        """
        Set the manning's roughness coefficient
        :param n:
        :return:
        """
        self.roughness = n

    def set_water_depth(self, h):
        """
        Set the water depth to get the discharge
        :param h:
        :return:
        """
        self.water_depth = h

    # Functions
    def calculate_discharge(self):
        """
        Calculate the hydraulic elements of the pipe
        :return:
        """
        h = self.water_depth
        dia = self.diameter
        slope = self.slope
        n = self.roughness

        if h > dia:
            print('Error in input. Water depth is greater than pipe diameter!')
            return 0, 0, 0, 0, 0

        if h < (dia/2):
            almost_full = False  # Indicates that the water surface is below the center
        else:
            almost_full = True

        ''' Calculate tetha '''
        if almost_full:
            tetha = 2 * math.acos((2 * h - dia)/dia) * 180 / math.pi
        else:
            tetha = 2 * math.acos((dia - 2 * h)/dia) * 180 / math.pi

        ''' Calculate area of triangle '''
        a_tri = (dia**2) * math.sin(tetha * math.pi / 180) / 8

        ''' Calculate area of sector '''
        if almost_full:
            a_sec = math.pi * dia**2 * (360 - tetha) / 1440
            self.wetted_area = a_sec + a_tri
            self.wetted_perimeter = math.pi * dia * (360 - tetha) / 360
        else:
            a_sec = tetha * math.pi * dia**2 / 1440
            self.wetted_area = a_sec - a_tri
            self.wetted_perimeter = math.pi * dia * tetha / 360

        self.hydraulic_radius = self.wetted_area / self.wetted_perimeter

        r = self.hydraulic_radius
        s = slope

        v = (1 / n) * r**(2/3) * math.sqrt(s)       # Velocity
        q = v * self.wetted_area                    # Discharge

        self.velocity = v
        self.discharge = q

        self.critical_flow = solve_critical_flow_circular(self.discharge,
                                                          self.diameter,
                                                          self.water_depth,
                                                          self.roughness,
                                                          self.wetted_area,
                                                          self.velocity)

        # Return the hydraulic elements in a tuple
        return self.discharge, self.velocity, self.wetted_area, self.wetted_perimeter, self.hydraulic_radius


# This class if for irrregular shape channels like rivers and creeks
class IrregularSection:
    def __init__(self, points):
        """
        Constructor and initializations
        :param points:
        :return:
        """
        self.points = points
        # Initializations
        self.roughness = 0.0            # Average roughness of the cross section
        self.bed_slope = 0.0            # River bed average slope
        self.water_elevation = 0.0      # Water surface elevation
        self.wetted_area = 0.0          # Wetted area
        self.wetted_perimeter = 0.0     # Wetted perimeter
        self.hydraulic_radius = 0.0     # Hydraulic radius
        self.velocity = 0.0             # Average velocity
        self.discharge = 0.0            # Discharge
        self.max_water_elevation = 0.0
        self.min_water_elevation = 0.0

    # ---------
    # Setters
    # ---------
    def set_average_rougness(self, roughness_coefficient):
        """
        Set the manning's roughness coefficient, n
        :param roughness_coefficient:
        :return:
        """
        self.roughness = roughness_coefficient

    def set_bed_slope(self, bed_slope):
        """
        Set the average bed slope
        :param bed_slope:
        :return:
        """
        self.bed_slope = bed_slope

    def set_water_elevation(self, water_elevation):
        """
        Sets the water surface elevation
        :param water_elevation:
        :return:
        """
        self.water_elevation = water_elevation

    # ----------
    # Methods
    # ----------
    def analyze(self):
        # Validate inputs
        if self.bed_slope == 0:
            raise Exception
        if self.roughness == 0:
            raise Exception

        # Count the points
        num_points = len(self.points)

        # Get the lower bank elevation
        if self.points[0][1] > self.points[num_points-1][1]:
            max_ws = self.points[num_points-1][1]
        else:
            max_ws = self.points[0][1]

        self.max_water_elevation = max_ws

        if self.water_elevation > max_ws:
            print('Water will overflow the bank!')
            # raise Exception
            return

        # Get the lowest possible water elevation
        if self.water_elevation < self.get_lowest_elev(self.points):
            print('Water surface is below the lowest point of the channel.')
            return

        # Number of intersections
        left = 0
        right = 0

        new_points = []     # New points, removing points out of range of the intersection

        for index in range(len(self.points)):
            x, y = self.points[index]

            # Look for the first point of intersection
            if left == 0:
                if y < self.water_elevation:
                    left += 1
                    x1 = self.points[index-1][0]
                    y1 = self.points[index-1][1]
                    x2 = self.points[index][0]
                    y2 = self.points[index][1]
                    x3 = (self.water_elevation - y1) * (x2 - x1) / (y2 - y1) + x1
                    new_points.append((x3, self.water_elevation))  # Add this point as the first new point from the left

            if right == 0:
                if left == 1:
                    if y > self.water_elevation:
                        right += 1
                        x1 = self.points[index-1][0]
                        y1 = self.points[index-1][1]
                        x2 = self.points[index][0]
                        y2 = self.points[index][1]
                        x3 = (self.water_elevation - y1) * (x2 - x1) / (y2 - y1) + x1
                        new_points.append((x3, self.water_elevation))

            if left == 1:
                if right == 0:
                    new_points.append(self.points[index])

        # Hydraulic elements
        self.wetted_area = self.polygon_area(new_points)
        self.wetted_perimeter = self.get_perimeter(new_points)
        self.hydraulic_radius = self.wetted_area / self.wetted_perimeter
        self.velocity = (1 / self.roughness) * self.hydraulic_radius**(2/3) * self.bed_slope**0.5
        self.discharge = self.velocity * self.wetted_area

    def polygon_area(self, vertices):
        """
        Implementation of Shoelace Formula in finding the area of a closed
        polygon bounded by vertices
        :param vertices:
        :return:
        """
        n = len(vertices) # of corners
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += vertices[i][0] * vertices[j][1]
            area -= vertices[j][0] * vertices[i][1]
        area = abs(area) / 2.0
        return area

    def get_perimeter(self, points):
        """
        Get the total distance covered by multiple points
        :param points:
        :return:
        """
        p = 0.0         # perimeter
        n = len(points)
        for i in range(n-1):
            p1 = points[i]
            p2 = points[i+1]
            p += self.point_distance([p1, p2])

        return p

    def point_distance(self, points):
        """
        Get the distance between two points
        :param points:
        :return:
        """
        p1 = points[0]
        p2 = points[1]
        x1, y1 = p1
        x2, y2 = p2

        dist = math.sqrt((y2-y1)**2 + (x2-x1)**2)

        return dist

    def get_lowest_elev(self, points):
        """
        Get the lowest point from the vertices
        :param points:
        :return: lowest
        """
        elevs = []                  # List of elevations (ordinates)
        lowest = 0                  # Initial value of lowest
        for point in points:
            elevs.append(point[1])  # Iterate through the points and collect the ordinates
        for i in range(len(elevs)): # Find the lowest in the list of ordinates
            if i == len(elevs):
                break
            if elevs[i] < lowest:
                lowest = elevs[i]
            else:
                lowest = lowest
        return lowest
