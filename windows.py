import numpy as np

def f_construct(shape): 
    def construct(a):
        x,y=np.linspace(0,1,shape[0]),np.linspace(1,0,shape[1])
        Y,X=np.meshgrid(y,x)
        return np.transpose(np.array([X,Y]),(1,2,0))
    return construct



def f_window(W):
    """For C within [0,1]x[0,1], maps C to be within the windo_w defined by a center and upper right corner."""
    def window(C):
        DD=W[1]-W[0]
        return W[0]-DD+C*DD*2
    return window
def f_unwindow(W):
    """For C within the windo_w defined by a center and upper right corner, maps C to be within [0,1]x[0,1]"""
    def unwindow(C):
        DD=W[1]-W[0]
        CD=C-W[0]+DD
        return CD/(2*DD)
    return unwindow

    
# def decanvasify(cx,cy):
#     """takes coordinates in the canvas, returns a complex number in [0,1]x[0,1]"""
#     #print((cx-7)/725,1-(cy-31)/723)
#     return complex((cx-11)/725,1-(cy-35)/723)
# def canvasify(Z):
#     """takes a complex number in [0,1]x[0,1], returns coordinates in the canvas"""
#     return int(Z.real*725+11),int((1-Z.imag)*723+35)
