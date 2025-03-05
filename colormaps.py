import matplotlib
import numpy as np
from PIL import Image, ImageTk
from colors import colormap_np

def complex_array_to_rgb(X, theme='dark', rmax=None):
    '''Takes an array of complex number and converts it to an array of [r, g, b],
    where phase gives hue and saturaton/value are given by the absolute value.
    Especially for use with imshow for complex plots.'''
    absmax = rmax or np.abs(X).max()
    Y = np.zeros(X.shape + (3,), dtype='float')
    Y[..., 0] = np.angle(X) / (2 * np.pi) % 1
    if theme == 'light':
        Y[..., 1] = np.clip(np.abs(X) / absmax, 0, 1)
        Y[..., 2] = 1
    elif theme == 'dark':
        Y[..., 1] = 1
        Y[..., 2] = np.clip(np.abs(X) / absmax, 0, 1)
    Y = matplotlib.colors.hsv_to_rgb(Y)
    return np.array(Y*255,dtype=np.uint8)

np_to_img=lambda data: ImageTk.PhotoImage(image=Image.fromarray(data))

def f_expand(n=1):
    def expand(data):
        return data.repeat(n, axis = 0).repeat(n, axis = 1)
    return expand