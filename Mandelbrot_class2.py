


from function_math import C


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
    from function_math import set_function_Magnitude,Newton, complex_log,exp
    from view_maps2 import *
    from data_objects import ComplexGrid,BiComplexGrid,IntGrid,EscapeDataGrid,ColorGrid
except:
    print("imports failed")
    raise

class Mandelbrot:
    def __init__(self):
        self.res = 16
        self.ROW = 720
        self.COL = 720

    
        

        if Newton:
            self.Magnitude=set_function_Magnitude('J only')## use with newton and some other stuff
        else:
            self.Magnitude=set_function_Magnitude()#'test_fill'


        self.C=-1.7492336681389355 + 0.0001653419260706073j
        d=2.4147167332422493e-07+2.4147167332422493e-07j
        self.Window = [(self.C), (self.C+d)]
        self.stepsize = (self.Window[1]-self.Window[0]).real/4
        self.ZWindow = [complex(0,0),d]
        self.scalefactor = .6


    
        self.view_maps={}
        self.view_maps['C_lin']=view_C_lin
        self.view_maps['J_lin']=view_J_lin
        self.view_maps['C_log']=view_C_log_2
        self.view_maps['J_log']=view_J_log_2

        self.inv_view_maps={}
        self.inv_view_maps['C_lin']=inv_view_C_lin
        self.inv_view_maps['J_lin']=inv_view_J_lin
        self.inv_view_maps['C_log']=inv_view_C_log_2
        self.inv_view_maps['J_log']=inv_view_J_log_2

        self.windows={}
        self.windows['C_lin']=self.Window.copy()
        self.windows['J_lin']= [complex(0,0),complex(1.3,1.3)]#
        self.windows['C_log']=[complex(-math.pi,math.pi),complex(-math.pi,math.pi)+complex(1,1)*2*math.pi]
        self.windows['J_log']=[complex(-math.pi,math.pi),complex(-math.pi,math.pi)+complex(1,1)*2*math.pi]
        

        self.view_map_name='C_lin'
        self.view_map=self.view_maps[self.view_map_name]
        self.inv_view_map=self.inv_view_maps[self.view_map_name]


        
        self.maxmag = 1500
        self.C=C
        self.set_Q()
        self.res_to_shape()
        self.set_view_domain()
        self.pixelsize=None
        self.colormap_np=colormap_np
        self.scalefactor=.6
        self.zooming=False
        
        self.sequence = []
                    

        self.filenumber = 0
        self.centered_zoom=False
        
        self.offset=0
        self.cyclelength=100


    def Render(self):
        """
        Create an image from matrix. """
        if self.pixelsize==None:
            self.pixelsize=self.res
            
        drawable=self.Data.inflated(self.pixelsize)
        self.img = drawable.to_img(self.colormap_np)
        print('did')


    #functions for creating images of regions of the complex plane

    def view_C_lin(self,point,Q,Window):
        C = window(point,Window)
        return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#
    def inv_view_C_lin(self,C,Window):
        point = unwindow(C,Window)
        return point#Attractor(complex(0,0),C,[C]+centers[1:])#

    # def view_C_log(point,Q,Window):
    #     lnScale=math.log(abs(Window[1]-Window[0]))-0.3465735902799727
    #     lnC = window(point,[complex(lnScale-math.pi,math.pi),complex(lnScale,2*math.pi)])
    #     C=Window[0]+math.exp(lnC.real)*complex(math.cos(lnC.imag),math.sin(lnC.imag))
    #     return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#

    def view_J_lin(self,point,Q,Window):
        C = window(point,Window)
        if point.imag>.8 and point.real>.8 and False:
            return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
        else:
            return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#
    def inv_view_J_lin(self,C,Window):
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

    def view_C_log_2(self,point,Q,Window):
        lnC = window(point,Window)
        C=self.windows['C_lin'][0]+exp(lnC)
        return [complex(0,0),C]#Attractor(complex(0,0),C,[C]+centers[1:])#
    def inv_view_C_log_2(self,C,Window):
        lnC = complex_log(C-self.windows['C_lin'][0])
        point=unwindow(lnC,Window)
        return point#Attractor(complex(0,0),C,[C]+centers[1:])#

    def view_J_log_2(self,point,Q,Window):
        lnC = window(point,Window)
        C=self.windows['J_lin'][0]+exp(lnC)
        #print(windows['J_lin'])
        if False:#point.imag>.8 and point.real>.8:##################################              legend
            return([complex(0,0),window(5*point-complex(4,4), [Q,Q+stepsize*complex(2,2)])])
        else:
            return([C,Q])#Attractor(C,Q,[Q]+centers[1:])#
    def inv_view_J_log_2(self,C,Window):
        lnC = complex_log(C-self.windows['J_lin'][0])
        point=unwindow(lnC,Window)
        return point#Attractor(complex(0,0),C,[C]+centers[1:])#








    def res_to_shape(self):
        self.shape=(math.ceil(self.COL/self.res),math.ceil(self.ROW/self.res))
        self.pixelsize=None
    def set_view_domain(self):
        """creates a list of lists of Z,C, maxmag triples. Global Windo_w controls the region shown. 
        shape controls the number of rows and columns, Q is either a Z or C value depending on view_map. 
        """
        self.set_Q()
        self.view_domain=ComplexGrid(self.Window,self.shape).apply(self.view_map,self.Q,iteration_limits=1500)
        



    def fill(self):
        """gets the output of Magnitude at each point in view_domain, returns these as matrix."""
        self.Data=self.view_domain.evaluate(self.Magnitude)

            
    def prepare_frames(self):
        """creates a list of viewpoints, which can be rendered as a zoom sequence."""


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

        self.zooming = True
        self.frames=[]
        minres = 8###############
        lastres = self.res*2
        while self.res != lastres and self.res>minres:
            lastres = self.res
            self.res_up()
        
        zoomtype='move'#'zoom'#
        if zoomtype=='zoom':
            self.scalefactor = .65#.9#####################
            minscale = .2#2.0134609968696852e-07###############
            try:
                self.C+complex(0)
            except:
                self.C=complex(0)
            while abs(self.Window[1]-self.Window[0])>(minscale/2**.5):
                self.set_view_domain()
                self.frames.append(self.view_domain)
                self.zoom_in()
                
                
        else:
            for C_i in domain:
                self.C=C_i
                self.set_Q()
                self.set_view_domain()
                self.frames.append(self.view_domain)

    def set_Q(self):
        if self.view_map_name[-3:]=="log":
            self.Q=[self.windows["J_lin"][0],self.C]
        else:
            self.Q=self.C
    def save(self,key_name):
        """Takes data as a string of hex codes, saves it as a text file. returns the name of the file.
        the name is determined by global filenumber, which it increments, and the current value of C. 
        Reports to the console.
        """
        
        print('filenumber:',self.filenumber)
        filename = key_name[:-4]+' '+str(self.filenumber)+'.png'
        self.filenumber+=1
        return(self.img.save(filename))

    def int_save(self,key_name):
        """Takes data as a string of hex codes, saves it as a text file. returns the name of the file.
        the name is determined by global filenumber, which it increments, and the current value of C. 
        Reports to the console.
        """
        
        print('filenumber:',self.filenumber)
        filename = key_name[:-4]+' '+str(self.filenumber)+'.npy'
        self.filenumber+=1
        return(self.Data.save(filename))
    def int_load(self,filename):
        return self.Data.load(filename)
    
    def get_filename(self,datatype=['thing','']):
        keepgoing=True
        hasfailed=0
        print(datatype)
        while keepgoing:
            try:
                i=simpledialog.askstring(
                                    'Load '+datatype[0],
                                    "Sorry, that's not a valid filename. "*hasfailed+'Which '+datatype[0]+' would you like to load? Enter a string'
                                )
                if i=="escape":
                    pass
                elif i[-4:]==datatype[1]:
                    print('entered if 1')
                    pass
                    # test = open(i,'r')
                    # test.close()
                else:
                    print('entered if 2')
                    1/0
                print('here')
                keepgoing=False
            except:
                hasfailed=1
            print(keepgoing)

        return(i)
    def get_valid_name(self,item=['sequence','Sequence','.txt']):
        """gets a filename that is not an empty string or the same as another file. 
        Returns None if the user clicks cancel."""
        
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
        return sequence_key,sequence_names

    def zoom_sequence(self):
        """creates a zoom sequence as a series of saved png files, with an index file that has their names. 
        uses current global information to create the regions. Very slow for long or high resolution sequences.
        """
        
        if not messagebox.askokcancel("Zoom Sequence", "Generating a zoom sequence may take a very long time. Do you want to continue?"):
            return
        sequence_key,sequence_names=self.get_valid_name()
        if sequence_key==None: return
        sequence_names.append(sequence_key)
            
            
        self.zooming = True
        self.prepare_frames()
        namelist = []
        for view in self.frames:
            self.view_domain=view
            self.fill()
            self.Render()
            filename=self.save(sequence_key)
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
        self.zooming = False
        print('zoom sequence ready')





    def res_up(self):
        if self.res%2==0:
            self.res = self.res//2
        self.res_to_shape()

    def res_down(self):
        if self.COL%(2*self.res)==0 and self.ROW%(2*self.res) == 0:
            self.res = self.res*2
        self.res_to_shape()
    ######
    def stepsize_down(self):
        self.stepsize = self.stepsize/2
        return self.update_window()

    def stepsize_up(self):
        self.stepsize = self.stepsize*2
        return self.update_window()
    ######
    def C_r_down(self):
        self.C-=self.stepsize
        return self.update_window()
        

    def C_r_up(self):
        self.C+=self.stepsize
        return self.update_window()
        
    ######
    def C_i_down(self):
        self.C-=complex(0,self.stepsize)
        return self.update_window()
        

    def C_i_up(self):
        self.C+=complex(0,self.stepsize)
        return self.update_window()
        

    
    def get_size_res(self):
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


    def save_image(self):
        filename=self.get_valid_name(item=['image','Image','.png'])[0]
        res_size=self.get_size_res()
        if res_size=='current':
            self.save(filename)
        else:
            self.set_Q()
            self.shape=(math.ceil((res_size[1])/res_size[0]),math.ceil(res_size[1]/res_size[0]))
            self.set_view_domain()
            self.fill()
            self.pixelsize=res_size[0]
            self.Render()
            self.pixelsize=None
            self.save(filename)
    def save_intarray(self):
        filename=self.get_valid_name(item=['integer array','Integer Array','.npy'])[0]
        self.int_save(filename)
    def load_intarray(self):
        filename=self.get_filename(datatype=['Integer Array','.npy'])
        self.int_load(filename)


            

    def zoom_point(self,point,inout=1):
        """zoom the windo_w in if inout=1, out if its -1, centered around windo_w(point)"""
        
        s = self.scalefactor**inout
        CC,UR=self.Window
        mid=window(point,self.Window)
        CC_new,UR_new=mid+s*(CC-mid),mid+s*(UR-mid)
        if self.centered_zoom:
            self.Window = [CC,UR_new]
        else:
            self.Window = [CC_new,UR_new]
        return self.update_constants()
        
    def zoom_in(self,a=0):
        self.centered_zoom=True
        r=self.zoom_point(complex(.5,.5),1)
        self.centered_zoom=False
        return r

    def zoom_out(self,a=0):
        self.centered_zoom=True
        r=self.zoom_point(complex(.5,.5),-1)
        self.centered_zoom=False
        return r
    ######
    def zoom_in_LR(self):
        return self.zoom_point(complex(1,0),1)
        

    def zoom_in_LL(self):
        return self.zoom_point(complex(0,0),1)
        

    def zoom_in_UR(self):
        return self.zoom_point(complex(1,1),1)
        

    def zoom_in_UL(self):
        return self.zoom_point(complex(0,1),1)
        

    
    def update_window(self):
        if self.view_map_name=='C_lin':
            print("parameter space")
            self.Window =[self.C,self.C+complex(4,4)*self.stepsize]
        return('Run()')
    def update_constants(self):
        if self.view_map_name=='C_lin':
            self.C = self.Window[0]
            self.stepsize = abs(self.Window[1]-self.Window[0])/(4*2**.5)
        if not self.zooming:
            return('Run()')

    

        
    def switch_M(self):

        self.ZWindow = self.Window.copy()
        
        if self.view_map_name =='J_log':
            self.update_view_map('J_log','C_log')
        else:
            self.update_view_map('J_lin','C_lin')
        
        print('btn_switch_M["text"] ="switch_J"')
        print('btn_switch_M["command"] =switch_J')
        self.res = max(4,self.res)
        return self.update_window()
        
    def switch_J(self):
        self.res = max(4,self.res)
        self.zooming,q=True,self.zooming
        self.update_constants()
        self.zooming=q
        
        if self.view_map_name=='C_log':
            self.update_view_map('C_log','J_log')
        else:
            self.update_view_map('C_lin','J_lin')
        self.Window = self.ZWindow.copy()
        #r='btn_switch_M["text"] ="switch_M"'+'\n'+'btn_switch_M["command"] =switch_M'+'\n'+'Run()'
        return

    def switch_log(self):
        self.res = max(4,self.res)
        
        if self.view_map_name[0]=='C':
            self.update_view_map('C_lin','C_log')
        else:
            self.update_view_map('J_lin','J_log')
        #print('btn_switch_log["text"] ="linear"')
        #print('btn_switch_log["command"] =switch_linear')
        
        #print('Run()')
        return

    def switch_linear(self):
        self.res = max(4,self.res)
        
        if self.view_map_name[0]=='C':
            self.update_view_map('C_log','C_lin')
        else:
            self.update_view_map('J_log','J_lin')
        #print('btn_switch_log["text"] ="logarithmic"')
        #print('btn_switch_log["command"] =switch_log')
        
        #print('Run()')
        return
    def update_view_map(self,old,new):
        #choose a map. Each map should be a function from [0,1]x[0,1] to CxC (depending on Q and Windo+w).
        self.view_map=self.view_maps[new]
        self.inv_view_map=self.inv_view_maps[new]
        self.windows[old]=self.Window.copy()
        self.Window=self.windows[new].copy()
        self.view_map_name=new
        self.set_Q()

        
    def change_variables(self):
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
            self.Newton=bool(new_val)
        if var_names[i]=='maxmag':
            self.maxmag=int(new_val)
        if var_names[i]=='scalefactor':
            self.scalefactor=float(new_val)
        if var_names[i]=='offset':
            self.offset=int(new_val)
            self.Data.offset=self.offset
        if var_names[i]=='cyclelength':
            self.cyclelength=int(new_val)
            self.Data.cyclelength=self.cyclelength
            
        

        
        
        
