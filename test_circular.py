from channelflowlib.openchannellib import Circular

# Initialize Rectangular Channel instance
circ = Circular()

# Set the inputs
circ.slope = 0.001
circ.set_diameter(1.0)
circ.set_roughness(0.015)
circ.set_water_depth(1)

# Analyze
circ.calculate_discharge()

# Show the outputs
print ('Discharge : ', round(circ.discharge, 2))
print ('Wet Area  : ', round(circ.wetted_area, 3))
print ('Wet Perimeter: ', round(circ.wetted_perimeter, 3))
print ('Hydraulic Radius: ', round(circ.hydraulic_radius, 4))

# Critical flow
critical_flow = circ.critical_flow
print('Froude Number: ', critical_flow['froude_number'])
print('Critical depth: ', critical_flow['critical_depth'])
print('Critical Wetted Perimeter: ', critical_flow['critical_wetted_perimeter'])
print('Top Width: ', critical_flow['top_width'])
