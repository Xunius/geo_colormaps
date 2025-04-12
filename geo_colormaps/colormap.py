'''自定义matplotlib色标实现

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-12 17:01:14
'''


__all__ = ['create_cmap_from_csv', 'ColorMap', 'ColorMapGroup']


# -------- Import modules -------------------------
import os
import warnings
from typing import Tuple, List, Union, Optional
from collections import namedtuple
from dataclasses import dataclass, field

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from .custom_errors import ColormapLoadError

# data to store a single level, with these fields:
# vmin, vmax: min/max value of the level, e.g. -30, -20
# if any of vmin and vmax is None, and the Level is the 1st one in the entire
# colormap, it means an underflow level. E.g. vmin=None, vmax=-30 means a level
# that corresponds to values <= -30.

# if any of vmin and vmax is None, and the Level is the last one in the entire
# colormap, it means an overflow level. E.g. vmin=40, vmax=None means a level
# that corresponds to values >= 40.

# rgb_tuple: (r, g, b) values, within range [0, 255].

# label: optional string label. E.g. '暴雨', '8级'.
Level = namedtuple('Level', ['vmin', 'vmax', 'rgb_tuple', 'label'], defaults=[''])



@dataclass
class ColorMap:
    """Colormap class

    name (str): name of colormap, e.g. 'pre'.
    unit (str): unit of colormap bin edges/centers, e.g. 'mm'.
    level_colors (list): list of Level tuples, defining the levels and colors.
    description (str): text description of the colormap.
    """

    name         : str  = ''
    unit         : str  = ''
    #level_colors : list = field(default_factory=list)
    level_colors : list = field(default_factory=list, repr=False)
    description  : str  = ''


    def __repr__(self):

        full_name = getattr(self, 'full_name', None)
        if full_name is not None:
            res = f'ColorMap(name={self.name}, unit={self.unit}, full_name={full_name}, description={self.description}'
        else:
            res = f'ColorMap(name={self.name}, unit={self.unit}, description={self.description}'
        return res


    def __post_init__(self):

        if len(self.level_colors) == 0:
            res = self.init_default_levels()
        elif len(self.level_colors) == 1:
            res = self.init_single_level()
        else:
            res = self.init_from_levels()

        self.bin_edges, self.bin_centers, self.cmap, self.norm, self.extend,\
            self.labels = res

        # colorbar ticks
        if all([x == '' or x is None for x in self.labels]):
            # if no labels, use boundary numbers as ticks
            self.ticks = self.bin_edges
            self.tick_labels = None
            self.spacing = 'proportional'
        else:
            # if labels provided, set ticks at level centers, and use uniform
            # spacing
            self.ticks = self.bin_centers
            self.tick_labels = self.labels
            self.spacing = 'uniform'

    @staticmethod
    def norm_rgb(rgb_tuple: Tuple) -> Tuple:
        '''Normalize RGB values to [0, 1] range'''
        return tuple(map(lambda x: x/255, rgb_tuple))


    @staticmethod
    def get_bin_centers(bin_edges: Union[List, np.ndarray]) -> np.ndarray:
        '''Get bin center values from bin edges'''

        bin_edges = np.array(bin_edges)
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        return bin_centers


    def init_default_levels(self):
        '''Init a default linear colormap'''

        bin_edges   = np.linspace(-1, 1, 256)
        bin_centers = self.get_bin_centers(bin_edges)
        cmap        = plt.cm.RdBu_r
        norm        = mpl.colors.Normalize()
        extend      = 'neither'
        labels      = ['']

        return bin_edges, bin_centers, cmap, norm, extend, labels


    def init_single_level(self):
        '''Init a single level colormap'''

        name        = self.name or 'my_cmap'
        vmin        = self.level_colors[0].vmin
        vmax        = self.level_colors[0].vmax
        bin_edges   = np.array([vmin, vmax])
        bin_centers = self.get_bin_centers(bin_edges)
        rgb         = self.norm_rgb(self.level_colors[0].rgb_tuple)
        cmap        = mpl.colors.ListedColormap([rgb,], name=name, N=1)
        norm        = mpl.colors.Normalize()
        extend      = 'neither'
        labels      = self.level_colors[0].label

        return bin_edges, bin_centers, cmap, norm, extend, labels


    def init_from_levels(self):
        '''Init from a list of Level objs'''

        # left most level
        first_level = self.level_colors[0]
        vmin, vmax, color, label = first_level
        if vmin is None or vmax is None:
            extend_left = True
        else:
            extend_left = False

        # right most level
        last_level = self.level_colors[-1]
        vmin, vmax, color, label = last_level
        if vmin is None or vmax is None:
            extend_right = True
        else:
            extend_right = False

        if extend_left and extend_right:
            extend = 'both'
        elif extend_left and not extend_right:
            extend = 'min'
        elif not extend_left and extend_right:
            extend = 'max'
        elif not extend_left and not extend_right:
            extend = 'neither'

        # levels in the middle
        mid_levels = self.level_colors[int(extend_left):len(self.level_colors)-\
                int(extend_right)]
        n_levels = len(mid_levels)

        # colors in the middle
        colors = [self.norm_rgb(x.rgb_tuple) for x in mid_levels]

        # labels in the middle
        labels = [x.label for x in mid_levels]

        # determine colormap is discrete or continous
        if all([x.vmin == x.vmax for x in mid_levels]):
            # if vmin == vmax for all levels
            bin_centers = [x.vmin for x in mid_levels]

            if all([x is None or len(x)==0 for x in labels]):
                # if no labels given, create continuous colormap
                # bin edges are the same as bin centers
                bin_edges = bin_centers.copy()
                is_continuous = True
            else:
                # if labels given, create discrete colormap
                # create bin edges from bin centers
                bin_edges = [bin_centers[0]*2 - bin_centers[1]] +\
                        bin_centers +\
                        [bin_centers[-1]*2 - bin_centers[-2]]
                bin_edges = self.get_bin_centers(bin_edges)

                is_continuous = False
        else:
            # if vmin != vmax for all levels, create discrete colormap
            bin_edges = [mid_levels[0].vmin,] + [x.vmax for x in mid_levels]
            bin_centers = self.get_bin_centers(bin_edges)

            is_continuous = False

        name = self.name or 'my_cmap'

        if is_continuous:
            assert len(bin_centers) == len(bin_edges), 'length wrong'
            assert len(bin_centers) == len(colors), 'length wrong'
            # create continuous colormap
            cmap = create_continuous_cmap(mid_levels, name)
            # create norm
            norm = mpl.colors.Normalize(vmin=np.min(bin_centers),
                                        vmax=np.max(bin_centers))

            self.is_continuous = True
        else:
            # create discrete colormap
            assert len(bin_edges) - len(colors) == 1, 'length wrong'
            assert len(bin_centers) == len(colors), 'length wrong'

            cmap = mpl.colors.ListedColormap(colors, name=name, N=len(colors))
            # create norm
            norm = mpl.colors.BoundaryNorm(bin_edges, n_levels)

            self.is_continuous = False

        # set overflow
        if extend_left:
            cmap.set_under(self.norm_rgb(first_level.rgb_tuple))

        if extend_right:
            cmap.set_over(self.norm_rgb(last_level.rgb_tuple))

        cmap.colorbar_extend = extend

        return bin_edges, bin_centers, cmap, norm, extend, labels


    def plot_demo(self, ax=None):
        '''Plot colorbar showing the colormap'''

        if ax is None:
            fig, ax = plt.subplots(figsize=(3, 6), dpi=100)

        vmin = np.min(self.bin_edges)
        vmax = np.max(self.bin_edges)

        # values
        yy = np.r_[np.array(vmin-1), self.bin_centers, self.bin_edges, np.array(vmax+1)]
        yy.sort()
        # make 3 columns array
        xx = np.arange(3)
        XX, YY = np.meshgrid(xx, yy)

        ax.pcolormesh(XX, YY, YY, cmap=self.cmap, norm=self.norm)
        ax.set_xticklabels([])
        ax.set_yticks(yy)

        # plot colorbar
        #cbar = fig.colorbar(cs, ax=ax, shrink=1.0, fraction=0.2,
        '''
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=self.norm,
                                                  cmap=self.cmap),
                            ax=ax,
                            ticks=self.ticks,
                            spacing=self.spacing,
                            extend=self.extend, label=self.unit)

        if self.tick_labels is not None:
            cbar.set_ticklabels(self.tick_labels)
        '''
        self.plot_colorbar(ax)

        #ax.set_title(self.description)
        title = getattr(self, 'full_name', self.description)
        ax.set_title(title)

        #fig.show()

        return ax


    def plot_colorbar(self, ax, cax=None, orientation='vertical', spacing='uniform',
                      fontsize: Optional[int]=None):

        fig = ax.get_figure()
        cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=self.norm, cmap=self.cmap),
                            ax=ax,
                            cax=cax,
                            ticks=self.ticks,
                            spacing=spacing,
                            extend=self.extend,
                            orientation=orientation,
                            label=self.unit)

        if self.tick_labels is not None:
            cbar.set_ticklabels(self.tick_labels, fontsize=fontsize)

        return cbar


    def read_from_csv(self, file_path: str):
        '''Read level and color definitions from a csv file

        Args:
            file_path (str): absolute file path to the csv file.

        Format of the csv file:

        description=<description text>
        unit=<unit string of vmin, vmax values>
        vmin , vmax , r   , g   , b  , label
        <x>  , <y>  , <r> , <g> , <b>, <optional label str>

        E.g.

        description=积雪分布图配色表
        unit=cm
        vmin , vmax , r   , g   , b   , label
        0    , 5    , 151 , 232 , 173 ,
        5    , 10   , 155 , 188 , 232 ,
        10   , 15   , 59  , 126 , 219 ,
        15   , 20   , 28  , 59  , 169 ,
        20   , 25   , 7   , 30  , 120 ,
        25   , 50   , 134 , 21  , 138 ,
        50   , None , 200 , 17  , 169 ,
        '''

        self.level_colors = []

        with open(file_path, 'r') as fin:
            # header line 1
            line = fin.readline().strip()
            self.description = line.split('=')[1]

            # header line 2
            line = fin.readline().strip()
            self.unit = line.split('=')[1]

            if self.unit[:2] == "r'" and self.unit[-1] == "'":
                self.unit = self.unit[2:-1]

            self.unit = self.unit.strip("'")

            # skip header line: vmin, vmax, r, g, b, label
            fin.readline()

            while True:
                line = fin.readline().strip()
                if len(line) == 0:
                    break

                vmin, vmax, r, g, b, label = line.split(',')

                vmin = vmin.strip(' ')
                if vmin == 'None':
                    vmin = None
                else:
                    vmin = float(vmin)

                vmax = vmax.strip(' ')
                if vmax == 'None':
                    vmax = None
                else:
                    vmax = float(vmax)

                r = int(r.strip(' '))
                g = int(g.strip(' '))
                b = int(b.strip(' '))
                label = label.strip(' ')

                ll = Level(vmin, vmax, (r, g, b), label)
                self.level_colors.append(ll)

        # name of the colormap is defined by: taking the file name of the
        # csv file, converted to upper case, and appended by '_CMAP'
        # e.g. rh.csv defines a colormap with name: RH_CMAP
        name = os.path.basename(file_path)
        name = '{}_CMAP'.format(os.path.splitext(name)[0].upper())
        self.name = name

        self.__post_init__()

        return self


