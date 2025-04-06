#!/usr/bin/python

# geo_colormap
from setuptools import find_packages, setup

setup(name='geo_colormaps',
        version='0.2.0',
        description='geo_colormap is a collection of standard weather/ocean colormaps, for creating plots using `matplotlib`. It allows easy additions of custom colormaps using csv tables.',
        author='Guangzhi XU',
        author_email='xugzhi1987@gmail.com',
        url='https://github.com/Xunius/geo_colormaps',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering :: Atmospheric Science'
            ],
        install_requires=[
            "numpy",
            "matplotlib",
        ],
        packages=find_packages(include=['geo_colormaps', 'geo_colormaps.*']),
        include_package_data=True,
        python_requires = ">=3.5",
        license='GPL-3.0-or-later'
        )

