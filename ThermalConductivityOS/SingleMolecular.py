import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR

class SingleMolecular:
    
    def __init__(self,MF,Name,TCList):
        self.MF = MF
        self.Name = Name
        self.TCList = TCList
          
    def __str__(self):
        info = "{}\t{:30}\t{:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format("MF","Name","100K",
                                                                       "200K","300K","400K",
                                                                       "500K","600K")
        data  = "{}\t{:<30}\t{:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(self.MF,self.Name,
                                                                         self.TCList[0],self.TCList[1],
                                                                         self.TCList[2],self.TCList[3],
                                                                         self.TCList[4],self.TCList[5])
        return info + "\n" + data
    
    def getMF(self):
        return self.MF
    
    def setMF(self,MF):
        self.MF  = MF
    
    def getName(self):
        return self.Name
    
    def setName(self,Name):
        self.Name  = Name
              
    def getValueOfK(self,temperature):
        if temperature < 100:
            temperature = 100
        elif temperature > 600:
            temperature = 600
        tem = temperature//100
        return self.TCList[tem-1]
        
    def setValueofK(self,temperature,tcValue):
        if temperature < 100:
            temperature = 100
        elif temperature > 600:
            temperature = 600
        tem = temperature//100
        self.TCList[tem-1] = tcValue
            
    def curveFitNp(self, degree):
        x = np.array([100,200,300,400,500,600])
        y = np.copy(self.TCList)
        index = np.isfinite(y)
        
        x = x[index]
        y = y[index]       
        
        z1 = np.polyfit(x, y, degree) 
        p1 = np.poly1d(z1) 
        y_pre = p1(x)
            
        plt.xlim(50, 650)
        plt.xlabel('Temperature(K)')
        plt.ylabel('Thermal Conductivity(mW $m^1$$K^1$)')
        plt.title(self.MF+": "+self.Name)
        plt.plot(x,y,'.',label="Data")
        plt.plot(x,y_pre,label="Fitting curve")
        plt.legend()
        plt.show()
       
    def curveFitSVR(self, degree):
        X = np.array([100,200,300,400,500,600])
        X = X.reshape(6,1)
        
        y = np.copy(self.TCList).ravel()
        index = np.isfinite(y)
        X = X[index]
        y = y[index]
        
        svr_rbf = SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
        svr_lin = SVR(kernel="linear", C=100, gamma="auto")
        svr_poly = SVR(kernel="poly", C = 100, degree=degree)  
        svrs = [svr_rbf, svr_lin, svr_poly]
        kernel_label = ["RBF", "Linear", "Polynomial"]
        model_color = ["m", "c", "g"]
        
        lw = 2
        fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 6), sharey=True)
        for ix, svr in enumerate(svrs):
            axes[ix].plot(
                X,
                svr.fit(X, y).predict(X),
                color=model_color[ix],
                lw=lw,
                label="{} model".format(kernel_label[ix]),
            )
            axes[ix].scatter(
                X[svr.support_],
                y[svr.support_],
                facecolor="none",
                edgecolor=model_color[ix],
                s=50,
                label="{} support vectors".format(kernel_label[ix]),
            )
            axes[ix].scatter(
                X[np.setdiff1d(np.arange(len(X)), svr.support_)],
                y[np.setdiff1d(np.arange(len(X)), svr.support_)],
                facecolor="none",
                edgecolor="k",
                s=50,
                label="other training data",
            )
            axes[ix].legend(
                loc="upper center",
                bbox_to_anchor=(0.5, 1.1),
                ncol=1,
                fancybox=True,
                shadow=True,
            )

        fig.text(0.5, 0.04, 'Temperature(K)' , ha="center", va="center")
        fig.text(0.06, 0.5, 'Thermal Conductivity(mW $m^1$$K^1$)', ha="center", va="center", rotation="vertical")
        fig.suptitle("Support Vector Regression", fontsize=14)
        plt.show()     