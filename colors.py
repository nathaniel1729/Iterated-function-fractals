# In[4]:


import numpy as np
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

def cmap1():
    #copper = cm.get_cmap('copper', 100)
    
    #n=number of attractors
    #indices: -1 -> didn't reach an attractor -> black; 0 -> reached infinity -> cmap_infinity
    colors_black=[[0,0,0],[0,0,0]],[0,1]#index=-1
    colors_infinity=[[0,0,0],[0,0,.25],[0,0,.7],[0,.7,.6],[.4,0,.7],[0,0,0.25],[0,0,0]],[0,.3,.4,.5,.6,.7,1]#black-blue-teal-purple (kind of cool)
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
    # offset=-5# Increasing the number pushes colors outward
    return np.array(255*cm_np(
        ((((M[:,:,0]+offset)/cyclelength)%1+(M[:,:,1]+1))/n)%1
        ),dtype=np.uint8)#

#[[1,0,0],[1,1,0],[0,1,0],[0,1,1],[0,0,1],[1,0,1],[1,0,0]], [i/6 for i in range(7)]#rainbow (some would say jarringly bright. I like it.)
#[[.6,0,.2],[.7,.7,0],[0,.4,.2],[0,.5,.7],[0,.1,.7],[.6,0,.7],[.6,0,.2]], [i/6 for i in range(7)]#chill rainbow (kind of sad. But usable. Just, dim.)
#[[1,1,1],[0,0,0],[.1,.1,.1],[1,0,0],[1,1,0],[0,1,0],[0,.8,.8],[0,0,1],[.2,0,.6],[.1,.1,.1],[0,0,0],[1,1,1]], [0,.1,.22,.3,.38,.46,.54,.62,.7,.78,.9,1]#prismatic: black with rainbow and white streaks. (fantastic at exactly one thing)
#[[1,1,1],[112/255,173/255,71/255],[46/255,117/255,182/255],[143/255,170/255,220/255],[1,1,1]],[i/4 for i in range(5)]#sky and green (sometimes a bit skylike, with clouds! maybe would be better without the green. Medium-good.)
#[[1,1,1],[143/255,170/255,220/255],[46/255,117/255,182/255],[112/255,173/255,71/255],[1,1,1]],[i/4 for i in range(5)]#sky and green backwards (looks less like a sky, sometimes like a swamp. Medium.)
#[[1,1,1],[46/255,117/255,182/255],[1,1,1]],[i/2 for i in range(3)]#sky and clouds (better than expected! nice!)
#[[1,1,1],[1,0,0],[0,0,0],[0,1,0],[1,1,1]],[i/4 for i in range(5)]#red black green white (Christmas! I like this one)
#[[0/255,214/255,87/255],[146/255,0/255,192/255],[254/255,97/255,0/255],[186/255,200/255,0/255],[0/255,214/255,87/255]],[0,1/3,2/3,5/6,1]#green purple orange (bright like the rainbow, but weirder. Good.)
#[[0,0,0],[0,0,1],[0,.3,.6],[0,0,0]],[0,.5,.75,1]#bright blue,grey (way too much blue)
#[[0,0,0],[0,.025,.15],[0,.1,.6],[0,.45,.675],[0,.5,.3],[0,0,0]],[0,.25,.5,.675,.75,1]#blue-green-black (dull but not the worst)
#[[0,0,0],[0,0,.25],[0,0,1],[1,1,1],[0,.45,1],[0,.25,0],[0,0,0]],[0,.3,.4,.5,.6,.7,1]#black-blue-white-greenish (too high contrast, not great)
#[[0,0,0],[0,0,.25],[0,0,.7],[.4,.4,.9],[.4,0,.7],[0,0,0.25],[0,0,0]],[0,.3,.4,.5,.6,.7,1]#black-blue-purple (almost as cool as the similar one with teal)
#[[0,0,0],[0,0,.25],[0,0,.7],[0,.7,.6],[.4,0,.7],[0,0,0.25],[0,0,0]],[0,.3,.4,.5,.6,.7,1]#black-blue-teal-purple (kind of cool)
#[[0,.5,0],[0,.8,.4],[0,.2,.2],[0,0,.4],[0,0,0],[0,.5,0]],[0,.25,.5,.625,.75,1]#soft_green with blue (the blue is weirdly intense, almost neon-looking. Not a fan.)
#[[0,.5,0],[0,.8,.4],[0,.2,.2],[0,0,0],[0,.5,0]],[0,.25,.5,.625,1]#soft_green without blue, or green-gray (pretty good)
#[[0,0,0],[.5,0,.25],[1,.5,1],[1,1,1],[1,.5,1],[.25,0,.5],[0,0,0]],[0,.25,.4,.5,.6,.75,1]#plasma (great!)
#[[6/16,3/16,0],[8/16,3.5/16,1/16],[4/16,2/16,0],[6/16,3/16,0]],[0,.333,.667,1]#brown (very low contrast, a bit like leather? not great)
#[[0,0,.2],[0,.4,.5],[0,0,.2]],[0,.5,1]#non-bright blue (too low contrast, but pretty)
#[[0,0,0],[.1,0,0],[182/255,10/255,0],[202/255,59/255,0/255],[237/255,132/255,0/255],[202/255,59/255,0/255],[182/255,10/255,0],[.1,0,0],[0,0,0]],[0,.13,.38,.44,.5,.56,.62,.87,1]#Lava (not sure if I got it quite though) (still really good though)
#[[0,0,0],[.1,0,0],[182/255,10/255,0],[1,.3,0],[1,1,.4],[1,.3,0],[182/255,10/255,0],[.1,0,0],[0,0,0]],[0,.2,.3,.4,.5,.6,.7,.8,1]#Sauron (like Lava but hotter) (eh.)
#[[0,0,0],[0,0,0],[1,.4,0],[0,0,0]],[0,.2,.6,1]#Halloween (meh)
# [[0,0,0],[.5,0,0],[.4,0,.7],[0,0,.5],[0,0,0]],[0,.25,.5,.75,1]#dark, blue and red (not a fan)
#(lambda n:([[1,1,1],[1,1,1],[1,0,0],[1,0,0]]*n, [((i+1)//2)/(2*n) for i in range(4*n)]))(10)#candy cane (A mistake. Maybe could be used for the back of playing cards?)
#[[0,0,0],[0,.5,.1],[0,0,0]],[i/2 for i in range(3)]#pine tree (simple and good, but not treelike)
#[[.5819,.9468,.5984],[.0445,.5147,.2605],[.5819,.9468,.5984]],[i/2 for i in range(3)]#random twocolor, dark and pale green. (simple and good!)
#[[.7966,.1993,.5540],[.9193,.7184,.6301],[.7966,.1993,.5540]],[i/2 for i in range(3)]#random twocolor, magenta and skin color. (simple, not desirable)
#[[.8658,.6182,.4197],[.1688,.8536,.3937],[.8658,.6182,.4197]],[i/2 for i in range(3)]#random twocolor, pinkish orange and light green. (simple, and simply bad. Also the pink one is a pretty good (more tan) skin color)
#[[0,0,0],[1,.3,0],[1,.5,.5],[1,1,.4],[1,1,1],[0,.3,1],[0,0,0]],[i/6 for i in range(7)]#sunset:black,red,pink,goldenyellow,white,deep blue,black. (Not actually remotely like a sunset, but pretty)
#[[0,0,0],[1,1,1],[0,0,0]],[i/2 for i in range(3)]#black and white. (exactly how it sounds)
#[[.2808,.6653,.6918],[.0714,.3763,.7626],[.2808,.6653,.6918]],[i/2 for i in range(3)]#random twocolor, light blue and slightly lighter, greener light blue (not bad, but not worth the trouble. too low contrast.)
#[[0,0,0],[.20,.73,.76],[0,0,0]],[i/2 for i in range(3)]#black+pale blue (nice)
# [[0,0,0],[.52,.44,.87],[0,0,0]],[i/2 for i in range(3)]#black+purple (okay. Dim.)

# C: -1.749001060266909 + 0.0002484749024054004j# Banana
# stepsize: 1.3777737303224153e-12
#[[0,0,0],[.05,.02,0],[.7,.3,0],[.9,.6,0],[1,.7,0],[.9,.6,0],[.7,.3,0],[0,0,0]],[0,.23,.32,.53,.6,.67,.91,1]#Banana (pretty good, medium good for a banana)

