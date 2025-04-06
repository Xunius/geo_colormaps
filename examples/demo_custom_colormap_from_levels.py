'''Demo script, plot ERA-I SST using a custom colormap defined from level list

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-06 08:00:38
'''

import os
import numpy as np
import matplotlib.pyplot as plt

import sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, '..', '..'))

import geo_colormaps


if __name__ == '__main__':

    DATA_FILE_NAME = os.path.join(current_dir, '..', 'geo_colormaps', 'tests',
                                  'fixtures', 'sample_erai_data.npz')

    # read a data file and load data
    npzfile = np.load(DATA_FILE_NAME)
    sst = npzfile['sst']
    lons = npzfile['lons']
    lats = npzfile['lats']

    # get the 1st time slice and convert to celsius
    sst = sst[0] - 273.15
    sst = np.where(sst > 1e5, np.nan, sst)



    # create figure and axis
    figure, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6), dpi=100)

    # subplot 1: create a custom (continous) colormap from:
    # 1. a level list,
    # 2. an optional unit string,
    # 3. an optional matplotlib built-in cmap (default to gist_rainbow

    custom_levels = [None] + list(np.arange(10, 32, 2)) + [None]
    custom_unit   = r'$^{\circ}C$'
    mpl_cmp       =  'rainbow'
    cmap_obj      = geo_colormaps.colormap.create_cmap_from_levels(custom_levels,
                                                                custom_unit,
                                                                mpl_cmp)

    # contourf plot
    ax = axes[0]
    ax.contourf(lons, lats, sst,
                cmap=cmap_obj.cmap,
                norm=cmap_obj.norm,
                extend=cmap_obj.extend)

    # plot colrobar
    cmap_obj.plot_colorbar(ax=ax)

    ax.set_title('(a) custom continuous levels')

    # subplot 2: create a custom (discrete) colormap from:
    # 1. a level list, now with the following format: [(discrete level, level label), (discrete level, level label), ...]
    # 2. an optional unit string,
    # 3. an optional matplotlib built-in cmap (default to gist_rainbow
    custom_levels = [(10, 'Ten'), (20, 'Twenty')]
    # can also omit the level label, then the discrete level it self will be used as label:
    #custom_levels = [(10, ), (20, )]
    custom_unit   = r'$^{\circ}C$'
    mpl_cmp       = 'rainbow'
    cmap_obj      = geo_colormaps.colormap.create_cmap_from_levels(custom_levels,
                                                                custom_unit,
                                                                mpl_cmp)

    # contourf plot
    ax = axes[1]
    ax.contourf(lons, lats, sst,
                cmap=cmap_obj.cmap,
                norm=cmap_obj.norm,
                extend=cmap_obj.extend)

    # plot colrobar
    cmap_obj.plot_colorbar(ax=ax)

    ax.set_title('(b) custom discrete levels')

    figure.show()