@dataclass
class ColorMapGroup:

    name        : str = ''
    folder      : str = ''
    base_folder : str = ''
    img_folder  : str = ''
    collection  : dict = field(default_factory=dict)
    description : str = ''

    def add(self, new: Union[ColorMap, 'ColorMapGroup']) -> None:
        '''Add new member sub-group or ColorMap to group'''
        # add member to collection dict
        self.collection[new.name] = new
        # set member as attribute
        self.__setattr__(new.name, new)
        # set self.name as member attribute
        setattr(new, 'group_name', self.name.upper())
        # set member's full name attribute
        setattr(new, 'full_name', f'{self.name.upper()}.{new.name.upper()}')

        return

    def remove(self, thing: Union[str, ColorMap, 'ColorMapGroup']) -> None:

        if isinstance(thing, str):
            key = thing
        elif isinstance(thing, (ColorMap, ColorMapGroup)):
            key = thing.name
        else:
            raise ValueError('<colormap> must be of type str or ColorMap or ColorMapGroup')

        try:
            del self.collection[key]
        except KeyError:
            print(f'{key} not in collection')

        return

    def info(self, verbose=False) -> None:

        count = len(self.collection)
        print(f'This ColorMapGroup has {count} elements:')

        for ii, (key, value) in enumerate(self.collection.items()):
            if verbose:
                print(f'{ii+1}/{count} {key}:')
                print(value)
            else:
                print(f'{ii+1}/{count} {value.name}: {value.description}')

        return


    def __getattr__(self, item):

        return self.collection[item]


    def __set__(self, key: str, value: Union[ColorMap, 'ColorMapGroup']) -> None:

        self.collection[key] = value

        return

    def plot_colormaps(self, output_dir: Optional[str]=None):

        if output_dir is None:
            output_dir = self.img_folder

        os.makedirs(output_dir, exist_ok=True)

        for kk, vv in self.collection.items():

            plot_save_name = '{}_demo.png'.format(vv.description)
            plot_save_name = os.path.join(output_dir, plot_save_name)

            if os.path.exists(plot_save_name):
                #print(f'file {plot_save_name} exists. skip plotting')
                continue

            #print(f'Plotting {kk}')
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                ax = vv.plot_demo()
                fig = ax.get_figure()

                #----------------- Save plot------------
                #print('\n# <cma_colors>: Save figure to', plot_save_name)
                fig.savefig(plot_save_name, dpi=100, bbox_inches='tight')
                plt.close(fig)

        return


