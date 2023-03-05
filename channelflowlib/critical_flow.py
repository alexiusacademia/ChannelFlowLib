import math

from .constants import GRAVITY_G


def solve_critical_flow_rectangular(flow_area: float,
                                    base_width: float,
                                    average_velocity: float,
                                    discharge: float,
                                    manning_roughness: float):
    hydraulic_depth = flow_area / base_width
    froude_number = average_velocity / math.sqrt(GRAVITY_G * hydraulic_depth)
    discharge_intensity = discharge / base_width
    critical_depth = math.pow(math.pow(discharge_intensity, 2.0) / GRAVITY_G, (1.0 / 3.0))
    critical_top_width = base_width
    critical_wetted_perimeter = base_width + (2 * critical_depth)
    critical_flow_area = base_width * critical_depth
    critical_hydraulic_radius = critical_flow_area / critical_wetted_perimeter
    critical_slope = GRAVITY_G * math.pow(manning_roughness, 2.0) * \
                     (critical_wetted_perimeter / critical_top_width) / \
                     math.pow(1, 2.0) * math.pow(critical_hydraulic_radius, (1.0 / 3.0))

    return {
        'hydraulic_depth': hydraulic_depth,
        'froude_number': froude_number,
        'discharge_intensity': discharge_intensity,
        'critical_depth': critical_depth,
        'critical_top_width': critical_top_width,
        'critical_wetted_perimeter': critical_wetted_perimeter,
        'critical_flow_area': critical_flow_area,
        'critical_hydraulic_radius': critical_hydraulic_radius,
        'critical_slope': critical_slope
    }


def solve_critical_flow_trapezoidal(discharge: float,
                                    water_depth: float,
                                    channel_base: float,
                                    side_slope: float,
                                    roughness: float,
                                    flow_area: float,
                                    velocity: float):
    Q2g = pow(discharge, 2.0) / GRAVITY_G

    tester = 0.0

    # Critical depth
    critical_depth = 0.0

    # Critical area, perimeter, hydraulic radius, critical slope
    critical_flow_area = 0.0

    while tester < Q2g:
        critical_depth += 0.00001
        top_width = channel_base + 2 * side_slope * critical_depth
        critical_flow_area = (top_width + channel_base) / 2 * critical_depth
        tester = pow(critical_flow_area, 3) / top_width

    critical_wetted_perimeter = 2 * critical_depth * math.sqrt(pow(side_slope, 2) + 1) + channel_base
    critical_hydraulic_radius = critical_flow_area / critical_wetted_perimeter
    critical_slope = pow(discharge / (critical_flow_area * pow(critical_hydraulic_radius, (2.0 / 3.0))) * roughness,
                         2.0)

    # Solve for froude number
    top_width = channel_base + 2 * side_slope * water_depth
    hydraulic_depth = flow_area / top_width
    froude_number = velocity / math.sqrt(GRAVITY_G * hydraulic_depth)

    discharge_intensity = discharge / top_width

    return {
        'hydraulic_depth': hydraulic_depth,
        'froude_number': froude_number,
        'discharge_intensity': discharge_intensity,
        'critical_depth': critical_depth,
        'top_width': top_width,
        'critical_wetted_perimeter': critical_wetted_perimeter,
        'critical_flow_area': critical_flow_area,
        'critical_hydraulic_radius': critical_hydraulic_radius,
        'critical_slope': critical_slope
    }


def solve_top_width_circular(y: float,
                             triangular_area: float,
                             almost_full: bool,
                             diameter: float):
    top_width = 0.0
    triangle_height = 0.0

    if almost_full:
        triangle_height = y - diameter / 2.0
    else:
        triangle_height = diameter / 2.0 - y

    top_width = 2.0 * diameter / triangle_height

    return top_width


