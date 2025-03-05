import numpy as np
import matplotlib
from PIL import Image, ImageTk
from tkinter import messagebox, simpledialog,ttk
from tkinter.filedialog import askopenfilename
import tkinter as tk
from view_maps2 import window




class ComplexGrid:#numpy array of complex numbers, with some added functions to make it easy to turn a window into a ComplexGrid
    #and a ComplexGrid into any of the other types
    def __init__(self,Window,dimensions,data=None,windowtype="CenterCorner"):
        if data == None:

            # if windowtype=="CenterCorner":
            #     min,max=2*window[0]-window[1],window[1]
            x,y=np.linspace(1,0,dimensions[0]),np.linspace(0,1,dimensions[1])
            X,Y=np.meshgrid(x,y)
            self.data=window(Y+1j*X,Window)
        else:
            self.data=data
    def apply(self, view_map,params=None,iteration_limits=1500):
        return BiComplexGrid(view_map(self.data,params),iteration_limits)
    def to_img(self, theme='dark', rmax=None):
        '''Takes an array of complex number and converts it to an array of [r, g, b],
        where phase gives hue and saturaton/value are given by the absolute value.'''
        absmax = rmax or np.abs(self).max(self)
        Y = np.zeros(self.shape + (3,), dtype='float')
        Y[..., 0] = np.angle(self) / (2 * np.pi) % 1
        if theme == 'light':
            Y[..., 1] = np.clip(np.abs(self) / absmax, 0, 1)
            Y[..., 2] = 1
        elif theme == 'dark':
            Y[..., 1] = 1
            Y[..., 2] = np.clip(np.abs(self) / absmax, 0, 1)
        Y = matplotlib.colors.hsv_to_rgb(Y)
        return np.array(Y*255,dtype=np.uint8)#                              change this


class BiComplexGrid:#numpy array of pairs of complex numbers, with some added functions to make it easy to turn a view map and a ComplexGrid
    #into a BiComplexGrid, and turn a BiComplexGrid into any of the other types
    def __init__(self, data,iteration_limits=1500):
        self.data=data
        self.iteration_limits=iteration_limits
        self.dimensions=self.data.shape[:2]
        #self.data= np.transpose(np.array([view_map(sourcegrid,params)]),(1,2,0)))
    def evaluate(self,Magnitude,threading=True,datatype="int"):
        if threading:
            if datatype=="int":
                dtype_=int
            elif datatype=="escapedata":
                dtype_=complex
            width,height =self.dimensions
            M=np.zeros((height,width,2),dtype=dtype_)
            #print(M)
            line = np.zeros((height,2),dtype=dtype_)
            for n_x,xline in enumerate(self.data):
                for n_y,point in enumerate(xline):
                    mag=Magnitude(point[0],point[1],self.iteration_limits)
                    #print(mag)
                    line[n_y,:]=mag#,dtype=int)#np.array(
                M[:,n_x,:]=line
            data=M
            if datatype=="int":
                return IntGrid(data)
            elif datatype=="escapedata":
                return EscapeDataGrid(data)
        else:
            if datatype=="int":
                return IntGrid(Magnitude(self))
            elif datatype=="escapedata":
                return EscapeDataGrid(Magnitude(self))


class IntGrid:#numpy array of integers, with some added functions to make it easy to turn it into an image
    def __init__(self,data,load=False):
        if load:
            self.load(load)
            pass
        else:
            self.data=data
        self.res=1
        self.offset=0
        self.cyclelength=100
    def expand_pixels(self,n=1):
        self.data=self.data.repeat(n, axis = 0).repeat(n, axis = 1)
    def inflated(self,n=1):
        new=IntGrid(self.data)
        new.expand_pixels(n)
        return new
    def save(self,filename=None):
        if filename==None:
            # filename=self.get_valid_name(item=['integer array','Integer Array','.npy'])[0]
            filename=askopenfilename()
        
        # filename = filename[:-4]+' '+'.npy'
        np.save(filename,self.data)
        print(filename,'this was an integer array save')
        return(filename)
    def load(self,filename):
        self.data=np.load(filename, allow_pickle=False)

    def to_img(self,colormap_np):
        """
        Create an image from matrix. 
        """
        cmap_type='np'
        if cmap_type=='np':
            #print(self.data)
            data3=colormap_np(self.data,self.offset,self.cyclelength)
            #print(data3[::20,::20])
        return ColorGrid(data3)


class EscapeDataGrid:#numpy array of complex numbers, with some added functions to make it easy to it into an image
    pass



class ColorGrid:#this is really just an image, with some added functions to make it easy to save and such.
    def __init__(self,data,datatype="np",filename=""):
        if datatype=="np":
            self.data =  ImageTk.PhotoImage(image=Image.fromarray(data))
        elif datatype=="file":
            self.data=tk.PhotoImage(file=filename)


    def save(self,filename=None):
        """Takes data as a string of hex codes, saves it as a text file. returns the name of the file.
        the name is determined by global filenumber, which it increments, and the current value of C. 
        Reports to the console.
        """
        if filename==None:
            filename=self.get_valid_name(item=['image','Image','.png'])[0]
        
        filename = filename[:-4]+' '+'.png'
        self.data._PhotoImage__photo.write(filename)
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


