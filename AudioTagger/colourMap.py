
import matplotlib.cm as cm
import matplotlib.colors as col
from matplotlib.colors import LinearSegmentedColormap


def getColourMap():
    """
    Function that defines colormap to be used to view spectrograms.

    getColourMap code from http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps.

    Colormap colours are adapted from gist_stern colormap in Matplotlib library, available:

    https://github.com/matplotlib/matplotlib/blob/ab3aa58867ecce6cc6c377c8aaff1e6074a27cdb/lib/matplotlib/_cm.py

    """
    # Original
    # cdict = {'red': ((0.000, 0.000, 0.000),
    # (0.0547, 1.000, 1.000),
    # (0.250, 0.027, 0.250),
    # (0.650, 1.000, 1.000),
    # (0.750, 1.000, 1.000),
    # (0.800, 1.000, 1.000),
    # (0.850, 1.000, 1.000),
    # (1.000, 0.000, 0.000)),
    # 'green': ((0.000, 0.000, 0.000),
    # (0.700, 1.000, 1.000),
    # (1.000, 0.000, 0.000)),
    # 'blue': ((0.000, 0.000, 0.000),
    # (0.400, 1.000, 1.000),
    # (0.500, 1.000, 1.000),
    # (0.635, 0.500, 0.500),
    # (0.700, 1.000, 1.000),
    # (1.000, 0.000, 0.000))}

    # Yellow enhanced
    # cdict = {'red': ((0.000, 0.000, 0.000),
    # (0.0547, 1.000, 1.000),
    # (0.250, 0.027, 0.250),
    # (0.500, 0.21960784494876862, 0.21960784494876862),
    # (0.700, 1.0, 1.0),
    # (0.800, 1.000, 1.000),
    # (0.850, 1.000, 1.000),
    # (1.000, 0.000, 0.000)),
    # 'green': ((0.000, 0.000, 0.000),
    # (0.500, 0.42352941632270813, 0.42352941632270813),
    # (0.700, 1.0, 1.0),
    # (1.000, 0.000, 0.000)),
    # 'blue': ((0.000, 0.000, 0.000),
    # (0.400, 1.000, 1.000),
    # (0.500, 0.69019609689712524, 0.69019609689712524),
    # (0.700, 0.20000002384185791, 0.20000002384185791),
    # (1.000, 0.000, 0.000))}

    # Black background yellow and red sounds - standard AudioTagger map
    # cdict = {'red': ((0.000, 0.000, 0.000),
    # (0.525, 0.0, 0.0),
    # (0.650, 1.0, 1.0),
    # (0.700, 0.69, 0.69),
    # (0.750, 0.69, 0.69),
    # (0.800, 0.000, 0.000),
    # (1.000, 0.000, 0.000)),
    # 'green': ((0.000, 0.000, 0.000),
    # (0.525, 0.0, 0.0),
    # (0.650, 1.0, 1.0),
    # (0.700, 0.349, 0.349),
    # (1.000, 0.000, 0.000)),
    # 'blue': ((0.000, 0.000, 0.000),
    # (0.525, 0.0, 0.0),
    # (0.650, 0.50000002384185791, 0.50000002384185791),
    # (0.700, 0.156, 0.156),
    # (1.000, 0.000, 0.000))}

    # Blue Low Amplitude and Red High Amplitude
    cdict = {'red': ((0., 0, 0),
                     (0.35, 0, 0),
                     (0.66, 1, 1),
                     (0.89, 1, 1),
                     (1, 0.5, 0.5)),
             'green': ((0., 0, 0),
                       (0.125, 0, 0),
                       (0.375, 1, 1),
                       (0.64, 1, 1),
                       (0.91, 0, 0),
                       (1, 0, 0)),
             'blue':  ((0., 0.5, 0.5),
                       (0.11, 1, 1),
                       (0.34, 1, 1),
                       (0.65, 0, 0),
                       (1, 0, 0))}

    # Colourmap for RM14_3YB files
    # cdict = {'red': ((0.000, 0.000, 0.000),
    # (0.625, 0.0, 0.0),
    # (0.750, 1.0, 1.0),
    # (0.800, 0.69, 0.69),
    # (0.850, 0.69, 0.69),
    # (0.900, 0.000, 0.000),
    # (1.000, 0.000, 0.000)),
    # 'green': ((0.000, 0.000, 0.000),
    # (0.625, 0.0, 0.0),
    # (0.750, 1.0, 1.0),
    # (0.800, 0.349, 0.349),
    # (1.000, 0.000, 0.000)),
    # 'blue': ((0.000, 0.000, 0.000),
    # (0.625, 0.0, 0.0),
    # (0.750, 0.50000002384185791, 0.50000002384185791),
    # (0.800, 0.156, 0.156),
    # (1.000, 0.000, 0.000))}

    cmap1 = col.LinearSegmentedColormap('SpecCM', cdict, N=256, gamma=0.75)
    cm.register_cmap(name='specColormap', cmap=cmap1)
    return cmap1


if __name__ == "__main__":
    getColourMap()
