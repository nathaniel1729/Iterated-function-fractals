#!/usr/bin/env python
# coding: utf-8

# In[1]:


pass


# To do:
# 
# number tags: 
#     #variable number, 
#     #multiples of k (slice style?), 
#     #shape (that transforms with function)? see cow
#     
# gradual resolution update
# 
# efficient motion without zooming, 
# 
# show the escape time at the location of the mouse
# 
# rendering status bar
# 
# save animations and images as image files, &/| with data (C,window, view map, f, maybe other stuff. Represent as string?)
# 
# cancel button in case you accidentally start rendering something ridiculously large
# 
# Constants user control (maxmag, etc), sliders (res, etc), show on screen(C, window, etc).
# 
# user can change function to be iterated and how to see attractors
# 
# user can change colormaps
# 
# replace console interaction with status updates in the window
# 
# maybe warning before rendering highest resolution stuff? 
# 
# improve interface
# 
# more flexible window/image stuff
# 
# poster
# 
# use numpy
# 
# support for higher precision complex numbers? 
# 
# see image/preimage of shapes under function, or n iterations (e.g. a cow)
# 

# THIS NOTEBOOK USES NUMPY! IT WON'T WORK IF YOU DOWNLOAD IT AS A .PY FILE!

# In[2]:


try:
    import random
    import math,time
    import numpy as np
    from PIL import Image, ImageTk
    #set up window and a few constants
    import tkinter as tk
    from tkinter import messagebox, simpledialog,ttk
except:
    print("imports failed")
    raise

root = tk.Tk()
res = 16
row = 726//res
col = 726//res

try:
    namefile = open("_sequence_names.txt",'r')
    #print('line1')
    names = namefile.readlines()
    #print('line2')
    sequence_names = ["_sequence_names.txt"]+[line.strip() for line in names]
    #print('line3')
    namefile.close()
    #print('line4')
except:
    #print('except')
    namefile = open("_sequence_names.txt",'w')
    namefile.close()
    sequence_names = ["_sequence_names.txt"]


# In[3]:


# set up the image and Render function
img = tk.PhotoImage(width=col*res, height=row*res)
img314 = tk.PhotoImage(width=col*res, height=row*res)
current_image=img
def show_img(img):
    label["image"] = img
def Render(M,img,label,savedata = False, draw = True, pixelsize=None):
    """
    Create an image from matrix. If savedata is True, it will save the image to a file and return the file name. 
    If draw is true, it will put the image on the canvas.
    """
    print('start render')
    #print(M)
    #data=''
    #data2=[]
    #data3=np.array([[[]]])
    global res,img314
    if pixelsize==None:
        pixelsize=res
    t1=time.time()
    #cols, rows=M.shape[:2]
    #firstround=True
    
    nlines=len(M)
    print(nlines)
    notify=int(nlines**.5)
    n=0
    print('calculating')
    tstart=time.time()#
    height, width=M.shape[0]*pixelsize,M.shape[1]*pixelsize
    data3=np.zeros((height,width,3),dtype=np.uint8)
    line3 = np.zeros((width,3),dtype=np.uint8)
    for n_y, row in enumerate(M):
        if n%notify==0:
            print(round(n/nlines,3),'t =',round(time.time()-tstart,3),'s')
        n+=1
        #line='{'
        #line2=[]
        for n_x,val in enumerate(row):
            #line=line + (' ' + get_color(val))*res
            ##markColor(6*matrix[x][y][0]/100))*res#attractor_color(matrix[x][y]))*res#
            #rgb=[int(np.random.random()*256**3),int(np.random.random()*256**3),int(np.random.random()*256**3)]
            color=get_color(val)
            rgb=[int('0x'+color[1:3],16),int('0x'+color[3:5],16),int('0x'+color[5:7],16)]
            #line2.extend([rgb]*pixelsize)
            line3[n_x*pixelsize:(n_x+1)*pixelsize,:]=np.array(rgb, dtype=np.uint8)
        data3[n_y*pixelsize:(n_y+1)*pixelsize,:,:]=line3
        
        #data=data+(line+'} ')*res
        
        
        #data2.extend([line2]*pixelsize)
        # if firstround:
        #     firstround=False
        #     data3=np.array([line2], dtype=np.uint8)
        #     print(data3)
        # np.append(data3,np.array([line2], dtype=np.uint8),0)
    
    print(data3.dtype)
    t2=time.time()
    print('time to convert matrix:',round(t2-t1,3))
    #data_array=np.array(data2, dtype=np.uint8)#no idea why this works. The dtype is apparantly super important. 
    t3=time.time()
    print('image array created','t =',round(t3-t2,3),'s')
    #print(data_array)
    #img.put(data, to=(0, 0))
    img314 =  ImageTk.PhotoImage(image=Image.fromarray(data3))#data_array))#
    t4=time.time()
    print('image created','t =',round(t4-t3,3),'s')
    print('end render')
    return img314

    ## print(img314)
    ## print(Image.fromarray(data_array,mode='RGB').getbands())
    # if savedata:
    #     return img314
    #     #filename=save(img314,savedata)
    #     #return(filename)
    # if draw:
    #     return img314
    #     #show_img(img314)
    #     #label["image"] = img
    #     #global label_id, canvas
    #     #canvas.itemconfigure(label_id, image=img)
        
        


# In[4]:


# set up the color system for the images
def brightness(x):
    """takes 0<=x<=6, returns a two-digit hex number based on the pattern
          1****2****3
         *           *
        *             *
       *               *
      *                 *
     0                   4****5****6
    """
    if 0<x<1:
        num=int(255*x)
    elif 1<=x<=3:
        return('ff')
    elif 3<x<4:
        num=int(255*(4-x))
    else:
        return('00')
    num = hex(num)[2:]
    #print(num)
    return('0'*(2-len(num))+num)

def num_to_color(rgb):
    """Converts an rgb tuple to a hex color"""
    color='#'
    for c in rgb:
        c = hex(c)[2:]
        c='0'*(2-len(c))+c
        color=color+c
    return color
    

phi=(math.sqrt(5)+1)/2
def attractor_color(x):
    """x is an integer or None. Returns a uniqe color, black if None"""
    global phi
    if x==None:
        return('#000000')
    return(markColor(1+phi*x))

def markColor(x,brightness=brightness):
    """Takes x and a function. Uses the function on r,g,b to create a cycle of hex colors, x%6 picks a color"""
    #if x==0:
    #    return('#000000')
    cycle=x%6
    red=brightness((cycle+2)%6)
    green=brightness(cycle)
    blue=brightness((cycle-2))
    hue='#'+red+green+blue
    return(hue)

