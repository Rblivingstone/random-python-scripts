# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:26:33 2017

@author: rbarnes
"""

import pandas as pd
import scipy.stats as stats
from scipy.optimize import minimize
import numpy as np

class common_point_of_purchase():
    def __init__(self,csv):
        self.df=pd.read_csv(csv,header=3,sep='~')
        self.df['Merchant Name 5']=[obj[:5].lower() for obj in self.df['Merchant Name']]
        self.df1=self.df[((self.df['POS Entry Mode']==5)|(self.df['POS Entry Mode']==90))&(self.df['Merchant Category Code']!=5411)&(self.df['Merchant Category Code']!=5541)&(self.df['Merchant Category Code']!=5300)&(self.df['Merchant Category Code']!=5814)&(self.df['Merchant Category Code']!=5542)&(self.df['Merchant Name']!='MOUNTAIN AMERICA CU      ')]
        self.transform_dataframe('Merchant Name 5')
        return(None)
    
    def transform_dataframe(self,var='Merchant DBA'):
        self.transformed=pd.pivot_table(self.df1,
                                   index=['Card Number'],
                                   columns=[var],
                                   aggfunc='count'
                                   ).fillna(0)['Settlement Amount (DTL)']
        return(None)
        
    def get_likelihood(self,params):
        negloglik=0
        logliks=stats.multinomial.logpmf(
                                             np.array(self.transformed),
                                             np.array(self.transformed.sum(axis=1)),
                                             params
                                             )
        negloglik=logliks.sum()
        #print(negloglik)
        return(negloglik)
        
    def maximize_likelihood(self,isweighted=True,maxiters=1000):
        #initparams = [1./self.transformed.shape[1]]*self.transformed.shape[1]
        initparams= np.array((self.transformed.sum()/self.transformed.sum().sum()))
        weighted=np.multiply(self.transformed.sum().sum()/self.transformed.sum(axis=1).reshape(-1,1),self.transformed)
        weightedinitparams=np.array((weighted.sum()/weighted.sum().sum()))
        #results = minimize(self.get_likelihood,initparams,method='SLSQP',constraints={'type':'eq','fun':self.prob_constraint},tol=0.001,options={'maxiter':maxiters,'disp':True})
        #self.results=results
        if isweighted:
            self.results=weightedinitparams
        else:
            self.results=initparams
        return(self.results)
        
        
    def prob_constraint(self,params):
        return(sum(params)-1)
        
    def print_likelihood(self,params):
        print("Log-Likelihood:  {0}".format(-self.get_likelihood(params)))
        return(None)
        
    def get_most_likely_point_of_purchase(self,n=0):
        return(self.transformed.columns.values[np.argsort(-self.results)[n]],self.results[np.argsort(-self.results)[n]])
        
    def build_dictionary(self):
        resp={}
        for i in range(len(self.results.x)):
            resp[self.transformed.columns.values[i]]=self.results.x[i]
        return(resp)
        
if __name__=='__main__':
    w=common_point_of_purchase('I:\\Fraud Analysis\\Ryan\\bukle no cams.txt')
    #v=common_point_of_purchase('I:\\Fraud Analysis\\Ryan\\bukle no cams.txt')
    #%%w.transform_dataframe('Merchant Corporate Name')
    
    results=w.maximize_likelihood(False)
    print('unweighted log-likelihood:   {0}'.format(w.get_likelihood(results)))
    print('--------------------------------')
    for i in range(10):
        print(w.get_most_likely_point_of_purchase(i))
#%%        
    results=w.maximize_likelihood()
    print('weighted log-likelihood:   {0}'.format(w.get_likelihood(results)))
    print('--------------------------------')
    #print(np.array_equal(results1,results2))
    for i in range(10):
        print(w.get_most_likely_point_of_purchase(i))
    #print(w.build_dictionary())