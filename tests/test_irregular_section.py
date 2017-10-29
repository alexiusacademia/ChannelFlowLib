from channelflowlib.openchannellib import IrregularSection

pts = (
    (0, 1.13),
    (1.287, 1.2),
    (2.58, 0.09),
    (5.223, -1.57),
    (10.446, -1.81),
    (12.333, 0.72),
    (14.188, 1.2)
)

channel = IrregularSection(pts)
channel.set_average_rougness(0.03)
channel.set_bed_slope(0.002)
channel.set_water_elevation(1)
channel.analyze()

print('Discharge : ', round(channel.discharge, 2))
print('Wet Area  : ', round(channel.wetted_area, 2))

# Plot a water rating curve
max_elev = 1.0
min_elev = -1.0
interval = 0.1
intervals = ((max_elev - min_elev) / interval)

elevs = []
discharges = []

for i in range(int(intervals) + 1):
    elev = min_elev + (i * interval)

    channel.set_water_elevation(elev)
    channel.analyze()

    discharge = channel.discharge

    elevs.append(elev)
    discharges.append(discharge)

try:
    import matplotlib.pyplot as plt

    plt.plot(discharges, elevs)
    plt.show()
except Exception as e:
    print(e)
