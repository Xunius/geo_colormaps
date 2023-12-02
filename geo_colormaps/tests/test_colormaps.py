'''Test matplotlib plot using geo_colormaps

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2023-11-23 13:36:19.
'''

import os
#import shutil
import unittest
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
import geo_colormaps

current_dir = os.path.dirname(__file__)
DATA_FILE_NAME = os.path.join(current_dir, 'fixtures', 'sample_erai_data.npz')

def readData(varid):
    '''Read in a variable from an netcdf file

    Args:
        abpath_in (str): absolute file path to the netcdf file.
        varid (str): id of variable to read.
    Returns:
        ncvarNV (NCVAR): variable stored as an NCVAR obj.
    '''

    npzfile = np.load(DATA_FILE_NAME)
    var = npzfile[varid]

    return var


class TestCartopyPlots(unittest.TestCase):
    '''Test Cartopy plots'''

    def setUp(self):
        '''Do preparation before test'''

        self.fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.output_dir = os.path.join(os.path.dirname(__file__), 'outputs')

        self.var1 = readData('msl')
        self.var2 = readData('sst')
        self.u    = readData('u')
        self.v    = readData('v')
        self.lats = readData('lats')
        self.lons = readData('lons')


    def test_cma_sst_colormap(self):

        figure = plt.figure(figsize=(8, 6), dpi=100)
        ax = figure.add_subplot(111)

        cmap_obj = geo_colormaps.CMA_COLORMAPS.SST_CMAP
        var = self.var2[0] - 273.15
        var = np.where(var > 1e5, np.nan, var)
        lats = self.lats
        lons = self.lons
        ax.contourf(lons, lats, var,
                         cmap=cmap_obj.cmap,
                         norm=cmap_obj.norm,
                         extend=cmap_obj.extend)

        cmap_obj.plot_colorbar(ax=ax)

        figure.show()

        #----------------- Save plot ------------
        plot_save_name = 'test_cma_sst_colormap.png'
        plot_save_name = os.path.join(self.output_dir, plot_save_name)
        os.makedirs(self.output_dir, exist_ok=True)
        print('\n# <test_cartopy>: Save figure to {}'.format(plot_save_name))
        figure.savefig(plot_save_name, dpi=100, bbox_inches='tight')

        self.assertTrue(os.path.exists(plot_save_name),
                        msg='{} not created.'.format(plot_save_name))

        return



    def tearDown(self):
        '''Do clean up after test'''

        try:
            #shutil.rmtree(self.output_dir)
            pass
        except:
            pass
        else:
            print('output folder removed: {}'.format(self.output_dir))

        return



if __name__ == '__main__':

    unittest.main()
    # to run in commandline:
    # python -m unittest tests/test_module.py
    # to run all tests in tests/ folder:
    # python -m unittest discover -s tests
    # NOTE: Start directory and subdirectories containing tests must be regular package that have __ini__.py file.
