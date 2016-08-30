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
# File:		    geofunc.py                                                  #
# Author:		Alexius Academia                                            #
# Email:		alexius.academia@gmail.com                                  #
# Date:         August 30, 2016                                             #
# --------------------------------------------------------------------------#
# Description:	This module is called by irrig_channel.py                   #
#               This consists of some basic geometric computations          #
# --------------------------------------------------------------------------#
import math


def polygon_area(vertices):
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


def get_perimeter(points):
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
        p += point_distance([p1, p2])

    return p


def point_distance(points):
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


def get_lowest_elev(points):
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