'''Utitlity functions to load colormap definitions

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2023-11-28 13:25:44.
'''

import os
from typing import List
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from .colormap import ColorMapGroup, create_cmap_from_csv


def get_config_path() -> str:
    '''Get the user config folder

    Returns:
        config_path (str): default user config location in the OS.

    In Linux and MacOS: default to the 'XDG_CONFIG_HOME' environment variable.
    In Windows, default to the 'APPDATA' environment variable.
    '''

    if 'APPDATA' in os.environ:
        config_path = os.environ['APPDATA']
    elif 'XDG_CONFIG_HOME' in os.environ:
        config_path = os.environ['XDG_CONFIG_HOME']
    else:
        config_path = os.path.join(os.environ['HOME'], '.config')

    return config_path


def get_custom_def_folder() -> str:
    '''Return the custom colormap definition folder

    Returns:
        def_folder (str): folder to save for custom user colormap definitions.
        This is default to a 'colormaps' folder inside the user's default config
        folder.
        The default config folder,
        in Linux and MacOS: default to the 'XDG_CONFIG_HOME' environment variable;
        in Windows, default to the 'APPDATA' environment variable.
    '''

    config_path = get_config_path()
    def_folder = os.path.join(config_path, 'geo_colormaps')

    return def_folder


def load_simhei_font() -> None:
    '''Load SimHei.ttf font file'''

    font_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'SimHei.ttf')

    if not os.path.exists(font_file):
        return

    font_manager.fontManager.addfont(font_file)
    fprop = font_manager.FontProperties(fname=font_file)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = fprop.get_name()

    return



def load_colormaps(def_folder: str, image_folder: str) -> List:
    '''Load colormap definitions from csv files

    Args:
        def_folder (str): base folder containing subfolders. Each subfolder
            is treated as a ColorMapGroup, and contains a number of csv files,
            defining individual colormaps.
        image_folder (str): base folder to save colorbar sample images.

    Returns:
        names (list): list of tuples (ColorMapGroup name, ColorMapGroup obj).
    '''

    def_folder = os.path.abspath(def_folder)
    image_folder = os.path.abspath(image_folder)
    base_folder = def_folder

    names = []

    # loop through sub folders
    for subdir in os.listdir(def_folder):
        if not subdir.endswith('colormaps'):
            continue

        subdir_path = os.path.join(def_folder, subdir)
        img_folder = os.path.join(image_folder, subdir)
        colormap_group = ColorMapGroup(name=subdir, folder=subdir_path,
                                       base_folder=base_folder,
                                       img_folder=img_folder)

        csv_files = os.listdir(subdir_path)

        # loop through csv files
        for ff in csv_files:
            if os.path.splitext(ff)[1] != '.csv':
                continue

            path = os.path.join(subdir_path, ff)

            try:
                cmap = create_cmap_from_csv(path)
            except:
                print(f'Failed to load colormap from file: {path}. Skip.')
            else:
                colormap_group.add(cmap)

        colormap_group.plot_colormaps()
        names.append((subdir.upper(), colormap_group))

    return names


load_simhei_font()
