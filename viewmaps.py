
import math,time
import numpy as np

def Identity(C,Q):
    return C

def view_C_lin(point,Q):
    return np.transpose(np.array([np.zeros_like(point,dtype=np.complex),point]),(1,2,0))
def inv_view_C_lin(C,Q):
    return C


def view_J_lin(point,Q):
    return np.transpose(np.array([point,np.zeros_like(point,dtype=np.complex)+Q]),(1,2,0))
def inv_view_J_lin(C,Q):
    return C


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
    C=Q[1]+np.exp(lnC)
    return np.transpose(np.array([np.zeros_like(point,dtype=np.complex),C]),(1,2,0))
def inv_view_C_log_2(C,Q):
    lnC = complex_log(C-Q[1])
    point=lnC
    return point

def view_J_log_2(point,Q):
    lnC = point
    C=Q[0]+np.exp(lnC)
    return np.transpose(np.array([C,np.zeros_like(point,dtype=np.complex)+Q[1]]),(1,2,0))
def inv_view_J_log_2(C,Q):
    lnC = complex_log(C-Q[0])
    point=lnC
    return point

maps={
    "Id":Identity,
    "view_C_lin":view_C_lin,
    "view_J_lin":view_C_lin,
    "view_C_log":view_J_log_2,
    "view_J_log":view_J_log_2,
}
inv_maps={
    "Id":Identity,
    "view_C_lin":inv_view_C_lin,
    "view_J_lin":inv_view_C_lin,
    "view_C_log":inv_view_J_log_2,
    "view_J_log":inv_view_J_log_2,
}
def f_viewmap(map_type,Q):
    M=maps[map_type]
    def viewmap(point):
        C=point[:,:,0]+1j*point[:,:,1]
        return M(C,Q)
    return viewmap
def f_inv_viewmap(map_type,Q):
    M=inv_maps[map_type]
    def viewmap(point):
        C=M(point,Q)
        return np.transpose([np.real(C),np.imag(C)],(2,0,1))
    return viewmap



