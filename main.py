#!/usr/bin/env python
# coding: utf-8



# To do:
#
# gradual resolution update
# 
# efficient motion without zooming, 
# 
# show the escape time at the location of the mouse
# 
# rendering status bar
# 
# save animations and images as image files, &/| with data (C,windo_w, view map, f, maybe other stuff. Represent as string?)
# 
# cancel button in case you accidentally start rendering something ridiculously large
# 
# Constants user control (maxmag, etc), sliders (res, etc), show on screen(C, windo_w, etc).
# 
# user can change function to be iterated and how to see attractors
# 
# user can change colormaps
# 
# replace console interaction with status updates in the windo_w
# 
# maybe warning before rendering highest resolution stuff? 
# 
# support for higher precision complex numbers? 
# 
# see image/preimage of shapes under function, or n iterations (e.g. a cow)
# 



try:
    import random
    import math,time
    import numpy as np
    from PIL import Image, ImageTk
    #set up windo_w and a few constants
    import tkinter as tk
    from tkinter import messagebox, simpledialog,ttk
    from colors import colormap_np#, set_colormap, get_color
    import function_math
    from function_math import set_function_Magnitude,Newton
    from camera import Camera
    from view_maps import *
except:
    print("imports failed")
    raise

root = tk.Tk()

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

George=Camera()

# set up the image and Render function

screen_img = tk.PhotoImage(width=1, height=1)
starting=True
def show_img(img):
    global screen_img
    screen_img=img
    label["image"] = screen_img



#defining the machinery that allows images and zoom sequences to be recalled and displayed. needs a lot of work.


display_num = 0
sequence_data = []
go = False

sequence_key = 'sequence_1.txt'
def display_next():
    global go
    if go:
        Step()
        root.after(200,display_next)
    else:
        print('stop1')

def get_sequence():
    global sequence_key, sequence_data
    names_list=''
    
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
    sequence = [line.strip() for line in sequence]
    key.close()
    return(sequence)
def display_sequence():
    global sequence_data, go
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
    go = True
    display_next()
    btn_display["text"] ="Stop"
    btn_display["command"] =Stop

def Step_back():
    global display_num, sequence_data
    display_num = (display_num-1)%len(sequence_data)
    img = sequence_data[display_num]
    show_img(img)
def Step():
    global display_num, sequence_data
    display_num = (display_num+1)%len(sequence_data)
    img = sequence_data[display_num]
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
    global George
    George.Q=George.C
    George.res_to_shape()
    George.set_view_domain()
    George.fill()
    George.Render()
    show_img(George.img)
    print('C:',str(George.C.real),'+',str(George.C.imag)+'j')
    print('stepsize:',George.stepsize)
    print('res:',George.res)
    print()
    return
######

######

def res_down():
    global George
    George.res_down()
def res_up():
    global George
    George.res_up()


def stepsize_down():
    global George
    r=George.stepsize_down()
    if r=='Run()':
        Run()
def stepsize_up():
    global George
    r=George.stepsize_up()
    if r=='Run()':
        Run()


def C_r_down():
    global George
    r=George.C_r_down()
    if r=='Run()':
        Run()
def C_r_up():
    global George
    r=George.C_r_up()
    if r=='Run()':
        Run()
def C_i_down():
    global George
    r=George.C_i_down()
    if r=='Run()':
        Run()
def C_i_up():
    global George
    r=George.C_i_up()
    if r=='Run()':
        Run()


def save_image():
    global George
    George.save_image()


def zoom_in():
    global George
    r=George.zoom_in()
    if r=='Run()':
        Run()
def zoom_out():
    global George
    r=George.zoom_out()
    if r=='Run()':
        Run()

def zoom_in_UR():
    global George
    r=George.zoom_in_UR()
    if r=='Run()':
        Run()
def zoom_in_UL():
    global George
    r=George.zoom_in_UL()
    if r=='Run()':
        Run()
def zoom_in_LR():
    global George
    r=George.zoom_in_LR()
    if r=='Run()':
        Run()
def zoom_in_LL():
    global George
    r=George.zoom_in_LL()
    if r=='Run()':
        Run()




