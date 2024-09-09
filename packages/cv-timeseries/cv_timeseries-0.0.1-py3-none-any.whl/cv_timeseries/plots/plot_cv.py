import matplotlib.pyplot as plt

class Plot:
    def __init__(self, cv, title='', labels=[]):
        self.cv = cv
    
    def plot_cv(self, title='', labels=[]):
        plt.plot (self.cv)
        plt.title(f'{title}')
        plt.legend(labels)
        plt.tight_layout()
        plt.show()

def __init__(cv, title='', labels=[]):
    return Plot(cv).plot_cv(title,labels)