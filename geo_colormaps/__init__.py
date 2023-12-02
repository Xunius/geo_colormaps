'''Load colormap defs into namespace of geo_colormaps

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2023-11-21 10:04:55.
'''

import os
from jinja2 import Environment, FileSystemLoader

from .loader import load_colormaps, get_custom_def_folder

# If True, the colormap_list.md file is updated in this repo's root folder.

# If False, the colormap_list.md is updated into a file inside user's default
# config folder,
# in Linux/MacOS, this is `$XDG_CONFIG_HOME/geo_colormaps/colormap_list.md`.
# in Windows, it is `%appdata%\geo_colormaps\colormap_list.md`.
# Only set to True when developing this package
IS_DEV = False


#-------------------Some folders-------------------
# default colormap definition folder
DEFAULT_DEF_FOLDER = os.path.join(os.path.dirname(__file__), 'colormap_defs')

# custom colormap definition folder
CUSTOM_FOLDER = get_custom_def_folder()

# folder to store default images of plotted colorbars
DEFAULT_IMG_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'images')

# folder to store user custom images of plotted colorbars
CUSTOM_IMG_FOLDER = os.path.join(CUSTOM_FOLDER, 'images')

# markdown file to store defeault colormap list
DEFAULT_COLORMAP_LIST_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'colormap_list.md'))

# markdown file to store default + user custom colormap list
CUSTOM_COLORMAP_LIST_FILE = os.path.join(CUSTOM_FOLDER, 'colormap_list.md')






def render_colormap_list_doc(colormap_group_list: list, colormap_list_file: str,
                             is_default: bool) -> None:

    # load jinja template
    jinja_template_path = os.path.join(os.path.dirname(__file__), 'docs', 'templates')
    env = Environment(loader=FileSystemLoader(jinja_template_path))
    template = env.get_template('colormap_list.md')

    # render jinja template
    colormap_groups = []
    for ii, (_, groupii) in enumerate(colormap_group_list):
        if is_default:
            # if render default list, do not add absolute paths
            groupii.base_folder = 'geo_colormaps/colormap_defs'
            groupii.img_folder = os.path.join('images', os.path.split(groupii.img_folder)[1])

        colormap_groups.append(groupii)

    try:
        readme_str = template.render({'colormap_groups': colormap_groups})
    except:
        print('Warning. Failed to render jinja template.')
    else:
        #print(readme_str)
        # save rendered jinja template to text file
        with open(colormap_list_file, 'w') as fout:
            fout.write(readme_str)

        #print(f'colormap list file {colormap_list_file} created.')

    return


# load default colormaps
default_names = load_colormaps(DEFAULT_DEF_FOLDER, DEFAULT_IMG_FOLDER)

# render default colormap list markdown file
if IS_DEV:
    render_colormap_list_doc(default_names, DEFAULT_COLORMAP_LIST_FILE, True)


# load custom colormaps
if os.path.exists(CUSTOM_FOLDER):
    try:
        custom_names = load_colormaps(CUSTOM_FOLDER, CUSTOM_IMG_FOLDER)
    except:
        print(f'Failed to load custom colormaps from {CUSTOM_FOLDER}.')
    else:
        names = default_names + custom_names


# render colormap list markdown file
if not IS_DEV:
    render_colormap_list_doc(names, CUSTOM_COLORMAP_LIST_FILE, False)


# add default + custom colormaps into this module's namespace
for name, obj in names:
    try:
        exec(f'{name} = obj')
    except:
        print(f'Failed to add name {name} to module namespace.')


#cm = __import__(__name__)
# remove these from namespace
del os, Environment, FileSystemLoader
del names, name, obj, render_colormap_list_doc, get_custom_def_folder
del IS_DEV
try:
    del custom_names, CUSTOM_FOLDER
except:
    pass
