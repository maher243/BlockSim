# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 19:11:48 2019

@author: b6068199
"""
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import RandomForestRegressor
from InputsConfig import InputsConfig as p
import pandas as pd

""" A class to fit distribution to Ethereum transaction attributes, which are 
    Gas Limit, Used Gas, Gas Price as well as CPU Time
"""
class DistFit():

    cgas=None
    cprice=None
    ctime=None
    egas=None
    eprice=None
    etime=None
    x=0

    def fit():
          if DistFit.x<1:
          	df= pd.read_excel("Models/Ethereum/Distribution/Data_sets.xlsx",sheet_name="Set1")
          	df2= pd.read_excel("Models/Ethereum/Distribution/Data_sets.xlsx",sheet_name="Set2")
          	DistFit.cgas,DistFit.cprice,DistFit.ctime= DistFit.creation_fit(df) # fitted models (u:used gas, p: gas price, t: cpu time)
          	DistFit.egas,DistFit.eprice,DistFit.etime= DistFit.execution_fit(df2)
          	DistFit.x+=1


    def creation_fit(df):
            """
                Define distribution of log(used gas) as Mixure Normal distribution with K components
            """
            K=39
            g = GaussianMixture(n_components = K)

            data= np.log(df['b']).values.reshape(-1,1)
            gmm= g.fit(data)# fit model

            """
                Define random forest regression between used gas and cpu time
            """
            X = np.transpose([df['b']]) # used gas
            y = np.array(df['d']) # cpu time

            #### configure parameters for the model
            depth= 30
            estimators= 10
            clf = RandomForestRegressor(max_depth=depth, n_estimators=estimators) # RF instance
            clf.fit(X, y) #fit model

            """
                Estimate parameters of log(gas price) as normal distribution
            """
            eps= 0.001 # correction param
            K=35
            gg = GaussianMixture(n_components = K)
            data= np.log(df['c']+eps).values.reshape(-1,1)
            ggmm= gg.fit(data)# fit model

            return gmm,ggmm,clf

    def execution_fit(df):
            """
                Define distribution of log(used gas) as Mixure Normal distribution with K components
            """
            K=39
            g = GaussianMixture(n_components = K)

            data= np.log(df['b']).values.reshape(-1,1)
            gmm= g.fit(data)# fit model

            """
                Define random forest regression between used gas and cpu time
            """
            X = np.transpose([df['b']]) # used gas
            y = np.array(df['d']) # cpu time

            #### configure parameters for the model
            depth= 300
            estimators= 100
            clf = RandomForestRegressor(max_depth=depth, n_estimators=estimators) # RF instance
            clf.fit(X, y) #fit model

            """
                Estimate parameters of log(gas price) as normal distribution
            """
            eps= 0.001 # correction param
            K=65
            gg = GaussianMixture(n_components = K)
            data= np.log(df['c']+eps).values.reshape(-1,1)
            ggmm= gg.fit(data)# fit model


            return gmm,ggmm,clf

    def sample_transactions(n):

        cN= round(n * 0.0121) # rate of contract creation transactions, based on real data
        eN= round(n * 0.9879)# rate of function execution transactions, based on real data
        ##### sample contract creation transactions ########
        b_s= DistFit.cgas.sample(cN)[0]
        b_s= np.exp(b_s).flatten().round()
        b_s[b_s<21000]= 21000
        b_s[b_s>8000000]= 8000000

        b_s=b_s.reshape(-1,1)
        d_s= DistFit.ctime.predict(b_s)
        c_s= np.exp(DistFit.cprice.sample(cN)[0])
        a_s= np.random.uniform(low = b_s.flatten(), high = 8*10**6, size=cN)

        a_s=a_s.round()
        b_s=b_s.flatten().round()
        c_s=c_s.flatten()
        d_s=d_s.round()

        ##### sample function execution transactions ########
        b_e= DistFit.egas.sample(eN)[0]
        b_e= np.exp(b_e).flatten().round()
        b_e[b_e<21000]= 21000
        b_e[b_e>8000000]= 8000000

        b_e=b_e.reshape(-1,1)
        d_e= DistFit.etime.predict(b_e)
        c_e= np.exp(DistFit.eprice.sample(eN)[0])
        a_e= np.random.uniform(low = b_e.flatten(), high = 8*10**6, size=eN)

        a_e=a_e.round()
        b_e=b_e.flatten().round()
        c_e=c_e.flatten()
        d_e=d_e.round()


        ######### preparing samples #######
        gasLimit= np.concatenate((a_s,a_e),axis=None)
        usedGas= np.concatenate((b_s,b_e),axis=None)
        gasPrice= np.concatenate((c_s,c_e),axis=None)
        CPUTime= np.concatenate((d_s,d_e),axis=None)

        return gasLimit,usedGas,gasPrice,CPUTime