def solve_critical_flow_circular(discharge: float,
                                 diameter: float,
                                 water_depth: float,
                                 roughness: float,
                                 wetted_area: float,
                                 velocity: float):
    # Q ^ 2 / g
    Q2g = pow(discharge, 2) / GRAVITY_G

    # Other side of equation
    tester = 0.0

    # Critical depth
    critical_depth = 0.0

    # Critical area, perimeter, hydraulic radius, critical slope
    critical_flow_area = 0.0
    Pc = 0.0
    critical_hydraulic_radius = 0.0
    critical_slope = 0.0

    # Top width
    T = 0.0

    # Angle of water edges from the center
    thetaC = 0.0

    # Triangle at critical flow
    aTriC = 0.0

    # Sector at critical flow
    aSecC = 0.0

    while tester < Q2g:
        critical_depth += 0.00001

        # Calculate theta
        if critical_depth > (diameter / 2.0):
            # Almost full
            thetaC = 2 * math.acos((2 * critical_depth - diameter) / diameter) * 180.0 / math.pi
        else:
            # Less than half full
            thetaC = 2 * math.acos((diameter - 2 * critical_depth) / diameter) * 180.0 / math.pi

        # Calculate area of triangle
        aTriC = pow(diameter, 2) * math.sin(thetaC * math.pi / 180) / 8

        T = solve_top_width_circular(y=critical_depth,
                                     triangular_area=aTriC,
                                     almost_full=(critical_depth > (diameter / 2.0)),
                                     diameter=diameter)

        # Calculate area of sector
        if critical_depth > (diameter / 2):
            aSecC = math.pi * pow(diameter, 2) * (360 - thetaC) / 1440
            critical_flow_area = aSecC + aTriC
            Pc = math.pi * diameter * (360 - thetaC) / 360
        else:
            aSecC = thetaC * math.pi * pow(diameter, 2) / 1440
            critical_flow_area = aSecC - aTriC
            Pc = math.pi * diameter * thetaC / 360

        # Compare the equation for equality
        tester = pow(critical_flow_area, 3) / T

    # Wetted properties
    theta = 0.0
    aSec = 0.0  # Area of sector

    almost_full_critical = (critical_depth >= (diameter / 2.0))

    # Calculate theta
    if almost_full_critical:
        theta = 2.0 * math.acos((2.0 * critical_depth - diameter) / diameter) * 180.0 / math.pi
    else:
        theta = 2.0 * math.acos((diameter - 2 * critical_depth) / diameter) * 180.0 / math.pi

    # Calculate the area of central triangle
    triangleArea = pow(diameter, 2.0) * math.sin(theta * math.pi / 180.0) / 8

    # Calculate area of sector
    if almost_full_critical:
        aSec = math.pi * pow(diameter, 2) * (360 - theta) / 1440
        critical_wetted_area = aSec + triangleArea
        critical_wetted_perimeter = math.pi * diameter * (360 - theta) / 360
    else:
        aSec = theta * math.pi * pow(diameter, 2) / 1440
        critical_wetted_area = aSec - triangleArea
        critical_wetted_perimeter = math.pi * diameter * theta / 360

    # End of wetted properties

    # Hydraulic radius at critical flow
    critical_hydraulic_radius = critical_flow_area / Pc

    critical_slope = pow((discharge / (critical_flow_area * pow(critical_hydraulic_radius, (2.0 / 3.0))) * roughness), 2)

    critical_velocity = (1.0 / roughness) * math.sqrt(critical_slope) * pow(critical_hydraulic_radius, (2.0 / 3.0))

    # Solve for froude number
    top_width = solve_top_width_circular(y=water_depth,
                                         triangular_area=triangleArea,
                                         almost_full=(water_depth > (diameter / 2)))
    hydraulic_depth = wetted_area / top_width

    froude_number = velocity / math.sqrt(GRAVITY_G * hydraulic_depth)

    discharge_intensity = 4 * discharge / ( math.pi * pow(water_depth, 2))

    return {
        'hydraulic_depth': hydraulic_depth,
        'froude_number': froude_number,
        'discharge_intensity': discharge_intensity,
        'critical_depth': critical_depth,
        'top_width': top_width,
        'critical_wetted_perimeter': critical_wetted_perimeter,
        'critical_flow_area': critical_flow_area,
        'critical_hydraulic_radius': critical_hydraulic_radius,
        'critical_slope': critical_slope
    }
