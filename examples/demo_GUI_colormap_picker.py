'''Demo script, a GUI colormap picker

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-06 07:08:56
'''

import geo_colormaps

if __name__ == "__main__":

    # launch the GUI picker
    result = geo_colormaps.gui_picker()
    if result:
        print(result)
    else:
        print("No selection was made.")


