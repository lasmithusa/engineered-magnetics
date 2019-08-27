'''
=================================
Magnetic Flux Density (B) Plotter
=================================

Calculates and plots the magnetic flux density, B, in Tesla for
opposed cylindrical magnets given the following inputs:

- Flux density remanence in Teslas (B_rem) - property of magnet type / grade
- Magnet radius in mm (mag_radius)
- Magnet thickness in mm (mag_thick)
- Midpoint distance range between magnets in mm (dist_range)

TODO:
- Add support for block and ring magnets
- Add support for single magnets

Author: Luke Smith, 8/26/2019
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# INPUTS #
# Magnet Properties
# flux density remanence - property of magnet type / grade
B_rem = 1.21
# magnet radius (mm)
mag_radius = 7.62
# magnet thickness (mm)
mag_thick = 2.794

# Design details
# midpoint distance betweeen magnets - design envelope [min, max]
dist_range = (0.00, 25.00)

# METHOD DEFINITIONS #
def calc_B(dist, pos, B_rem, mag_radius, mag_thick, mag_shape = 'cyl'):
    '''
    ====================================
    Magnetic Flux Density (B) Calculator
    ====================================

    Calculates the magnetic flux density, B, in Tesla for
    opposed cylindrical magnets given the following inputs:

    - Midpoint distance between magnets in mm (dist)
    - Position from midpoint in mm (pos)
    - Flux density remanence in Teslas (B_rem) - property of magnet type / grade
    - Magnet radius in mm (mag_radius)
    - Magnet thickness in mm (mag_thick)
    
    TODO:
    - Add support for block and ring magnets
    - Add support for single magnets

    '''

    # convert inputs in mm to m
    dist_m = dist / 1000
    pos_m = pos / 1000
    mag_radius_m = mag_radius / 1000
    mag_thick_m = mag_thick / 1000

    if mag_shape == 'cyl':
        B = (B_rem / 2) * ((mag_thick_m + (dist_m + pos_m)) / np.sqrt(mag_radius_m**2 + (mag_thick_m + (dist_m + pos_m))**2) \
             - (dist_m + pos_m) / np.sqrt(mag_radius_m**2 + (dist_m + pos_m)**2)) \
        + (B_rem / 2) * ((mag_thick_m + (dist_m - pos_m)) / np.sqrt(mag_radius_m**2 + (mag_thick_m + (dist_m - pos_m))**2) \
             - (dist_m - pos_m) / np.sqrt(mag_radius_m**2 + (dist_m - pos_m)**2))

    elif mag_shape == 'block':
        return np.nan
    elif mag_shape == 'ring':
        return np.nan
    else:
        return np.nan

    # set all flux density values where the calculation position
    # is *behind* or *inside* the magnet (outside of envelope) to 0
    try:
        B[pos > dist] = 0
    except TypeError:
        # pos not iterable
        if pos > dist:
            return 0
        else:
            return B
    else:
        return B

# CALCULATIONS #
# generate X values to plot
dist = np.linspace(*dist_range, 100)

# generate plotting grid
dist, pos = np.meshgrid(dist, dist)

# calculate B values
B = calc_B(dist, pos, B_rem, mag_radius, mag_thick)

# PLOT #
# plot with matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')
ax.set_xlabel('\nMidpoint Distance Between Magnets\nX [mm]')
ax.set_ylabel('\nDistance from Midpoint\nP [mm]')
ax.set_zlabel('\nFlux Density\nB [Tesla]')

surf = ax.plot_surface(dist, pos, B, cmap=cm.RdBu)

plt.show()