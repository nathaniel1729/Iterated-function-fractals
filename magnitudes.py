import numpy as np
from function_math import set_function_Magnitude
mag1=set_function_Magnitude()
#mag1=lambda x,y,z: [np.sin(y.real*4)//.01,0]
def Magnitude(Z):
    """gets the output of Magnitude at each point in view_domain, returns these as matrix."""
    view_domain, iteration_limits=Z,300
    width,height =view_domain.shape[:2]
    M=np.zeros((height,width,2),dtype=int)
    line = np.zeros((height,2),dtype=int)
    for n_x,xline in enumerate(view_domain):
        for n_y,point in enumerate(xline):
            mag=mag1(point[0],point[1],iteration_limits)
            #print(mag)
            line[n_y,:]=mag#,dtype=int)#np.array(
        M[:,n_x,:]=line
    return M