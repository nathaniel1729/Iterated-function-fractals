


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
    from function_math import set_function_Magnitude,Newton, complex_log
    from view_maps import *
except:
    print("imports failed")
    raise

class Mandelbrot:
    def __init__(self):
        self.res = 16
        self.ROW = 720
        self.COL = 720

    
        self.img = tk.PhotoImage(width=self.COL, height=self.ROW)
        

        if Newton:
            self.Magnitude=set_function_Magnitude('J only')## use with newton and some other stuff
        else:
            self.Magnitude=set_function_Magnitude()#'test_fill'

        self.xm,self.Xm,self.ym,self.Ym=-364,364,-363,363

        self.C=-.884112847821245 + 1.007559240005834352j
        self.Window = [(self.C), (self.C+1+1j)]
        self.stepsize = (self.Window[1]-self.Window[0]).real/4
        self.ZWindow = [complex(0,0),complex(1.3,1.3)]
        self.scalefactor = .6


    
        self.view_maps={}
        self.view_maps['C_lin']=self.view_C_lin
        self.view_maps['J_lin']=self.view_J_lin
        self.view_maps['C_log']=self.view_C_log_2
        self.view_maps['J_log']=self.view_J_log_2

        self.inv_view_maps={}
        self.inv_view_maps['C_lin']=self.inv_view_C_lin
        self.inv_view_maps['J_lin']=self.inv_view_J_lin
        self.inv_view_maps['C_log']=self.inv_view_C_log_2
        self.inv_view_maps['J_log']=self.inv_view_J_log_2

        self.windows={}
        self.windows['C_lin']=self.Window.copy()
        self.windows['J_lin']= [complex(0,0),complex(1.3,1.3)]#
        self.windows['C_log']=[complex(-math.pi,math.pi),complex(-math.pi,math.pi)+complex(1,1)*2*math.pi]
        self.windows['J_log']=[complex(-math.pi,math.pi),complex(-math.pi,math.pi)+complex(1,1)*2*math.pi]
        

        self.view_map_name='C_lin'
        self.view_map=self.view_maps[self.view_map_name]
        self.inv_view_map=self.inv_view_maps[self.view_map_name]


        
        self.maxmag = 1500
        self.Q=C
        self.res_to_shape()
        self.set_view_domain()
        self.pixelsize=None
        self.colormap_np=colormap_np
        self.scalefactor=.6
        self.zooming=False
        
        self.sequence = []
                    

        self.filenumber = 0
        self.centered_zoom=False
        
        


    def Render(self):
        """
        Create an image from matrix. If savedata is True, it will save the image to a file and return the file name. 
        If draw is true, it will put the image on the canvas.
        """
        if self.pixelsize==None:
            self.pixelsize=self.res
        cmap_type='np'
        if cmap_type=='np':    
            M = self.Data.repeat(self.pixelsize, axis = 0).repeat(self.pixelsize, axis = 1)
            data3=self.colormap_np(M)
        
        img314 =  ImageTk.PhotoImage(image=Image.fromarray(data3))
        self.img = img314


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
        self.shape=(math.ceil((int(self.Xm)-int(self.xm))/self.res),math.ceil((int(self.Ym)-int(self.ym))/self.res))
        self.pixelsize=None
    def set_view_domain(self):
        """creates a list of lists of Z,C, maxmag triples. Global Windo_w controls the region shown. 
        shape controls the number of rows and columns, Q is either a Z or C value depending on view_map. 
        """
        
        view_domain2=np.zeros(self.shape+(2,),dtype=complex)
        iteration_limits=np.zeros(self.shape,dtype=int)
        iteration_limits[:,:]=self.maxmag
        line2=np.zeros((self.shape[1],2),dtype=complex)
        for x in range(self.shape[0]):
            for y in range(self.shape[1]):
                point = complex(x/self.shape[0],1-y/self.shape[1])
                item=self.view_map(point,self.Q,self.Window)
                line2[y,:]=item
            view_domain2[x,:,:]=line2
        self.view_domain=(view_domain2,iteration_limits)

        
    def fill(self):
        """gets the output of Magnitude at each point in view_domain, returns these as matrix."""
        view_domain, iteration_limits=self.view_domain
        width,height =view_domain.shape[:2]
        M=np.zeros((height,width,2),dtype=int)
        line = np.zeros((height,2),dtype=int)
        for n_x,xline in enumerate(view_domain):
            for n_y,point in enumerate(xline):
                mag=self.Magnitude(point[0],point[1],iteration_limits[n_x,n_y])
                #print(mag)
                line[n_y,:]=mag#,dtype=int)#np.array(
            M[:,n_x,:]=line
        self.Data=M

            
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
                self.Q=C_i
                self.set_view_domain()
                self.frames.append(self.view_domain)

    
    def save(self,key_name):
        """Takes data as a string of hex codes, saves it as a text file. returns the name of the file.
        the name is determined by global filenumber, which it increments, and the current value of C. 
        Reports to the console.
        """
        
        
        print('filenumber:',self.filenumber)
        filename = key_name[:-4]+' '+str(self.filenumber)+'.png'
        self.filenumber+=1
        self.img._PhotoImage__photo.write(filename)
        
        print(filename,'this was a save')
        return(filename)

    
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

    def res_down(self):
        if self.COL%(2*self.res)==0 and self.ROW%(2*self.res) == 0:
            self.res = self.res*2
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
            self.Q=self.C
            self.shape=(math.ceil((res_size[1])/res_size[0]),math.ceil(res_size[1]/res_size[0]))
            self.set_view_domain()
            self.fill()
            self.pixelsize=res_size[0]
            self.Render()
            self.pixelsize=None
            self.save(filename)


            

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

        
    def change_variables(self):
        var_names={
            0 :'Newton',
            1 :'maxmag',
            2 :'scalefactor'
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
        

        
        
        
