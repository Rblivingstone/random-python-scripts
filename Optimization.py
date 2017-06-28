# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 09:42:53 2017

@author: rbarnes
"""
import random
import numpy as np

class Optimize:
    def __init__(self,domain,costf,maxiter=100,tol=0.001):
        self.domain=domain
        self.costf=costf
        self.maxiter=maxiter
        self.tol=tol
        return None
        
    def geneticoptimize(self,popsize=100,step=1,mutprob=0.25,elite=0.25):
        # Mutation Operation
        def mutate(vec):
            i=random.randint(0,len(self.domain)-1)
            if random.random( )<0.5 and (vec[i]>self.domain[i][0]):
                return vec[0:i]+[vec[i]-step]+vec[i+1:]
            elif random.random( )<0.5 and vec[i]<self.domain[i][1]:
                return vec[0:i]+[vec[i]+step]+vec[i+1:]
            else:
                return vec
     
                 # Crossover Operation
        def crossover(r1,r2):
            i=random.randint(1,len(self.domain)-2)
            return r1[0:i]+r2[i:]
     # Build the initial population
        pop=[]
        for i in range(popsize):
            vec=[random.uniform(self.domain[i][0],self.domain[i][1]) for i in range(len(self.domain))]
            #validate vec
            for j in range(len(self.domain)):
                #print(j,vec[j])
                if vec[j]<self.domain[j][0]:
                    vec[j]=self.domain[j][0]
                if vec[j]>self.domain[j][1]:
                    vec[j]=self.domain[j][1]
            #print(vec)
            pop.append(vec)
            #print(pop)
     
     # How many winners from each generation?
        topelite=int(elite*popsize)
     # Main loop
        for i in range(self.maxiter):
            scores=[(self.costf(v),v) for v in pop]
            scores.sort( )
            ranked=[v for (s,v) in scores]
     
            # Start with the pure winners
            pop=ranked[0:topelite]
     
            # Add mutated and bred forms of the winners
            while len(pop)<popsize:
                if random.random( )<mutprob:
                    # Mutation
                    c=random.randint(0,topelite)
                    thing2=mutate(ranked[c])
                    #print(thing2,ranked[c])
                    pop.append(thing2)
                else:
                    # Crossover
                    c1=random.randint(0,topelite)
                    c2=random.randint(0,topelite)
                    thing1=crossover(ranked[c1],ranked[c2])
                    #print(thing1)
                    pop.append(thing1)
                    
            # Print current best score
            print(scores[0][0])
            
            #Validate range on domains
            for k in range(len(pop)):
                for j in range(len(self.domain)):
                    #print(j,vec[j])
                    if pop[k][j]<self.domain[j][0]:
                        pop[k][j]=self.domain[j][0]
                    if pop[k][j]>self.domain[j][1]:
                        pop[k][j]=self.domain[j][1]
        return scores[0][1]

if __name__=='__main__':
    a=Optimize([(1.0,100.05),(1,100.3),(-100.2,100.2)],cost,maxiter=200).geneticoptimize(step=50)