def zoom_sequence():
    global George
    George.zoom_sequence()


def set_dots_range():
    global George
    George.set_dots_range()
def change_variables():
    global George
    George.change_variables()


######
######

    

def on_closing():
    root.destroy()
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

# ######
# btn_switch_M = tk.Button(root,text='switch_J',width=12,height=1, command=switch_J)
# btn_switch_M.grid(row=8,column=2)


# btn_switch_log = tk.Button(root,text='logarithmic',width=12,height=1, command=switch_log)
# btn_switch_log.grid(row=9,column=2)

# ######

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

label=tk.Label(root, image=George.img)
label.grid(row=0,column=1,rowspan = 120)
#canvas = tk.Canvas(root, width=500, height=400, background='gray75')
canvas = tk.Canvas(label, width=500, height=400, background='gray75')
label_id=canvas.create_image(0, 0, image=George.img)#photo, anchor="nw")#Label(root, image=img)
canvas.itemconfigure(label_id, image=George.img)
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

def where(posn):                       
    """positions the trailing dots of whichever type are active"""
    global root,all_tips,George,dot_range
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
    zi,c0=George.fractal.view_map(decanvasify(cx,cy),George.C,George.Window)
    print(zi)
    
    exploded=False
    #print('where',dot_range)
    for i,tip in enumerate(dots_list):
        if i>=dot_range[1]:
            #print('too big',i)
            tip.place(x=dots_hide[0]+shiftxy[0], y=dots_hide[1]+shiftxy[1])
        if cx>745:
            cx,cy=dots_hide
        if True or i>=dot_range[0] and (i-dot_range[0])%dot_range[2]==0:
            tip.place(x=cx+shiftxy[0], y=cy+shiftxy[1])
        if exploded==False:
            try:
                zi=function_math.f(zi,c0)
                if i+1>=dot_range[0] and (i+1-dot_range[0])%dot_range[2]==0:
                    #print('ok',i)
                    cx,cy=canvasify(George.fractal.inv_view_map(zi,George.Window))
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
    tipC=tk.Canvas(root,width=tip_rad*2,height=tip_rad*2,highlightthickness=0)
    tipL=tk.Canvas.create_oval(tipC,tip_rad/2,tip_rad/2,tip_rad/2*3,tip_rad/2*3, width=0, fill="blue")
    tipC.bind("<1>",lambda a, clickType='circle': f_click(a,clickType))
    return tipC
# Make a cursor tip using a label
def make_dot_label(root,n,typeName='number',f_click=changetip):
    """create a new trailing number"""
    tip_size=1
    tipL=tk.Label(root,width=tip_size, height=tip_size,text=n)
    tipL.bind("<1>",lambda a, clickType=typeName: f_click(a,clickType))
    return tipL
    
dots_hide=[740,900]
rest_spots={}
rest_spots['circle']=[George.COL+30,600]
rest_spots['number']=[George.COL+30,650]
rest_spots['zoom_in']=[George.COL+30,550]
rest_spots['zoom_out']=[George.COL+80,550]
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
    global George
    a=0
    cx=posn.x_root-root.winfo_x()
    cy=posn.y_root-root.winfo_y()
    if cx>745:
        changetip(a,clickType)
        print(tipType)
        return
    if tipType=='zoom_in':
        s = 1
        trick=1
    elif tipType=='zoom_out':
        s = -1
        trick=1#/(1-.6)
    else:
        return
    
    c0=decanvasify(cx,cy)
    c0=(c0-.5-.5j)*trick+.5+.5j
    George.zoom_point(c0,s)
    Run()
    return
    
    
    
                                   
all_tips['zoom_in']=[]
all_tips['zoom_in'].append(make_dot_label(root,'+',typeName='zoom_in',f_click=spot_zoom))

                                   
all_tips['zoom_out']=[]
all_tips['zoom_out'].append(make_dot_label(root,'-',typeName='zoom_out',f_click=spot_zoom))

    
changetip(0,'None')

    
    

#start everything running. Wheeeeeeeeeeee!!!!!!

root.after(10,Run)
tk.mainloop()



