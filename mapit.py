from __future__ import print_function

from time import time

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import svm, metrics
import pandas

# if basemap is available, we'll use it.
# otherwise, we'll improvise later...
try:
    from mpl_toolkits.basemap import Basemap
    basemap = True
except ImportError:
    basemap = False



df=pandas.read_csv('h:/desktop/geo_mobile.csv')




def generate_data(somedf):
    x=np.linspace(-130,-57,100)
    y=np.linspace(20,50,100)
    xv,yv=np.meshgrid(x,y)
    xa=np.ravel(xv)
    ya=np.ravel(yv)
    data=pandas.DataFrame([xa,ya]).T
    data.columns=['lng','lat']
    result=data
    return result

def plot_distribution(alpha=0.25):
    
    # Plot map of United States
    plt.subplot(1, 1, 1)
    if basemap:
        print(" - plot coastlines using basemap")
        m = Basemap(projection='cyl', llcrnrlat=20,
                    urcrnrlat=50, llcrnrlon=-130,
                    urcrnrlon=-57, resolution='c')
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
    
    plt.scatter(df['lng'],df['lat'],alpha=alpha)
    plt.show()

    
    
def fit_distribution(df,df2,exclude_ut=True):
    df=df.dropna()
    X_train,X_test,y_train,y_test = train_test_split(df[['accountprimenamestate','lng','lat']],df['depvar'],test_size=.33)
    model=svm.OneClassSVM(nu=0.01,kernel='rbf',gamma=1)

    
    if exclude_ut:
        model.fit(np.array(df[df['accountprimenamestate']!='UT'][['lng','lat']]))
    else:
        model.fit(np.array(df[['lng','lat']]))

        

    plt.subplot(1, 1, 1)
    if basemap:
        print(" - plot coastlines using basemap")
        m = Basemap(projection='cyl', llcrnrlat=20,
                    urcrnrlat=50, llcrnrlon=-130,
                    urcrnrlon=-57, resolution='c')
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()

    x=np.linspace(-130,-57,100)
    y=np.linspace(20,50,100)
    xv,yv=np.meshgrid(x,y)
    Z=model.decision_function(np.c_[xv.ravel(),yv.ravel()])
    Z = Z.reshape(xv.shape)

    a=plt.contour(xv, yv, Z, levels=[0], linewidths=2, colors='red')
    plt.contourf(xv, yv, Z, levels=[0, Z.max()], colors='orange')
    
    plt.show()


df2=generate_data(df)
fit_distribution(df,df2)
plot_distribution()
