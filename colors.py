# In[4]:


import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

def cmap1():
    #copper = cm.get_cmap('copper', 100)
    
    #n=number of attractors
    #indices: -1 -> didn't reach an attractor -> black; 0 -> reached infinity -> cmap_infinity
    colors_black=[[0,0,0],[0,0,0]],[0,1]#index=-1
    colors_infinity=[[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]], [i/6 for i in range(7)]## index=0
    attractor_colorlists=[colors_black,colors_infinity]
    n=len(attractor_colorlists)
    colors_n=[]
    nodes_n=[]
    for i in range(n):
        colors_n.extend(attractor_colorlists[i][0])
        nodes_n.extend([node/n+i/n for node in attractor_colorlists[i][1]])
    return LinearSegmentedColormap.from_list("mycmap",list(zip(nodes_n, colors_n))),n

cm_np,n=cmap1()
def colormap_np(M,offset=0,cyclelength=100):
    return np.array(255*cm_np(
        ((((M[:,:,0]+offset)/cyclelength)%1+(M[:,:,1]+1))/n)%1
        ),dtype=np.uint8)#

#[[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]], [i/6 for i in range(7)]#rainbow
#[[1,1,1],[112/255,173/255,71/255],[46/255,117/255,182/255],[143/255,170/255,220/255],[1,1,1]],[i/4 for i in range(5)]#sky and green
#[[1,1,1],[143/255,170/255,220/255],[46/255,117/255,182/255],[112/255,173/255,71/255],[1,1,1]],[i/4 for i in range(5)]#sky and green backwards
#[[1,1,1],[1,0,0],[0,0,0],[0,1,0],[1,1,1]],[i/4 for i in range(5)]#red black green black
#[[0/255,214/255,87/255],[146/255,0/255,192/255],[254/255,97/255,0/255],[186/255,200/255,0/255],[0/255,214/255,87/255]],[0,1/3,2/3,5/6,1]#green purple orange