def color_ring(color0,bx,by,n):
    """given 3 vectors (lists) in R^3 and integer n, creates the hex color cycle of n colors: color0 + bx*cos(t) + by*sin(t), 0<=t<2*pi,
    replacing any colors that give errors with a different color."""
    l=[]
    t=0
    dt=2*math.pi/n
    for i in range(n):
        new=[color0[i]+ math.cos(t)*bx[i]+math.sin(t)*by[i] for i in range(3)]
        l.append(list(new))
        t=t+dt
    for i in range(len(l)):
        for j in range(3):
            l[i][j]=int(max(0,min(255,l[i][j])))
    result=[num_to_color(color) for color in l]
    return result
def color_ball(color0,bx,by,bz,n,k):
    """given 4 vectors (lists) in R^3 and integers n,k, creates the hex color cycle of n colors consisting of k rings whose
    axes revolve around bz.
    replacing any colors that give errors with a different color."""
    breakup=[n//k+int(i<n%k) for i in range(k)]
    if sum(breakup)!=n:
        for i in range(100):
            print('color ball function is faulty')
        return
    result=[]
    t=0
    dt=2*math.pi/k
    for n_i in breakup:
        b_new=[math.cos(t)*bx[i]+math.sin(t)*by[i] for i in range(3)for i in range(3)]
        result.extend(color_ring(color0,bz,b_new,n_i))
        t+=dt

        
    return result
        
def highbrightness(n):
    """creates a list of n hex colors in a cycle, bright eastery theme."""
    l=[]
    for i in range(n):
        x=(3*i/n+1/2)%3
        r=int(((-abs(x-1)+2*abs(x-2)-1+x)/2)*255)
        g=int((-(abs(x-1)+abs(x-2)-3)/2)*255)
        b=int(((-abs(2-x)+2*abs(1-x)+2-x)/2)*255)
        l.append(num_to_color((r,g,b)))
    return l
def lowbrightness(n):
    """creates a list of n hex colors in a cycle, bright eastery theme."""
    l=[]
    for i in range(n):
        x=(3*i/n+1/2+3/2)%3
        r=255-int(((-abs(x-1)+2*abs(x-2)-1+x)/2)*255)
        g=255-int((-(abs(x-1)+abs(x-2)-3)/2)*255)
        b=255-int(((-abs(2-x)+2*abs(1-x)+2-x)/2)*255)
        l.append(num_to_color((r,g,b)))
    return l
def standard_colors(n):
    return [markColor(i*6/n) for i in range(n)]
#print(highbrightness(30))
Newton=False#change f when you change this
def set_colormap():
    """creates a colormap using the attractors and the point at infinity"""
    lines=[]##insert at indices 1,2 for newton
    if Newton:
        return [highbrightness(100),lowbrightness(100),color_ring([127,127,127],[128,-64,-64],[0,111,-111],100),standard_colors(100)]#color_ball([192,64,64],[96,-96,0],[48,48,-96],[96,96,96],300,3)]#
    else:
        return [highbrightness(100),standard_colors(100)]
def get_color(mag):
    """takes a list [count,i] and chooses a color cycle corresponding to attractor 'i' and a color 
    within that cycle based on 'count'"""
    
    if mag[0]==-1:
        return '#000000'
    global colormap
    if mag[1]==-1 or len(colormap)==1:
        line=colormap[-1]
    else:
        line=colormap[mag[1]%(len(colormap)-1)]
    #print(mag,len(line),mag[0]%len(line))
    return line[int(mag[0]%len(line))]
    

    


# In[5]:


#set up some complex functions and numbers

def inv(c):
    """Safe division, return 1/c unless c is 0, then returns 0."""
    if abs(c)==0:
        return c
    return 1/c

def rootcircle(n, initial = complex(1,0)):
    """creates a circle of n evenly spaced complex numbers starting with inital."""
    roots = [initial]
    angle = 2*math.pi/n
    rotate = complex(math.cos(angle),math.sin(angle))
    for i in range(n-1):
        roots.append(roots[-1]*rotate)
    return(roots)

#set centers to be the 3rd roots of unity
centers = rootcircle(3)

def P(C,roots = centers):
    """Creates the polynomial consisting of the product of (x-x0) for x0 in roots,
    evaluates this polynomial at the complex nubmer C"""
    p= complex(1,0)
    for root in roots:
        p = p*(C-root)
    return(p)

def dP(C,roots = centers):
    
    """Creates the derivative of the polynomial consisting of the product of (x-x0) for x0 in roots,
    evaluates this derivative at the complex nubmer C"""
    dp = complex(0,0)
    for i in range(len(roots)):
        dp = dp+(P(C,roots[:i]+roots[i+1:]))
    return(dp)
        

def P_dP(C,roots):
    """Creates the polynomial consisting of the product of (x-x0) for x0 in roots,
    returns a step calculated using newtons method (-P'(C)/P(C)). Will return 0 where P' is 0.
    """
    p_dp = -P(C,roots)*inv(dP(C,roots))
    return(p_dp)


e=complex(math.exp(1),0)
def exp(x):
    return e**x

######################################################################################################################
############################## most important function in the program right here #####################################
######################################################################################################################

def f(Z,C=0,roots=centers):#.285,.01)):#,C2 = complex(-3.0789856785439538, 0.2719380912620699)
    """the function to be iterated. Usually z^2+c, this gives the mandelbrot set. z+P_dP is newtons method."""
    global centers
    return(Z**2+C)#(Z+P_dP(Z,attractors))#or Z,roots#((Z-(Z**2))*C)#(Z**4-Z**2+C)#
#(Z**3+Z**2+C)#
#(e**Z+C)#
#    k=3/2*(2+C1+C2);#(Z**3/(6*k)+k*Z/2+(C1+C2)/2)
#((Z**2/(np.sqrt(Z.real**2+Z.imag**2)))*1.1+C)


C= complex(-0.11712655777245454, 0.6495111247984681)+complex(.080,.12)#weird spot under 3 bulb
Z=complex(0,0)
# #calculate attractors using C
# for i in range(5000):
#     Z=f(Z,C)
#     if abs(Z)>5:
#         break#commented out for newton stuff,but I don't think I need it anyway...
if abs(Z)<=5 and not Newton:#:#and False added for newton stuff#
    attractors=[Z]#+complex(.01,0)]
else:
    attractors=[complex(1),complex(-1),0]##for newton, insert at indices 0,1

colormap=set_colormap()


def Attractor(Z,C,roots,count=100):
    """
    given Z,C, and a list of roots, calculates which (if any) of the roots is nearly (within .1)
    reached after 100 iterations of f_C at Z, returns the index of the root or None.
    """
    while count>0:
        Z=f(Z,C,roots)
        count-=1
    for center in roots:
        if abs(Z-center)<.1:
            return(roots.index(center))
    return

r_escape=max([abs(x) for x in attractors]+[1])+4+(40000-4)*int(Newton)#was 4, changed for newton stuff to 40000
r_trap=.005
def attractor(Z):
    """
    given Z, uses the global variable attractors as a list of roots, calculates which (if any) 
    of the roots is nearly (within r_trap) reached after 100 iterations of f_C at Z, returns the 
    index of the root or -1 if Z escapes to infinity.
    """
    global attractors,r_escape,r_trap
    if abs(Z)>r_escape:
        return -1
    for i,center in enumerate(attractors):
        if abs(Z-center)<r_trap:
            return(i)
    return


def set_attractors(C,maxmag=5000,newton=False):
    """Finds Z after maxmag iterations of f_C, if |Z|<5, assumes that Z is an attractor and 
    adds it to the global variable attractors"""
    global attractors
    if newton:
        attractors=[complex(1)-C/2,complex(-1)-C/2,C]
        return
    Z=complex(0,0)
    for i in range(maxmag):
        Z=f(Z,C)
        if abs(Z)>5:
            return
    attractors=[Z]#+complex(.01,0)]#[]#
set_attractors(C,15,newton=True)
def set_function_Magnitude(find_attractor=False):
    """creates and returns one of two functions, depending on find_attractor"""
    if find_attractor==True:
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            #C = Z
            #Z=complex(0,0)
            count = 0
            set_attractors(C,15)
            while count<maxcount and attractor(Z)==None:
                Z=f(Z,C)
                count+=1
            if count == maxcount: return [-1,1]
            return([count,attractor(Z)])
        return Magnitude
    elif find_attractor=='J only':
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            #C = Z
            #Z=complex(0,0)
            count = 0
            #set_attractors(C,1500)
            if Newton:
                set_attractors(C,15,newton=True)#for newton only!
            while count<maxcount and attractor(Z)==None:
                Z=f(Z,C)
                count+=1
            if count == maxcount: 
                return [-1,-1]
            return([count,attractor(Z)])
        return Magnitude
    elif find_attractor=='test_fill':
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            return [0,472]
            # #C = Z
            # #Z=complex(0,0)
            # count = 0
            # #set_attractors(C,1500)
            # if Newton:
            #     set_attractors(C,15,newton=True)#for newton only!
            # while count<maxcount and attractor(Z)==None:
            #     Z=f(Z,C)
            #     count+=1
            # if count == maxcount: 
            #     return [-1,-1]
            # return([count,attractor(Z)])
        return Magnitude
    else:
        def Magnitude(Z,C,maxcount = 100):
            """Counts how many iterations of f_C are needed for Z to escape or reach an attractor. 
            Returns both the number of steps taken (-1 if it didn't find an attractor or escape)
            and which attractor (which index of the global variable attractors, or -1 if it escapes, or None.)
            """
            #C = Z
            #Z=complex(0,0)
            count = 0
            #set_attractors(C,1500)
            while count<maxcount and abs(Z)<10:
                try:
                    Z=f(Z,C)
                except:
                    break
                count+=1
            if count == maxcount: return [-1,-1]
            else: return [count,-1]
        return Magnitude
if Newton:
    Magnitude=set_function_Magnitude('J only')## use with newton and some other stuff
else:
    Magnitude=set_function_Magnitude()#'test_fill'


# In[6]:


#some transformations that facilitate sampling complex numbers from a particular region 
#as well as representing complex numbers on the canvas

def unwindow(C,W):
    """For C within the window defined by a center and upper right corner, maps C to be within [0,1]x[0,1]"""
    DD=W[1]-W[0]
    CD=C-W[0]+DD
    return complex(CD.real/(2*DD.real),CD.imag/(2*DD.imag))

def window(C,W):
    """For C within [0,1]x[0,1], maps C to be within the window defined by a center and upper right corner."""
    DD=W[1]-W[0]
    return W[0]-DD+complex(C.real*DD.real*2,C.imag*DD.imag*2)

def decanvasify(cx,cy):
    """takes coordinates in the canvas, returns a complex number in [0,1]x[0,1]"""
    #print((cx-7)/725,1-(cy-31)/723)
    return complex((cx-11)/725,1-(cy-35)/723)
def canvasify(Z):
    """takes a complex number in [0,1]x[0,1], returns coordinates in the canvas"""
    return int(Z.real*725+11),int((1-Z.imag)*723+35)


# In[7]:


#functions for creating images of regions of the complex plane

def view_C_lin(point,Q,Window):
    C = window(point,Window)
    return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#
def inv_view_C_lin(C,Window):
    point = unwindow(C,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

# def view_C_log(point,Q,Window):
#     lnScale=math.log(abs(Window[1]-Window[0]))-0.3465735902799727
#     lnC = window(point,[complex(lnScale-math.pi,math.pi),complex(lnScale,2*math.pi)])
#     C=Window[0]+math.exp(lnC.real)*complex(math.cos(lnC.imag),math.sin(lnC.imag))
#     return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#

def view_J_lin(point,Q,Window):
    C = window(point,Window)
    if point.imag>.8 and point.real>.8 and False:
        return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
    else:
        return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#
def inv_view_J_lin(C,Window):
    point = unwindow(C,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

# def view_J_log(point,Q,Window):
#     lnScale=math.log(abs(Window[1]-Window[0]))-0.3465735902799727
#     lnC = window(point,[complex(lnScale-math.pi,math.pi),complex(lnScale,2*math.pi)])
#     C=Window[0]+math.exp(lnC.real)*complex(math.cos(lnC.imag),math.sin(lnC.imag))
#     if point.imag>.8 and point.real>.8:
#         return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
#     else:
#         return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#

#######
def complex_log(x):
    try:
        a=math.log(abs(x))
    except:
        print('log error,',x)
        a=-100
    b=math.atan2(x.imag,x.real)
    return complex(a,b)

def view_C_log_2(point,Q,Window):
    lnC = window(point,Window)
    C=windows['C_lin'][0]+exp(lnC)
    return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#
def inv_view_C_log_2(C,Window):
    lnC = complex_log(C-windows['C_lin'][0])
    point=unwindow(lnC,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

def view_J_log_2(point,Q,Window):
    lnC = window(point,Window)
    C=windows['J_lin'][0]+exp(lnC)
    #print(windows['J_lin'])
    if point.imag>.8 and point.real>.8:
        return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
    else:
        return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#
def inv_view_J_log_2(C,Window):
    lnC = complex_log(C-windows['J_lin'][0])
    point=unwindow(lnC,Window)
    return point#Attractor(complex(0,0),C,[C]+centers[1:])#

view_map=view_C_lin
inv_view_map=inv_view_C_lin

maxmag = 1500
def set_view_domain(shape,Q,Window):
    """creates a list of lists of Z,C, maxmag triples. Global Window controls the region shown. 
    shape controls the number of rows and columns, Q is either a Z or C value depending on view_map. 
    currently, seed space view maps contain a small legend of the parameter space (C) in the 
    upper right corner, it's zoom level is determined by stepsize
    """
    print('start set_view_domain')
    global view_map,maxmag
    print(view_map)
    ##choose a map. Each map should be a function from [0,1]x[0,1] to CxC (depending on Q and Window).
    
    
    nlines=shape[0]
    print(nlines)
    notify=int(nlines**.5)
    n=0
    print('calculating')
    tstart=time.time()#
    #
    view_domain2=np.zeros(shape+(2,),dtype=complex)
    iteration_limits=np.zeros(shape,dtype=int)
    iteration_limits[:,:]=maxmag
    line2=np.zeros((shape[1],2),dtype=complex)
    #iter_line=np.zeros((shape[1],),dtype=int)
    for x in range(shape[0]):
        if n%notify==0:
            print(round(n/nlines,3),'t =',round(time.time()-tstart,3),'s')
        n+=1
        for y in range(shape[1]):
            point = complex(x/shape[0],1-y/shape[1])
            item=view_map(point,Q,Window)
            #item.extend([maxmag])
            #iter_line[y]=maxmag
            line2[y,:]=item#)#np.array(
        view_domain2[x,:,:]=line2
        #iteration_limits[x,:]=iter_line
        
    print(round(1,3),'t =',round(time.time()-tstart,3),'s')
    
    print('end set_view_domain')
    return(view_domain2,iteration_limits)


# pb = ttk.Progressbar(
#         root,
#         orient='horizontal',
#         mode='indeterminate',
#         length=180
#     )
# pb.grid(row=12,column=2,columnspan = 2)
# pb.start()
def fill(view_domain):
    """gets the output of Magnitude at each point in view_domain, returns these as matrix."""
    print('start fill')
    view_domain, iteration_limits=view_domain
    width,height =view_domain.shape[:2]
    M=np.zeros((height,width,2),dtype=int)
    nlines=width
    print(nlines)
    notify=int(nlines**.5)
    n=0
    print('calculating')
    tstart=time.time()#
    line = np.zeros((height,2),dtype=int)
    for n_x,xline in enumerate(view_domain):
        if n%notify==0:
            print(round(n/nlines,3),'t =',round(time.time()-tstart,3),'s')
        n+=1
        for n_y,point in enumerate(xline):
            mag=Magnitude(point[0],point[1],iteration_limits[n_x,n_y])
            #print(mag)
            line[n_y,:]=mag#,dtype=int)#np.array(
        M[:,n_x,:]=line
    print(round(1,3),'t =',round(time.time()-tstart,3),'s')
    print(M.shape)
    print('matrix array created')
    print('end fill')
    return(M)

domain=[]
r=-complex(0,(1.0577644392199486-0.6443213634110101)/2)
center=-r+complex((-0.19807849916533377 -0.05216187123852948)/2, -(-0.7223148298516319 -0.5763982019248275)/2)

nsteps=3
angles=[math.pi*(1+math.sin((i/nsteps-1/2)*math.pi)) for i in range(nsteps)]

for a in angles:
    domain.append(center+r*complex(math.cos(a),math.sin(a)))
    #print(domain[-1].real,domain[-1].imag)
#for c in domain:
#    print(c.real)
def prepare_frames():
    """creates a list of viewpoints, which can be rendered as a zoom sequence."""
    global scalefactor, res, C, zooming,domain
    zooming = True
    frames=[]
    minres = 8###############
    lastres = res*2
    while res != lastres and res>minres:
        lastres = res
        res_up()
    
    zoomtype='move'#'zoom'#
    if zoomtype=='zoom':
        scalefactor = .65#.9#####################
        minscale = .2#2.0134609968696852e-07###############
        try:
            C+complex(0)
        except:
            C=complex(0)
        while abs(Window[1]-Window[0])>(minscale/2**.5):
            shape=(math.ceil((int(Xm)-int(xm))/res),math.ceil((int(Ym)-int(ym))/res))
            view=set_view_domain(shape,C,Window)
            zoom_in()
            print('Window:',Window)
            frames.append(view)
            
            
    else:
        for C_i in domain:
            shape=(math.ceil((int(Xm)-int(xm))/res),math.ceil((int(Ym)-int(ym))/res))
            view=set_view_domain(shape,C_i,Window)
            frames.append(view)
    return frames


# In[8]:


# a bunch of variables and obsolete stuff, mostly.

square,xm,Xm,ym,Ym=res,-364,364,-363,363
#unwindow_og = lambda C: unwindow(C,[(complex(xm,ym)+complex(Xm,Ym))/2,complex(Xm,Ym)])#



########all the windows between here and the line of # are LL and UR corners, instead of center and UR corner##########
#C = complex((-1.2545086026025125 -1.2545085781339527)/2, (-0.38184660232426615-0.381846577855703)/2)#3-lightning->seahorse valley
#some good Z windows for viewing the above:
#Window=[complex(-1.254510943011526-.01, -0.3818442136529039-.01), complex(-1.254510943011526+.01 , -0.3818442136529039+.01)]
#Window = [complex(-0.0006404037772671987, -0.0006404037772671987), complex(0.0006404037772671987, 0.0006404037772671987)]
#Window = [complex(-2.1936950640377943e-06, -2.1936950640377943e-06), complex(2.1936950640377943e-06, 2.1936950640377943e-06)]
#Window = [complex(-0.0016796160000000027, -0.0016796160000000027), complex(0.0016796160000000027, 0.0016796160000000027)]
#1.862645149230957e-09#?????

#[complex(0.3604215953428633, -0.6413087582998904), complex(0.36042159534287416, -0.6413087582998795)]#Foot fractal (C window?)
################################################################################################################


#C = complex(0.3600112403769836 , -0.6412401127733343)#first finite partial x chain
#C = complex(-1.942401867089655,0)#point on antenna
#C = complex(0.3601577313902783 , -0.6413692730296517)#lots of multilevel detail, the first zoom sequence I made

#C = complex((-1.2597225553541898 -1.2512524556688622)/2, (-0.3776091638102406-0.3860792634955672)/2)#3-lightning->main bulb leftish
#C = complex(-0.04486189663259376 , 0.6511456779174767)# messy spirals, 3-bulb right valley
#C = complex(0.28488922119140625 , 0.011072158813476562)# almost connected nautilus, very tightly wound together in center.
#C = complex(0.28488922119140625 , 0.01107218861579895)#same as previous, but a little tighter
#0.35860048046605797 + 0.6464082787564494 i# similar to video, but with seahorses instead of shells


#I have pics already of J for both of these spots:
#C: -0.06842892391218167 + -0.663010464304677j# nice fractal with triple spirals and shells, bottom 3 bulb left 11
#C: -0.0682983692727371 + -0.6530916379390759 i# close to the above, but on the other side of the valley. 

#[(-1.7496544421700426+6.931210349204815e-05j), (-1.7496544417812514+6.931249228319112e-05j)]#img4 4
#C=(complex(0.3602404434376136+0.6413130610648023j)+complex(0.3602404434376152+0.6413130610648039j))/2#almost exactly the one from the video, this window is maximum zoom.
#C=-0.15215242321248967+1.0329351579150852j#cool variant on the 5-5 thing 
#C=0.06263749141789529+3.023722147812313j#super cool in newton
#C=0.5326542403833178+0.555620466144246j#close to Ben Beckstrom fractal

#0.5326542505796272+0.5556204832914241j#Ben Beckstrom fractal. good window:[(0.5326542505796272+0.5556204832914241j), (0.5326543571932145+0.5556205899050114j)]

#[(-1.7573291273522558+0.012074115417193047j), (-1.7573290987941184+0.012074143975330458j)]#needs way more than 1500 iterations. do later.
#0.30073456857702113+0.02007580577294269j#threads and shells
#-.7644+0j#good center for looking at whole mandelbrot set
#[(-0.06842892391218167 -0.663010464304677j), (-0.06842892391218167 -0.663010464304677j+.1+.1j)]#[C,C+complex(4,4)*stepsize]#
#[(-0.15405122541900643+1.036884037073183j), (-0.15405114560289007+1.0368841168892995j)]#3 lightning, 3 valley, bubbles (but with cool color gradients)
#[(-1.7644680509835375+0j), (-1.7374781222771942+0.026989928706343314j)]#medalion


C=-1.7644680509835375+0j
Window = [(-1.7644680509835375+0j), (-1.7374781222771942+0.026989928706343314j)]
stepsize = (Window[1]-Window[0]).real/4
ZWindow = [complex(0,0),complex(1.3,1.3)]#Window.copy()
scalefactor = .6
windows={}
windows['C_lin']=Window.copy()#[(-1.7573291273522558+0.012074115417193047j), (-1.7573290987941184+0.012074143975330458j)]#
windows['J_lin']= [complex(0,0),complex(1.3,1.3)]#
windows['C_log']=[complex(-math.pi,math.pi),complex(-math.pi,math.pi)+complex(1,1)*2*math.pi]
windows['J_log']=[complex(-math.pi,math.pi),complex(-math.pi,math.pi)+complex(1,1)*2*math.pi]
view_maps={}
view_maps['C_lin']=view_C_lin
view_maps['J_lin']=view_J_lin
view_maps['C_log']=view_C_log_2
view_maps['J_log']=view_J_log_2
inv_view_maps={}
inv_view_maps['C_lin']=inv_view_C_lin
inv_view_maps['J_lin']=inv_view_J_lin
inv_view_maps['C_log']=inv_view_C_log_2
inv_view_maps['J_log']=inv_view_J_log_2


# In[9]:


#defining the machinery that allows images and zoom sequences to be created and saved. needs a lot of work.

sequence = []
zooming = False
            

filenumber = 0
def save(img,key_name):
    """Takes data as a string of hex codes, saves it as a text file. returns the name of the file.
    the name is determined by global filenumber, which it increments, and the current value of C. 
    Reports to the console.
    """
    #global img314
    #img314.put(data, to=(0, 0))
    #print(tk.Image)
    #help(img)
    #help(tk.Image.__init__)
    #help(img314)
    
    global filenumber
    print('filenumber:',filenumber)
    filename = key_name[:-4]+' '+str(filenumber)+'.png'#'('+str(C.real)+'+'+str(C.imag)+'i).txt'
    filenumber+=1
    # f = open(filename,'w')
    # f.write(data)
    # f.close()
    img314._PhotoImage__photo.write(filename)
    
    print(filename,'this was a save')
    return(filename)
def get_valid_name(item=['sequence','Sequence','.txt']):
    """gets a filename that is not an empty string or the same as another file. 
    Returns None if the user clicks cancel."""
    sequence_key =simpledialog.askstring(''+item[1]+' Name','What would you like to name this '+item[0]+'?').strip()
    if sequence_key==None:
        return
    while sequence_key=='':
        sequence_key =simpledialog.askstring(
            ''+item[1]+' Name',
            'Sorry, that is not a valid name. What would you like to name this '+item[0]+'?'
        ).strip()
    sequence_key=sequence_key+item[2]
    while sequence_key in sequence_names:
        sequence_key =simpledialog.askstring(''+item[1]+' Name','Sorry, the name "'+sequence_key[:-4]+'" is taken. What would you like to name this '+item[0]+'?').strip()
        if sequence_key==None:
            return
        while sequence_key=='':
            sequence_key =simpledialog.askstring(
                ''+item[1]+' Name',
                'Sorry, that is not a valid name. What would you like to name this '+item[0]+'?'
            ).strip()
        sequence_key=sequence_key+item[2]
    return sequence_key
def zoom_sequence():
    """creates a zoom sequence as a series of saved png files, with an index file that has their names. 
    uses current global information to create the regions. Very slow for long or high resolution sequences.
    """
    global img, label, sequence, zooming, sequence_key
    if not messagebox.askokcancel("Zoom Sequence", "Generating a zoom sequence may take a very long time. Do you want to continue?"):
        return
    sequence_key=get_valid_name()
    if sequence_key==None: return
    sequence_names.append(sequence_key)
        
        
    zooming = True
    frames=prepare_frames()
    namelist = []
    for view in frames:
        M=fill(view)
        filename=save(Render(M,img,label, savedata = sequence_key, draw = False),sequence_key)
        namelist.append(filename)
        print('filename:',filename)
    sequence = namelist
    key = open(sequence_key,'w')
    for filename in sequence:
        key.write(filename+'\n')
    key.close()
    names = open("_sequence_names.txt",'a')
    names.write(sequence_key+'\n')
    names.close()
    zooming = False
    print('zoom sequence ready')

    


# In[10]:


#defining the machinery that allows images and zoom sequences to be recalled and displayed. needs a lot of work.


display_num = 0
sequence_data = []
go = False
def display_next():
    global go
    if go:
        Step()
        root.after(200,display_next)
        #print("going")
    else:
        print('stop1')

sequence_key = 'sequence_1.txt'
def get_sequence():
    global sequence_key, sequence_data
    names_list=''
    print(sequence_names[1:])
    for i,name in enumerate(sequence_names[1:]):
        names_list = names_list+'\n'+str(i)+') '+name
    if names_list=='':
        return
    i=simpledialog.askinteger(
                                'Display Sequence',
                                'Which sequence would you like to display? Enter a number.\n'+names_list
                            )%(len(sequence_names)-1)
    sequence_key=sequence_names[i+1]
    key = open(sequence_key)
    sequence = key.readlines()
    #print(sequence)
    sequence = [line.strip() for line in sequence]
    key.close()
    return(sequence)
def display_sequence():
    global img, label, sequence_data, go
    sequence=get_sequence()
    if sequence==None:
        return
    if len(sequence_data)==0:
        btn_Step = tk.Button(root,text='Step',width=12,height=1, command=Step)
        btn_Step.grid(row=10,column=3)
        btn_Step_back = tk.Button(root,text='Step_back',width=12,height=1, command=Step_back)
        btn_Step_back.grid(row=11,column=3)
    sequence_data = []
    for filename in sequence:
        sequence_data.append(tk.PhotoImage(file=filename))
        # f = open(filename)
        # sequence_data.append(f.read())
        # f.close()
    go = True
    display_next()
    btn_display["text"] ="Stop"
    btn_display["command"] =Stop

def Step_back():
    global display_num,img, label, sequence_data
    display_num = (display_num-1)%len(sequence_data)
    img = sequence_data[display_num]
    #img.put(data, to=(0, 0))
    show_img(img)
def Step():
    global display_num,img, label, sequence_data
    display_num = (display_num+1)%len(sequence_data)
    img = sequence_data[display_num]
    #img.put(data, to=(0, 0))
    show_img(img)
    

def Stop():
    global go
    
    print('stop2')
    go = False
    btn_display["text"] ="display_sequence"
    btn_display["command"] =display_sequence
    


# In[11]:


# functions attached to buttons. 

def Run():
    global img, label,C,current_image
    shape=(math.ceil((int(Xm)-int(xm))/res),math.ceil((int(Ym)-int(ym))/res))
    view=set_view_domain(shape,C,Window)
    M=fill(view)
    img314=Render(M,img,label)
    current_image=img314
    show_img(img314)
    print('C:',C.real,'+',C.imag,'i')
    print('stepsize:',stepsize)
    print('res:',res)
    print('Window:',Window)
    print()
    return
    #global go
    #go = True
    #regular_step()
    #btnRun["text"] ="Stop"
    #btnRun["command"] =Stop

######
def res_up():
    global res, row, col
    if res%2==0:
        res = res//2
        row = row*2
        col = col*2
    return

def res_down():
    global res, row, col
    if col%2==0 and row%2 == 0:
        res = res*2
        row = row//2
        col = col//2
    return
######
def stepsize_down():
    global stepsize
    stepsize = stepsize/2
    update_window()
    return

def stepsize_up():
    global stepsize
    stepsize = stepsize*2
    update_window()
    return
######
def C_r_down():
    global stepsize,C
    C-=stepsize
    update_window()
    return

def C_r_up():
    global stepsize,C
    C+=stepsize
    update_window()
    return
######
def C_i_down():
    global stepsize,C
    C-=complex(0,stepsize)
    update_window()
    return

def C_i_up():
    global stepsize,C
    C+=complex(0,stepsize)
    update_window()
    return

######

def get_size_res():
    """gets a size and resolution for the image to be saved."""
    customize =messagebox.askyesno(
        'Resolution and Size',
        'Customize resolution and size? (Click No to use current resolution and size) '
    )
    if not customize:
        return 'current'
    resolution =simpledialog.askinteger(
        'Resolution and Size',
        'Resolution?'
    )
    
    size =simpledialog.askinteger(
        'Resolution and Size',
        'Size?'
    )
    
    return [resolution,size]


def save_image():
    filename=get_valid_name(item=['image','Image','.png'])
    res_size=get_size_res()
    if res_size=='current':
        save(current_image,filename)
    else:
        global img, C
        shape=(math.ceil((res_size[1])/res_size[0]),math.ceil(res_size[1]/res_size[0]))
        view=set_view_domain(shape,C,Window)
        M=fill(view)
        img=Render(M,img,label,pixelsize=res_size[0])
        save(img,filename)
    
    # shape=(math.ceil((int(Xm)-int(xm))/res),math.ceil((int(Ym)-int(ym))/res))
    # view=set_view_domain(shape,C,Window)
    # M=fill(view)
    
    #     global stepsize,C
    #     C = complex(2*random.random()-1,2*random.random()-1)
    #     update_window()
    #     return
######
centered_zoom=False
def zoom_point(point,inout=1):
    """zoom the window in if inout=1, out if its -1, centered around window(point)"""
    global Window,scalefactor,centered_zoom
    
    s = scalefactor**inout
    CC,UR=Window
    mid=window(point,Window)
    CC_new,UR_new=mid+s*(CC-mid),mid+s*(UR-mid)
    if centered_zoom:
        Window = [CC,UR_new]
    else:
        Window = [CC_new,UR_new]
    update_constants()
    return
    
def zoom_in(a=0):
    centered_zoom=True
    zoom_point(complex(.5,.5),1)
    centered_zoom=False
    return

def zoom_out(a=0):
    centered_zoom=True
    zoom_point(complex(.5,.5),-1)
    centered_zoom=False
    return
######
def zoom_in_LR():
    zoom_point(complex(1,0),1)
    return

def zoom_in_LL():
    zoom_point(complex(0,0),1)
    return

def zoom_in_UR():
    zoom_point(complex(1,1),1)
    return

def zoom_in_UL():
    zoom_point(complex(0,1),1)
    return

######
def switch_M():
    global Window,ZWindow, C,res,view_map_name
    
    ZWindow = Window.copy()
    
    if view_map_name =='J_log':
        update_view_map('J_log','C_log')
    else:
        update_view_map('J_lin','C_lin')
    btn_switch_M["text"] ="switch_J"
    btn_switch_M["command"] =switch_J
    res = max(4,res)
    update_window()
    return
def update_window():
    global view_map_name
    print('update_window')
    global C, stepsize, Window
    if view_map_name=='C_lin':
        print("parameter space")
        Window =[C,C+complex(4,4)*stepsize]
    Run()
def update_constants():
    global zooming
    
    global C, stepsize, Window
    if view_map_name=='C_lin':
        C = Window[0]
        stepsize = abs(Window[1]-Window[0])/(4*2**.5)
    if not zooming:
        Run()
        pass

def switch_J():
    global Window,ZWindow, C, res,view_map_name
    res = max(4,res)
    update_constants()
    
    if view_map_name=='C_log':
        update_view_map('C_log','J_log')
    else:
        update_view_map('C_lin','J_lin')
    Window = ZWindow.copy()
    btn_switch_M["text"] ="switch_M"
    btn_switch_M["command"] =switch_M
    
    Run()
    return

def switch_log():
    global Window,ZWindow, C, res,view_map_name
    res = max(4,res)
    
    if view_map_name[0]=='C':
        update_view_map('C_lin','C_log')
    else:
        update_view_map('J_lin','J_log')
    btn_switch_log["text"] ="linear"
    btn_switch_log["command"] =switch_linear
    
    Run()
    return

def switch_linear():
    global Window,ZWindow, C, res
    res = max(4,res)
    
    if view_map_name[0]=='C':
        update_view_map('C_log','C_lin')
    else:
        update_view_map('J_log','J_lin')
    btn_switch_log["text"] ="logarithmic"
    btn_switch_log["command"] =switch_log
    
    Run()
    return
view_map_name='C_lin'
def update_view_map(old,new):
    global view_map,Window,inv_view_map,view_map_name
    #choose a map. Each map should be a function from [0,1]x[0,1] to CxC (depending on Q and Window).
    view_map=view_maps[new]
    inv_view_map=inv_view_maps[new]
    windows[old]=Window.copy()
    Window=windows[new].copy()
    view_map_name=new
            

        
        
        

def change_variables():
    var_names={
        0 :'Newton',
        1 :'maxmag'
    }
    names_list=''
    for i in var_names:
        names_list = names_list+'\n'+str(i)+') '+var_names[i]
    if names_list=='':
        return
    i=simpledialog.askinteger(
                                'Change variables',
                                'Which variable would you like to change? Enter a number.\n'+names_list
                            )%(len(var_names))
    new_val=float(simpledialog.askstring(
                names_list[i],
                'Enter a new value for '+var_names[i]+':'
            ))
    if var_names[i]=='Newton':
        global Newton
        Newton=bool(new_val)
    if var_names[i]=='maxmag':
        global maxmag
        maxmag=int(new_val)
    

def on_closing():
    root.destroy()
    #if messagebox.askokcancel("Quit", "Do you want to quit?"):
#help(messagebox)
root.protocol("WM_DELETE_WINDOW", on_closing)






dot_range=[0,100,1]
def set_dots_range():
    global dot_range
    new=[None,None,None]
    new[0]=simpledialog.askinteger(
                                'Dots options',
                                'First dot number?'
                            )
    if new[0]==None:
        return
    new[1]=simpledialog.askinteger(
                                'Dots options',
                                'Upper limit?'
                            )
    if new[1]==None:
        return
    new[2]=simpledialog.askinteger(
                                'Dots options',
                                'Step size?'
                            )
    if new[2]==None:
        return
    dot_range=new
    


#btnStep = tk.Button(root,text='Step',width=12,height=1, command=step)
#btnStep.grid(row=0,column=1)
#btn

btnRun = tk.Button(root,text='Run',width=12,height=1, command=Run)
btnRun.grid(row=0,column=2)
######
btn_res_down = tk.Button(root,text='res down',width=12,height=1, command=res_down)
btn_res_down.grid(row=1,column=2)

btn_res_up = tk.Button(root,text='res up',width=12,height=1, command=res_up)
btn_res_up.grid(row=1,column=3)

######
btn_stepsize_down = tk.Button(root,text='stepsize down',width=12,height=1, command=stepsize_down)
btn_stepsize_down.grid(row=2,column=2)

btn_stepsize_up = tk.Button(root,text='stepsize up',width=12,height=1, command=stepsize_up)
btn_stepsize_up.grid(row=2,column=3)

######
btn_C_r_down = tk.Button(root,text='C_r down',width=12,height=1, command=C_r_down)
btn_C_r_down.grid(row=3,column=2)

btn_C_r_up = tk.Button(root,text='C_r up',width=12,height=1, command=C_r_up)
btn_C_r_up.grid(row=3,column=3)

######
btn_C_i_down = tk.Button(root,text='C_i down',width=12,height=1, command=C_i_down)
btn_C_i_down.grid(row=4,column=2)

btn_C_i_up = tk.Button(root,text='C_i up',width=12,height=1, command=C_i_up)
btn_C_i_up.grid(row=4,column=3)

######
btn_save_image = tk.Button(root,text='save image',width=12,height=1, command=save_image)
btn_save_image.grid(row=0,column=3)



######
btn_zoom_in = tk.Button(root,text='zoom_in',width=12,height=1, command=zoom_in)
btn_zoom_in.grid(row=5,column=2)

btn_zoom_out = tk.Button(root,text='zoom_out',width=12,height=1, command=zoom_out)
btn_zoom_out.grid(row=5,column=3)

######
btn_zoom_in_UR = tk.Button(root,text='zoom_in_UR',width=12,height=1, command=zoom_in_UR)
btn_zoom_in_UR.grid(row=6,column=3)

btn_zoom_in_UL = tk.Button(root,text='zoom_in_UL',width=12,height=1, command=zoom_in_UL)
btn_zoom_in_UL.grid(row=6,column=2)

btn_zoom_in_LR = tk.Button(root,text='zoom_in_LR',width=12,height=1, command=zoom_in_LR)
btn_zoom_in_LR.grid(row=7,column=3)

btn_zoom_in_LL = tk.Button(root,text='zoom_in_LL',width=12,height=1, command=zoom_in_LL)
btn_zoom_in_LL.grid(row=7,column=2)

######
btn_switch_M = tk.Button(root,text='switch_M',width=12,height=1, command=switch_M)
btn_switch_M.grid(row=8,column=2)


btn_switch_log = tk.Button(root,text='logarithmic',width=12,height=1, command=switch_log)
btn_switch_log.grid(row=9,column=2)

######

btn_zoom_sequence = tk.Button(root,text='zoom_sequence',width=12,height=1, command=zoom_sequence)
btn_zoom_sequence.grid(row=8,column=3)

btn_display = tk.Button(root,text='display_sequence',width=12,height=1, command=display_sequence)
btn_display.grid(row=9,column=3)

######

######

btn_dots_range = tk.Button(root,text='Dot options',width=12,height=1, command=set_dots_range)
btn_dots_range.grid(row=50,column=2)


btn_change_variables = tk.Button(root,text='change_variables',width=12,height=1, command=change_variables)
btn_change_variables.grid(row=10,column=2)

######


# In[12]:


# working out some kinks and creating the main image and trailing dots. And spot zooming.

label=tk.Label(root, image=img)
label.grid(row=0,column=1,rowspan = 120)
#canvas = tk.Canvas(root, width=500, height=400, background='gray75')
canvas = tk.Canvas(label, width=500, height=400, background='gray75')
label_id=canvas.create_image(0, 0, image=img)#photo, anchor="nw")#Label(root, image=img)
canvas.itemconfigure(label_id, image=img)
#####################################
def changetip(a,clickType):            
    """activate or deactivate whatever was clicked"""
    global tipType,dot_range
    if tipType==clickType: tipType="None"
    else: tipType=clickType
    for T in all_tips:
        for i,tip in enumerate(all_tips[T]):
            tip.place(x=rest_spots[T][0],y=rest_spots[T][1])
    
    if tipType=='circle':
        #print('circle')
        dot_range=[0,20,1]
    elif tipType=='number':
        dot_range=[0,100,1]
    #print(tipType)
    
def update_dots(n):
    """ensures that there are at least n of whichever type of trailing entities are currently active."""
    global root,all_tips
    if tipType=="circle":
        if len(all_tips['circle'])<n:
            for i in range(len(all_tips['circle']),n):
                all_tips['circle'].append(make_dot_canvas(root))
    elif tipType=='number':
        if len(all_tips['number'])<n:
            for i in range(len(all_tips['number']),n):
                all_tips['number'].append(make_dot_label(root,str(i)))

#   cx=w.winfo_pointerx() - w.winfo_rootx()
#   cy=w.winfo_pointery() - w.winfo_rooty()
def where(posn):                       
    """positions the trailing dots of whichever type are active"""
    global root,all_tips,Window,dot_range
    #print('where',dot_range)
    
    cx=posn.x_root-root.winfo_x()
    cy=posn.y_root-root.winfo_y()
    if tipType=="circle":
        update_dots(dot_range[1])
        shiftxy=[-14,-36]
        dots_list=all_tips['circle']
                
    elif tipType=='number':
        update_dots(dot_range[1])
        shiftxy=[-15,-40]
        dots_list=all_tips['number']
                
    elif tipType=='zoom_in':
        shiftxy=[-15,-40]
        dots_list=all_tips['zoom_in']
        for i,tip in enumerate(dots_list):
            #if cx>722:
            #    cy=900
            tip.place(x=cx+shiftxy[0], y=cy+shiftxy[1])
        return
                
    elif tipType=='zoom_out':
        shiftxy=[-15,-40]
        dots_list=all_tips['zoom_out']
        for i,tip in enumerate(dots_list):
            #if cx>722:
            #    cy=900
            tip.place(x=cx+shiftxy[0], y=cy+shiftxy[1])
        return
        
    else:
        return
    zi,c0=view_map(decanvasify(cx,cy),C,Window)
        
    #print(inv_view_map(zi,Window)-c0)
    
    exploded=False
    #print('where',dot_range)
    for i,tip in enumerate(dots_list):
        if i>=dot_range[1]:
            #print('too big',i)
            break
        if cx>745:
            cx,cy=dots_hide
        if i>=dot_range[0] and (i-dot_range[0])%dot_range[2]==0:
            tip.place(x=cx+shiftxy[0], y=cy+shiftxy[1])
        if exploded==False:
            try:
                zi=f(zi,c0)
                if i+1>=dot_range[0] and (i+1-dot_range[0])%dot_range[2]==0:
                    #print('ok',i)
                    cx,cy=canvasify(inv_view_map(zi,Window))
                else:
                    #print('too small or not divisible',i)
                    cx,cy=dots_hide
            except:
                exploded=True
                cx,cy=dots_hide
                continue
        else:
            continue
        

root.bind("<Motion>",where)        #track mouse movement


# Make a cursor tip using a circle on canvas
def make_dot_canvas(root,f_click=changetip):
    """create a new trailing circle"""
    tip_rad=5
    tipC=tk.Canvas(root,width=tip_rad*2,height=tip_rad*2,highlightthickness=0)#,bg="green")
    #print(tipC)
    tipL=tk.Canvas.create_oval(tipC,tip_rad/2,tip_rad/2,tip_rad/2*3,tip_rad/2*3, width=0, fill="blue")
    #help(tk.Canvas.create_oval)
    #print('l',tipL)
    tipC.bind("<1>",lambda a, clickType='circle': f_click(a,clickType))
    #print(tipC)
    return tipC
# Make a cursor tip using a label
def make_dot_label(root,n,typeName='number',f_click=changetip):
    """create a new trailing number"""
    tip_size=1
    tipL=tk.Label(root,width=tip_size, height=tip_size,text=n)#,bg="yellow")
    #print('l',tipL)
    tipL.bind("<1>",lambda a, clickType=typeName: f_click(a,clickType))
    #print('l',tipL)
    return tipL
#dot_range=[0,100,1]
#def set_dots_range():
    
dots_hide=[740,900]
rest_spots={}
rest_spots['circle']=[750,600]
rest_spots['number']=[750,650]
rest_spots['zoom_in']=[750,550]
rest_spots['zoom_out']=[800,550]
all_tips={}
all_tips['circle']=[]
all_tips['number']=[]
tipType='number'
update_dots(1)
tipType="circle" 
update_dots(1)     
tipType="None"     
    
def spot_zoom(posn,clickType):
    """if the mouse is over the image, zoom in or out centered at the mouse. Otherwise, dismiss 
    or change the object following the mouse.
    """
    #global Window,scalefactor
    
    cx=posn.x_root-root.winfo_x()
    cy=posn.y_root-root.winfo_y()
    #print(cx)
    if cx>745:
        changetip(a,clickType)
        print(tipType)
        return
    #print('this shouldn')
    if tipType=='zoom_in':
        s = 1
    elif tipType=='zoom_out':
        s = -1
    else:
        return
    
    c0=decanvasify(cx,cy)
    zoom_point(c0,s)
    return
    
    
    
                                   
all_tips['zoom_in']=[]
all_tips['zoom_in'].append(make_dot_label(root,'+',typeName='zoom_in',f_click=spot_zoom))

                                   
all_tips['zoom_out']=[]
all_tips['zoom_out'].append(make_dot_label(root,'-',typeName='zoom_out',f_click=spot_zoom))

    
changetip(0,'None')

    
    
#dotlabel=tk.Label(root, image=img)
#dotlabel.bind("<1>",changetip)
##canvas = tk.Canvas(root, width=500, height=400, background='gray75')
#canvas = tk.Canvas(dotlabel, width=500, height=400, background='gray75')
#dotlabel_id=canvas.create_oval(dotlabel,tip_rad/2,tip_rad/2,tip_rad/2*3,tip_rad/2*3, width=0, fill="blue")
##canvas.itemconfigure(dotlabel_id, image=img)

#####################################


#photo = PhotoImage(file='Alveoli.ppm')
#canvas.create_image(0, 0, image=photo, anchor="nw")
#oc = canvas.create_oval(0, 0, 400, 400, fill = 'red')


#tipC.tkraise(True)
#tipL.tkraise(True)


# In[13]:


def test_save_image(n):
    global filenumber
    t1=time.time()
    M=[[[int((i+3*j)%1500),-1] for i in range(n)] for j in range(n)]
    t2=time.time()
    print('created original matrix', 't =',round(t2-t1,3),'s')
    global img, label
    img=Render(M,img,label,pixelsize=1)

    t3=time.time()
    print('created image', 't =',round(t3-t2,3),'s')
    save(img,'test_save_image '+str(n)+' '+str(filenumber)+'.png')
    filenumber+=1

    t4=time.time()
    print('saved image', 't =',round(t4-t3,3),'s')
    print('\n\n')


def Test_function():
    for i in range(4):
        test_save_image(750*2**i)


# In[ ]:





# In[14]:


#start everything running. Wheeeeeeeeeeee!!!!!!
#print("you need to test and compare: removing the step of casting to an array")
#1/0

root.after(10,Run)
#root.after(10,Test_function)
tk.mainloop()


# In[15]:


#help(simpledialog)
#help(messagebox.askokcancel)
tk.TkVersion


# In[16]:


X=np.array([[1,2,3],[4,5,6]])
Y=np.array([[5,6,7]])
Z=np.array([[8],[9]])
print(np.append(X,Z,1))

print(maxmag)


#You can use the color maps from matplotlib and apply them without any matplotlib figures etc. 
#This will make things much faster:

# import matplotlib.pyplot as plt

# # Get the color map by name:
# cm = plt.get_cmap('gist_rainbow')

# # Apply the colormap like a function to any array:
# colored_image = cm(image)

# # Obtain a 4-channel image (R,G,B,A) in float [0, 1]
# # But we want to convert to RGB in uint8 and save it:
# Image.fromarray((colored_image[:, :, :3] * 255).astype(np.uint8)).save('test.png')

