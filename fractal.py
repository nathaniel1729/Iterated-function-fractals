


from function_math import C


try:
    import math
    import numpy as np
    from function_math import set_function_Magnitude,Newton, complex_log,exp
except:
    print("imports failed")
    raise

class Fractal:
    def __init__(self,view_map,inv_view_map):

        if Newton:
            self.value=set_function_Magnitude('J only')## use with newton and some other stuff
        else:
            self.value=set_function_Magnitude()#'test_fill'


        self.C=-0.2829083486891697 + -1.3532971029220109j
        self.view_map=view_map
        self.inv_view_map=inv_view_map


        
        self.maxmag = 1500
        self.Q=C






    def Magnitude(self,view_domain):
        """gets the output of Magnitude at each point in view_domain, returns these as matrix."""
        
        iteration_limits=self.maxmag
        width,height =view_domain.shape[:2]
        M=np.zeros((height,width,2),dtype=int)
        line = np.zeros((height,2),dtype=int)
        for n_x,xline in enumerate(view_domain):
            for n_y,point in enumerate(xline):
                mag=self.value(point[0],point[1],iteration_limits)
                #print(mag)
                line[n_y,:]=mag#,dtype=int)#np.array(
            M[:,n_x,:]=line
        return M


        
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

        