'''Demo script, plot ERA-I SST using CMA SST colormap

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-04 15:50:20
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
    figure = plt.figure(figsize=(8, 6), dpi=100)
    ax = figure.add_subplot(111)

    # get the colormap object
    cmap_obj = geo_colormaps.CMA_COLORMAPS.SST_CMAP

    # contourf plot
    ax.contourf(lons, lats, sst,
                     cmap=cmap_obj.cmap,
                     norm=cmap_obj.norm,
                     extend=cmap_obj.extend)

    # plot colrobar
    cmap_obj.plot_colorbar(ax=ax)

    figure.show()

