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
                     math.pow(1, 2.0) * math.pow(critical_hydraulic_radius, (1.0/3.0))

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