def create_cmap_from_csv(file_path: str) -> ColorMap:
    '''Helper function to create a colormap obj from csv file'''

    cmap = ColorMap()
    try:
        cmap.read_from_csv(file_path)
    except Exception:
        raise ColormapLoadError(f'Failed to load colormap from file: {file_path}.')

    return cmap


def create_cmap_from_levels(levels: Union[list, tuple, np.ndarray],
                            unit: Optional[str]='',
                            cmap: Union[None, str]=None,
                            is_continuous: bool=False) -> ColorMap:
    '''Helper function to create a colormap obj from given levels and a mpl colormap

    Args:
        levels (list, tuple or 1darray): 1d sequence of value levels.
    Keyword Args:
        unit (str): unit for values in levels.
        cmap (str or None): name of built-in matplotlib colormap name, e.g. 'jet', 'rainbow'.
            If None, use default (gist_rainbow).
        is_continuous (bool): if True, create continuous colormap. If False,
            colormap is discrete.
    Returns:
        cmap (ColorMap): created ColorMap obj.
    '''

    if cmap is None:
        cmap = plt.cm.gist_rainbow
    elif isinstance(cmap, str):
        cmap = getattr(plt.cm, cmap)
    else:
        cmap = plt.cm.gist_rainbow

    color_list = []

    if all(isinstance(x, tuple) for x in levels):
        # if levels are all tuples, this is a categorical colormap
        # e.g. [(0, ), (1, )], or
        # e.g. [(0, 'class-1'), (1, 'class-2')]

        n_levels = len(levels)
        for ii, levelii in enumerate(levels):
            leftii, *labelii = levelii
            if len(labelii):
                labelii = str(labelii[0])
            else:
                labelii = str(leftii)
            colorii = cmap(ii / n_levels, bytes=True)
            levelii = Level(leftii, leftii, colorii, labelii)
            color_list.append(levelii)

    else:
        if is_continuous:
            # if continuous colormap
            n_levels = len(levels)
            for ii, leftii in enumerate(levels):
                colorii = cmap(ii / n_levels, bytes=True)
                labelii = None
                levelii = Level(leftii, leftii, colorii, labelii)
                color_list.append(levelii)
        else:
            # if create discrete colormap, use values in levels as bin edges
            n_levels = len(levels) - 1
            for ii, (leftii, rightii) in enumerate(zip(levels[:-1], levels[1:])):
                colorii = cmap(ii / n_levels, bytes=True)
                labelii = str(leftii)
                levelii = Level(leftii, rightii, colorii, labelii)
                color_list.append(levelii)

    res = ColorMap('anoymous_cmap', unit, level_colors=color_list)
    res.__post_init__()

    return res


