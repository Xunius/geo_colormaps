'''Demo script, list existing colormaps

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-06 21:11:55
'''

import geo_colormaps

if __name__ == "__main__":

    # print out colormap list
    geo_colormaps.list_cmaps()

    # create a plot of all default + custom colormap, save image to:
    # + in Linux and MacOS: default to the 'XDG_CONFIG_HOME' environment variable;
    # + in Windows, default to the 'APPDATA' environment variable.
    geo_colormaps.plot_cmaps()

