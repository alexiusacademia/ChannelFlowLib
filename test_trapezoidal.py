from channelflowlib.openchannellib import Trapezoidal

# Initialize Trapezoidal Channel instance
trap = Trapezoidal(unknown='discharge')

# Set the inputs
trap.set_channel_slope(0.001)
trap.set_sideslope(1.0)
trap.set_channel_base(1.0)
trap.set_roughness(0.015)
trap.set_water_depth(0.989)

# Analyze
trap.analyze()

# Show the outputs
print ('Discharge : ', round(trap.discharge, 2))
print ('Wet Area  : ', round(trap.wetted_area, 3))
print ('Wet Perimeter: ', round(trap.wetted_perimeter, 3))
print ('Hydraulic Radius: ', round(trap.hydraulic_radius, 4))
