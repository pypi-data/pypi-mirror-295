import numpy as np

class VC:
    def __init__(self, time_series, t_interval=None, bin_size=50e-3):
        self.time_series = time_series
        if t_interval is None:
            self.t_interval = (0,len(time_series))
        else:
            self.t_interval = t_interval
        self.bin_size = bin_size
        self.N = time_series.unique().size

    def calculate_vc(self):
        t = self.time_series.index.values
        bins=np.arange(int(self.t_interval[0]),np.ceil(self.t_interval[-1])+self.bin_size,self.bin_size)
        count,_ = np.histogram(t,bins=bins)
        count=count/self.bin_size/self.N
        #print(count)
        #print(count.shape)
        if count.shape[0]%10!=0:
            count=count[0:-1]
        fr=count.reshape(10,int(count.shape[0]//10))
        mu=fr.mean(axis=0)
        #print(mu)
        sigma=fr.std(axis=0)
        #print(sigma)
        cv=sigma/mu

        return cv
    
def __init__(time_series, t_interval=None, bin_size=50e-3):
    vc = VC(time_series, t_interval, bin_size)
    return vc.calculate_vc()