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
# File:		    irrig_channel.py                                            #
# Author:		Alexius Academia                                            #
# Email:		alexius.academia@gmail.com                                  #
# Date:         August 30, 2016                                             #
# --------------------------------------------------------------------------#
# Description:	This module is for the computation of discharge rating curve#
#               of an stream/river section                                  #
# --------------------------------------------------------------------------#
from geofunc import *
try:
    import matplotlib.pyplot as plt
except Exception as e:
    print(e)


def irregular_channel(*points):
    # Parameters:
    slope = 0.008               # Riverbed slope
    interval = .1               # Interval of w.s. elevation
    roughness = 0.04            # Manning's n

    # Get the lowest elevation
    datum = get_lowest_elev(points)
    wse = datum + interval

    # Count the points
    num_points = len(points)

    # Get the lower bank elevation
    if points[0][1] > points[num_points-1][1]:
        max_ws = points[num_points-1][1]
    else:
        max_ws = points[0][1]

    elev_list = []          # List of elevations in the iteration
    discharge_list = []     # List of corresponding discharges per elevation

    # print('W.S. El.', '\t', 'Discharge')

    while wse < max_ws:
        left = 0            # number of intersection at left
        right = 0           # number of intersection at right

        new_points = []     # New points, disregarding out of range of the intersection

        intersections = []
        for index in range(len(points)):
            x, y = points[index]

            # Look for the first point of intersection
            if left == 0:
                if y < wse:
                    left += 1
                    x1 = points[index-1][0]
                    y1 = points[index-1][1]
                    x2 = points[index][0]
                    y2 = points[index][1]
                    x3 = (wse - y1) * (x2 - x1) / (y2 - y1) + x1
                    intersections.append((x3, wse))
                    new_points.append((x3, wse))

            if right == 0:
                if left == 1:
                    if y > wse:
                        right += 1
                        x1 = points[index-1][0]
                        y1 = points[index-1][1]
                        x2 = points[index][0]
                        y2 = points[index][1]
                        x3 = (wse - y1) * (x2 - x1) / (y2 - y1) + x1
                        intersections.append((x3, wse))
                        new_points.append((x3, wse))

            if left == 1:
                if right == 0:
                    new_points.append(points[index])

        wetted_area = polygon_area(new_points)
        wetted_perimeter = get_perimeter(new_points)
        hydraulics_radius = wetted_area / wetted_perimeter
        velocity = (1 / roughness) * hydraulics_radius ** (2/3) * slope ** 0.5
        discharge = velocity * wetted_area

        elev_list.append(wse)               # Add the elevation to the list
        discharge_list.append(discharge)    # Add the discharge to the list per elevation

        # print(round(wse, 4), '\t', round(discharge, 3))

        wse += interval

    try:
        plt.plot(discharge_list, elev_list)
        plt.show()
    except Exception as e:
        print(e)

    return elev_list, discharge_list

# Sample Usage
# Please remove all the codes below if you are going to use this module.
# The code below is for illustration only
if __name__ == '__main__':
    elev, q = irregular_channel((0, 1.13), (1.287, 1.2), (2.58, 0.09),
                                (5.223, -1.57), (10.446, -1.81), (12.333, 0.72), (14.188, 1.2))

    print('W.S. El.\tDischarge')
    for i in elev:
        for j in q:
            print(round(i, 4), '\t', round(j, 3))