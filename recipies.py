


class Recipie:
    def __init__(self,steps=[],data=[]):
        self.steps=steps
        self.n=len(self.steps)
        if self.n+1==len(data):
            self.data=data
        else:
            self.data=[None]*(self.n+1)
    
    def copy(self):
        return Recipie(self.steps,self.data)
    
    def clear_range(self, start_index=0,stop_index=None):
        if stop_index==None:
            stop_index=self.n+1
        for i in range(start_index,stop_index):
            self.data[i]=None

    def replace_step(self,index,step):
        self.steps[index]=step
        self.clear_range(index+1)
    
    def apply(self,start_index=0,stop_index=None,forget=False,return_result=True):
        if stop_index==None:
            stop_index=self.n
        for i in range(start_index,stop_index):
            self.data[i+1]=self.steps[i](self.data[i])
        if forget:
            self.clear_range(0,self.n)
        if return_result:
            return self.data[stop_index]
