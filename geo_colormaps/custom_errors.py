'''Custom exceptions

Author: guangzhi XU (xugzhi1987@gmail.com)
Update time: 2025-04-04 15:10:39
'''

class GeoColormapsBaseError(Exception):
    '''Base Error'''

    def __init__(self, string=None):
        if string is not None:
            self.message = string

    def __str__(self):
        return self.message


class ColormapLoadError(GeoColormapsBaseError):
    message = 'Failed to import some colormaps'

    def __init__(self, string=None):
        if string is not None:
            self.message = string

    def __str__(self):
        return self.message
