from channelflowlib.openchannellib import Trapezoidal

# Initialize Rectangular Channel instance
trap = Trapezoidal(unknown='water_depth', unit='metric')

# Set the inputs
trap.set_channel_slope(0.001)
trap.set_channel_base(1.0)
trap.set_sideslope(1)
trap.set_roughness(0.015)
trap.set_discharge(1.0)

# Analyze
trap.analyze()

# Show the outputs
print ('Discharge : ', round(trap.discharge, 2))
print ('Wet Area  : ', round(trap.wetted_area, 3))
print ('Wet Perimeter: ', round(trap.wetted_perimeter, 3))
print ('Hydraulic Radius: ', round(trap.hydraulic_radius, 4))

# Critical flow
critical_flow = trap.critical_flow
print('Critical Depth: ', critical_flow['critical_depth'])
print('Critical Wetted Perimeter: ', critical_flow['critical_wetted_perimeter'])
