# In[4]:


import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

def cmap1():
    #copper = cm.get_cmap('copper', 100)
    
    #n=number of attractors
    #indices: -1 -> didn't reach an attractor -> black; 0 -> reached infinity -> cmap_infinity
    colors_black=[[0,0,0],[0,0,0]],[0,1]#index=-1
    colors_infinity=[[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]], [i/6 for i in range(7)]# index=0
    attractor_colorlists=[colors_black,colors_infinity]
    n=len(attractor_colorlists)
    colors_n=[]
    nodes_n=[]
    for i in range(n):
        colors_n.extend(attractor_colorlists[i][0])
        nodes_n.extend([node/n+i/n for node in attractor_colorlists[i][1]])
    return LinearSegmentedColormap.from_list("mycmap",list(zip(nodes_n, colors_n))),n

cm_np,n=cmap1()
def colormap_np(M):
    return np.array(255*cm_np(
        (((M[:,:,0]/100)%1+(M[:,:,1]+1))/n)%1
        ),dtype=np.uint8)#

     