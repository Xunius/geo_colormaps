import unittest

class TestInstall(unittest.TestCase):
    '''Test Install'''

    def test_install(self):

        for xx in ['numpy', 'matplotlib']:
            exec('import {}'.format(xx))
            print(xx, eval(xx).__version__)

if __name__ == '__main__':

    unittest.main()
    # to run in commandline:
    # python -m unittest tests/test_module.py
    # to run all tests in tests/ folder:
    # python -m unittest discover -s tests
    # NOTE: Start directory and subdirectories containing tests must be regular package that have __ini__.py file.
