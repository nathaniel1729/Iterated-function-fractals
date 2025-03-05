


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
        d=(2.4147167332422493e-07+2.4147167332422493e-07j)*.6**(-20)
        self.Window = [(self.C), (self.C+d)]
        self.stepsize = (self.Window[1]-self.Window[0]).real/4
        self.ZWindow = [complex(0,0),d]
        self.scalefactor = .5


    
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

        self.switch_J()


    def Render(self):
        """
        Create an image from matrix. """
        if self.pixelsize==None:
            self.pixelsize=self.res
            
        drawable=self.Data.inflated(self.pixelsize)
        drawable.offset=self.offset
        drawable.cyclelength=self.cyclelength
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
        self.view_domain=ComplexGrid(self.Window,self.shape).apply(self.view_map,self.Q,iteration_limits=self.maxmag)
        



    def fill(self):
        """gets the output of Magnitude at each point in view_domain, returns these as matrix."""
        self.Data=self.view_domain.evaluate(self.Magnitude)

            
    def prepare_frames(self):
        """creates a list of viewpoints, which can be rendered as a zoom sequence."""


        domain=[]
        r=((-1.768898444675856 + 0.0024940515331034322j)-(-1.7688999353245756+0.0024918585249065353j))
        center=-1.7688999353245756+0.0024918585249065353j

        clip=32

        f=open("startpoint.txt","r")
        s=int(f.read().strip())
        f.close()

        startpoint=s/clip

        f=open("startpoint.txt","w")
        f.write(str(s+1))
        f.close()

        nsteps=96*64//clip
        #Anticipated: nsteps=192*32, res=1, framerate=32. sample in Art28try
        #On second thought, that's toos slow. I need to either double the framerate to 64 or half nsteps.
        #okay I tried both and I'm really not sure if it's worth doubling the time for a very marginal gain in quality. Estimated render time for the "Anticipated" above (changing the framerate to 64 for a video length of  1:36) is 40min*(2/res)**2*(nsteps/(192*4))=32*40 min= about 22hrs. (I would of course break that into about 8 3hr chunks, which might be able to run simultaneously). The truth is that doubling the render time isn't that big a deal, at least if I'm parallelizing things a bit. I have almost a week to finish this, and I have the fundamentals ready. But the other truth is that the two videos are so very similar! The higher framerate one is ever so slightly smoother to they eye for stuff further away from the center, and the high speed motion in the centerlooks a bit more like motion rather than just flashing colors.
        #There's another test I should do before deciding: does this "parallelizing" thing actually work? I'd like to try to generate a video in about 10 minutes by running 8 programs in parallel. That's about 80 minutes of rendering, so I think I'll do nsteps=192*2=96*4 and res=1, (so framerate 4). That means 8 different programs each doing 48 frames, so clip=8 and startpoint ranges from 0/8 to 7/8. I'm going to give these a slightly different set of names too.
        # two things learned from the experiment: first of all, make sure to save! I didn't save before doing the 0 render, and the result was that I had to do that one over again. The other thing I learned is that parallelizing didn't help a lot. With 7-8 things running, what I had hoped would take 10 minutes took more like 40. But that's less than 80, it looks like I can get about a 2x speedup  by parallelizing. Thus rather than put all my eggs in 1 basket by running several things at once, I think I'll break the 22hr render into 32 40 ish minute renders, and run them two at a time. Hopefully they will still get the speedup, and that's not too long a block of time, so I can incorporate rendering into my schedule (maybe do a lot of it at night too). I also wrote myself a little program that can stitch together the text files from several zoom sequences, and I checked and the one I made did in fact work.
        # oh and I'm going to change the default initial zoom so I don't have to hit zoom_out 20 times before every render. That should make things easier.

        # final render parameters:
        # clip=32
        # startpoint=i/clip for i in range(clip)
        # framerate=64
        # nsteps=96*framerate//clip
        # res=1
        #
        # Procedure: Set the values above. Save the program. set startpoint.txt to contain the number 0. Then repeat the following: open a program. look at the file startpoint.txt. generate a zoom sequence named ArtFinal0.#, where # is the number written in startpoint.txt. Do not edit startpoint.txt. Do this for each value of #, and once the #=31 sequence is rendered, rendering is complete. Next edit concatenate.py to correctly assemble these into a single file, and finally use the Mathematica notebook to combine the images into a video. By the way, each render should have 192 images.

        angles=[2*math.pi*(i/(clip*nsteps)+startpoint) for i in range(nsteps)]
        #[math.pi*(1+math.sin((i/nsteps-1/2)*math.pi)) for i in range(nsteps)]

        #Art16try
        #n=20
        # C1=[0,0.334074,0.0640362529243,-0.0466771008766,-0.176725267301,-0.000377463336095,-0.0191565850737,0.00303498596052,-0.0187679189316,0.00672696494618,-0.00581275594532,0.0000341217669139,-0.00727868427749,0.00128351108815,-0.00326159391225,0.00032110840756,-0.00212992498257,0.00043048575061,-0.00112990583922,0.000135630854355,-0.000714815429505]
        # D1=[0,0.166703401656,0.0207675065395,0.183990309862,0.0278744904357,0.00564606376345,0.0103872235551,0.00483279469491,0.000355367910967,0.00489970728526,0.00180980808703,0.0000628591006391,0.000562012724766,0.000318492000544,.0000006017453605,0.00014368085877,0.0000914939335181,0.0000027183599253,0.0000200008039865,0.0000176860763038,6.3088188351e-7]

        # #accuratized version of 16
        # #Art24try
        # n=8
        # C2=[0,0.339995, 0.0633439, -0.0449984, -0.168472, 0.00417905, -0.0145691,
        #     0.0104177, -0.0131756]
        # D2=[0,0.164516, 0.0198503, 0.188459, 0.0320132, 0.00424582, 0.0106062,
        #     0.00937527, 0.00369474]
        # E2=[0,0.000710806, 0.0062501, 0.00162841, -0.00208567, -0.00503162,
        #     -0.00161361, 0.00271667, -0.00253246]
        # F2=[0,0.000194077, -0.000768256, -0.00147351, 0.000419799, 0.00165322,
        #     -0.000363319, -0.000379527, 0.00070743]

        # Art19try
        n=20
        C2=[0,-0.299029, 0.211078, 0.00751196, 0.0539717, 0.0668618, 0.013408,
            0.0242027, 0.0452507, 0.011691, 0.00603374, -0.000077676,
            -0.00837442, 0.00131167, -0.00570328, -0.000435834, 0.00115083,
            -0.000959999, -0.000137003, 0.000937689, 0.000184511]
        D2=[0,0.00881761, 0.321533, -0.114201, -0.0155227, 0.0436392, -0.0605868,
            -0.0162078, 0.00442921, -0.00866695, -0.00610446, -0.00667129,
            -0.00258359, 0.00260661, -0.0015083, 0.00113499, 0.00113993,
            -0.00019004, 0.000759128, -0.000270971, -0.000314777]
        E2=[0,0.105169, -0.116532, -0.120879, 0.0506722, 0.029227, 0.00374618,
            -0.00288012, 0.00166136, -0.0198923, -0.00467476, -0.00692007,
            0.00408357, 0.00327326, -0.00220286, 0.00304486, 0.0000192088,
            0.000465952, -0.000564418, 0.0000271109, 0.00042513]
        F2=[0,-0.12962, -0.0624032, 0.105705, 0.0418791, -0.0139002, 0.128527,
            0.00583419, 0.00550306, -0.0199793, 0.0118674, -0.0133154,
            0.000515375, -0.00123184, -0.000247185, 0.0006522, -0.000442031,
            0.00200737, -0.000650509, 0.000426275, 0.000124592]

        # #Art21try
        # n=20
        # C2=[0,-0.259829, 0.115068, 0.093199, -0.0662191, 0.0966355, 0.023074,
        #     0.00527218, -0.00416199, 0.0419194, -0.00374968, -0.0106202,
        #     0.00311663, 0.00347379, -0.000512318, -0.00157666, -0.000244153,
        #     0.000261085, -0.000616187, 0.000191881, 0.0000431917, -2.13121e-6,
        #     -0.000277448, -0.0000345425, -0.000135594, 0.0000704651,
        #     -0.0000188011, 0.0000239689, -5.19867e-7, -4.08061e-6,
        #     8.10959e-6]
        # D2=[0,-0.20167, -0.0304288, 0.0375776, 0.0573099, -0.0744329, 0.0131507,
        #     -0.000939014, 0.01642, -0.00452767, -0.0148819, 0.00319092,
        #     0.000663267, 0.00460615, -0.00101122, -0.000075501, 0.000671329,
        #     0.000740724, -0.000744423, -0.000195608, 0.00011562, 0.0000322042,
        #     0.000119253, -0.0000434043, -0.0000203308, -0.0000133879,
        #     -4.99225e-6, 0.0000356314, -5.39916e-6, -0.0000162621,
        #     5.04001e-6]
        # E2=[-0.0792351/2,0.159238, 0.133462, -0.0195019, -0.11667, -0.0807598, -0.0133611,
        #     -0.0128461, 0.00287197, -0.0107557, -0.000941295, 0.00198429,
        #     -0.00397289, -0.00220479, 0.00169597, 0.00160323, 0.00100742,
        #     0.00016154, -0.00108037, -0.000351315, -0.0000184059, -0.0000317838,
        #     0.0000478802, -0.0000215095, -0.0000210139, 0.0000505147,
        #     0.0000257642, -1.01823e-6, -6.48998e-6,
        #     3.62293e-6, 0.0000105705]
        # F2=[ 0.269063/2,-0.0501916, -0.0848628, 0.00218291, 0.00334824, 0.0246747,
        #     0.0158047, -0.0418884, 0.00361763, 0.00153846, 0.00356055,
        #     -0.00685035, -0.00244976, -0.00561417, -0.000139588, 0.00109775,
        #     0.00131695, -0.000489625, 0.00107021, -0.000279102, -0.000105069,
        #     -0.000242772, 0.000246838, 0.0000554975,
        #     3.54743e-7, 0.000018668, 0.0000122834, 0.0000169969, 0.0000189016,
        #     9.54651e-6, -9.6256e-6]

        for a in angles:
            domain.append(center+r*2*complex(sum([C2[i]*np.sin(i*a)+E2[i]*np.cos(i*a) for i in range(n+1)]),sum([D2[i]*np.sin(i*a)+F2[i]*np.cos(i*a) for i in range(n+1)])))
            #print(domain[-1].real,domain[-1].imag)
        #for c in domain:
        #    print(c.real)

        self.zooming = True
        self.frames=[]
        minres = 1##############################
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
            
        

        
        
        
