#!/usr/bin/env python
# coding: utf-8



import numpy as np
from PIL import Image, ImageTk
#set up windo_w and a few constants
import tkinter as tk
from tkinter import messagebox, simpledialog,ttk
from colors import colormap_np#, set_colormap, get_color
import function_math
from function_math import set_function_Magnitude,Newton
from Mandelbrot_class2 import Mandelbrot
from view_maps2 import *

from recipies import Recipie
from windows import f_window,f_construct
from viewmaps import f_viewmap
from magnitudes import Magnitude
from colormaps import complex_array_to_rgb,np_to_img,f_expand


root = tk.Tk()


scalefactor=.6



shape=(96,96)
window=np.array([[0,0],[1,1]])
map_name="view_C_lin"
mag=Magnitude
pixelsize=8
cmap=colormap_np





R=Recipie([f_construct(shape),f_window(window),f_viewmap(map_name,0),mag,f_expand(pixelsize),cmap,np_to_img])

# set up the image and Render function

screen_img = tk.PhotoImage(width=1, height=1)
def show_img(img):
    global screen_img
    screen_img=img
    label["image"] = img



#defining the machinery that allows images and zoom sequences to be recalled and displayed. needs a lot of work.



# functions attached to buttons. 


def Run():
    img=R.apply()
    show_img(img)
    return
######

def res_down():
    global shape,pixelsize
    w,h=shape
    print('res')
    if w%2==0 and h%2==0:
        print('down')
        shape=(w//2,h//2)
        pixelsize=2*pixelsize
        R.replace_step(0,f_construct(shape))
        R.replace_step(4,f_expand(pixelsize))
def res_up():
    global shape,pixelsize
    w,h=shape
    print('res')
    if pixelsize%2==0:
        print('up')
        shape=(w*2,h*2)
        pixelsize=pixelsize//2
        R.replace_step(0,f_construct(shape))
        R.replace_step(4,f_expand(pixelsize))


def zoom_point(point,inout=1,centered=False):
    """zoom the windo_w in if inout=1, out if its -1, centered around windo_w(point)"""
    global window
    s = scalefactor**inout
    CC,UR=window
    mid=f_window(window)(point)
    CC_new,UR_new=mid+s*(CC-mid),mid+s*(UR-mid)
    if centered:
        window = [CC,UR_new]
    else:
        window = [CC_new,UR_new]
    R.replace_step(1,f_window(window))
    return Run()
    

def zoom_in(a=0):
    return zoom_point(np.array([.5,.5]),1,True)

def zoom_out(a=0):
    return zoom_point(np.array([.5,.5]),-1,True)
######
def zoom_in_LR():
    return zoom_point(np.array([1,0]),1)
    
def zoom_in_LL():
    return zoom_point(np.array([0,0]),1)
    
def zoom_in_UR():
    return zoom_point(np.array([1,1]),1)
    
def zoom_in_UL():
    return zoom_point(np.array([0,1]),1)




def change_variables():
    var_names={
        0 :'Newton',
        1 :'maxmag',
        2 :'scalefactor',
        3 :'offset',
        4 :'cyclelength'
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
        Newton=bool(new_val)
    if var_names[i]=='maxmag':
        maxmag=int(new_val)
    if var_names[i]=='scalefactor':
        global scalefactor
        scalefactor=float(new_val)
    if var_names[i]=='offset':
        offset=int(new_val)
    if var_names[i]=='cyclelength':
        cyclelength=int(new_val)


######
######

    

def on_closing():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)






btnRun = tk.Button(root,text='Run',width=12,height=1, command=Run)
btnRun.grid(row=0,column=2)
######
btn_res_down = tk.Button(root,text='res down',width=12,height=1, command=res_down)
btn_res_down.grid(row=1,column=2)

btn_res_up = tk.Button(root,text='res up',width=12,height=1, command=res_up)
btn_res_up.grid(row=1,column=3)

######

######



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

# ######
# ######

######

btn_change_variables = tk.Button(root,text='change_variables',width=12,height=1, command=change_variables)
btn_change_variables.grid(row=10,column=2)

######


# In[12]:


# working out some kinks and creating the main image and trailing dots. And spot zooming.

label=tk.Label(root, image=tk.PhotoImage(width=1, height=1))
label.grid(row=0,column=1,rowspan = 120)
#canvas = tk.Canvas(root, width=500, height=400, background='gray75')
canvas = tk.Canvas(label, width=500, height=400, background='gray75')
label_id=canvas.create_image(0, 0, image=tk.PhotoImage(width=1, height=1))#photo, anchor="nw")#Label(root, image=img)
canvas.itemconfigure(label_id, image=tk.PhotoImage(width=1, height=1))
#####################################





#####################################
    

#start everything running. Wheeeeeeeeeeee!!!!!!

root.after(10,Run)
tk.mainloop()