def create_continuous_cmap(color_points: list, name: Optional[str]=None):
    """Creates a continuous colormap with linear interpolation between specified color points.

    Args:
        color_points (list): .ist of Level objects, specifying the colormap anchors.
    Keyword Args:
        name (str or None): optional name for new colormap>
    Returns:
        cmap (matplotlib.colors.LinearSegmentedColormap): The created colormap.
    """

    if len(color_points) < 2:
        raise ValueError("At least two color points are required.")

    # Sort color points by their values
    sorted_points = sorted(color_points, key=lambda x: x.vmin)
    values = [x.vmin for x in sorted_points]
    colors = [ColorMap.norm_rgb(x.rgb_tuple) for x in sorted_points]

    vmin = min(values)
    vmax = max(values)
    if vmin == vmax:
        raise ValueError("All values in color_points are the same. Cannot create a colormap.")

    # Normalize the values to [0, 1]
    positions = [(v - vmin) / (vmax - vmin) for v in values]

    # Prepare the color dictionary for LinearSegmentedColormap
    cdict = {'red': [], 'green': [], 'blue': [], 'alpha': []}
    for pos, color in zip(positions, colors):
        r, g, b, *a = color
        a = a[0] if len(a) else 1.0 # optional alpha channel
        cdict['red'].append((pos, r, r))
        cdict['green'].append((pos, g, g))
        cdict['blue'].append((pos, b, b))
        cdict['alpha'].append((pos, a, a))

    # Create the colormap
    name = name or 'my_continuous_cmap'
    cmap = mpl.colors.LinearSegmentedColormap(name, cdict)

    return cmap
