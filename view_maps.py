
try:
    # import random
    import math,time
    import numpy as np
    # from PIL import Image, ImageTk
    # #set up windo_w and a few constants
    # import tkinter as tk
    # from tkinter import messagebox, simpledialog,ttk
    # from colors import colormap_np#, set_colormap, get_color
    # import function_math
    # from function_math import set_function_Magnitude,Newton,exp
    pass
except:
    print("imports failed")
    raise



def unwindow(C,W):
    """For C within the windo_w defined by a center and upper right corner, maps C to be within [0,1]x[0,1]"""
    DD=W[1]-W[0]
    CD=C-W[0]+DD
    return (np.real(CD)/(2*np.real(DD)))+(np.imag(CD)/(2*np.imag(DD)))*1j

def window(C,W):
    """For C within [0,1]x[0,1], maps C to be within the windo_w defined by a center and upper right corner."""
    DD=W[1]-W[0]
    return W[0]-DD+(np.real(C)*np.real(DD)*2)+(np.imag(C)*np.imag(DD)*2)*1j


def decanvasify(cx,cy):
    """takes coordinates in the canvas, returns a complex number in [0,1]x[0,1]"""
    #print((cx-7)/725,1-(cy-31)/723)
    return complex((cx-11)/725,1-(cy-35)/723)
def canvasify(Z):
    """takes a complex number in [0,1]x[0,1], returns coordinates in the canvas"""
    return int(Z.real*725+11),int((1-Z.imag)*723+35)






def view_C_lin(point,Q):
    return np.transpose(np.array([np.zeros_like(point,dtype=np.complex),point]),(1,2,0))
def inv_view_C_lin(C,Q):
    return C


def view_J_lin(point,Q):
    return np.transpose(np.array([point,np.zeros_like(point,dtype=np.complex)+Q]),(1,2,0))
def inv_view_J_lin(C,Q):
    return C

e=complex(math.exp(1),0)
def exp(x):
    return e**x

def complex_log(x):
    try:
        a=math.log(abs(x))
    except:
        print('log error,',x)
        a=-100
    b=math.atan2(x.imag,x.real)
    return complex(a,b)
def view_C_log_2(point,Q):
    lnC = point
    C=Q+exp(lnC)
    return np.transpose(np.array([np.zeros_like(point,dtype=np.complex),C]),(1,2,0))
def inv_view_C_log_2(C,Q):
    lnC = complex_log(C-Q)
    point=lnC
    return point

def view_J_log_2(point,Q):
    lnC = point
    C=Q[0]+exp(lnC)
    return np.transpose(np.array([C,np.zeros_like(point,dtype=np.complex)+Q[1]]),(1,2,0))
def inv_view_J_log_2(C,Q):
    lnC = complex_log(C-Q[0])
    point=lnC
    return point






