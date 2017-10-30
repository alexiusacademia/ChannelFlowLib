from channelflowlib.openchannellib import Rectangular

# Initialize Rectangular Channel instance
rect = Rectangular(unknown='discharge', unit='english')

# Set the inputs
rect.set_channel_slope(0.001)
rect.set_channel_base(1.0)
rect.set_roughness(0.015)
rect.set_water_depth(0.989)

# Analyze
rect.analyze()

# Show the outputs
print ('Discharge : ', round(rect.discharge, 2))
print ('Wet Area  : ', round(rect.wetted_area, 3))
print ('Wet Perimeter: ', round(rect.wetted_perimeter, 3))
print ('Hydraulic Radius: ', round(rect.hydraulic_radius, 4))
