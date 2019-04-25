from InputsConfig import InputsConfig as p
from Consensus import Consensus as c
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics
import scipy as sp
import math
import statistics
from scipy import stats
import xlsxwriter as xlsw


class Results:

    ########################################################### Global variables used to calculate and print simuation results ###########################################################################################
    totalBlocks=0
    mainBlocks= 0
    totalUncles=0
    uncleBlocks=0
    staleBlocks=0
    uncleRate=0
    staleRate=0
    blockData=[]
    blocksResults=[]
    index=0
    profits= [[0 for x in range(7)] for y in range(p.Runs * len(p.NODES))] # rows number of miners * number of runs, columns =7
    chain=[]
    transactions=[]

    def calculate():
        Results.global_chain() # print the global chain
        Results.blocks_results() # calcuate and print block statistics e.g., # of accepted blocks and stale rate etc
        Results.profit_results() # calculate and distribute the revenue or reward for miners

    ########################################################### Calculate block statistics Results ###########################################################################################
    def blocks_results():
        trans = 0

        Results.mainBlocks= len(c.global_chain)-1
        Results.staleBlocks = Results.totalBlocks - Results.mainBlocks
        for b in c.global_chain:
            Results.uncleBlocks += len(b.uncles)
            trans += len(b.transactions)
        Results.staleRate= round(Results.staleBlocks/Results.totalBlocks * 100, 2)
        Results.uncleRate= round(Results.uncleBlocks/Results.totalBlocks * 100, 2)
        Results.blockData = [ Results.totalBlocks, Results.mainBlocks,  Results.uncleBlocks, Results.uncleRate, Results.staleBlocks, Results.staleRate, trans]
        Results.blocksResults+=[Results.blockData]

    ########################################################### Calculate and distibute rewards among the miners ###########################################################################################
    def profit_results():
        for bc in c.global_chain:
            for m in p.NODES:
                if bc.miner == m.id:
                    m.blocks +=1
                    m.balance += p.Breward # increase the miner balance by the block reward
                    m.balance += Results.calculate_txFee(bc) # add transaction fees to balance

                    for uncle in bc.uncles:
                        m.balance += p.UIreward
                        for k in p.NODES:
                            if uncle.miner == k.id:
                                Results.totalUncles +=1
                                uncle_height = uncle.depth # uncle depth
                                block_height = bc.depth# block depth
                                k.uncles+=1
                                k.balance += ((uncle_height - block_height + 8) * p.Breward / 8) # Reward for mining an uncle block

        for m in p.NODES:
            i = Results.index + m.id * p.Runs
            Results.profits[i][0]= m.id
            Results.profits[i][1]= m.hashPower
            Results.profits[i][2]= m.blocks
            Results.profits[i][3]= round(m.blocks/Results.mainBlocks * 100,2)
            Results.profits[i][4]= m.uncles
            Results.profits[i][5]= round((m.blocks + m.uncles)/(Results.mainBlocks + Results.totalUncles) * 100,2)
            Results.profits[i][6]= m.balance
        Results.index+=1

    def calculate_txFee(bc):
        fee=0
        for tx in  bc.transactions:
            fee += tx.usedGas * tx.gasPrice
        return fee

    ########################################################### prepare the global chain  ###########################################################################################
    def global_chain():
        for i in c.global_chain:
            block= [i.depth, i.id, i.previous, i.timestamp, i.miner, len(i.transactions), i.size, len(i.uncles)]
            Results.chain +=[block]

    ########################################################### Print simulation results to Excel ###########################################################################################
    def print_to_excel():

        df1 = pd.DataFrame({'Block Time': [p.Binterval], 'Block Propagation Delay': [p.Bdelay], 'No. Miners': [len(p.NODES)], 'Simulation Time': [p.simTime]})
        data = {'Stale Rate': Results.staleRate,'Uncle Rate': Results.uncleRate ,'# Stale Blocks': Results.staleBlocks,'# Total Blocks': Results.totalBlocks, '# Included Blocks': Results.mainBlocks, '# Uncle Blocks': Results.uncleBlocks}

        df2= pd.DataFrame(Results.blocksResults)
        df2.columns= ['Total Blocks', 'Main Blocks', 'Uncle blocks', 'Uncle Rate', 'Stale Blocks', 'Stale Rate', '# transactions']

        df3 = pd.DataFrame(Results.profits)
        df3.columns = ['Miner ID', '% Hash Power','# Mined Blocks', '% of main blocks','# Uncle Blocks','% of uncles', 'Profit (in ETH)']

        df4 = pd.DataFrame(Results.chain)
        df4.columns= ['Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions','Block Limit', 'Uncle Blocks']

        writer = pd.ExcelWriter('t.xlsx', engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='InputConfig')
        df2.to_excel(writer, sheet_name='SimOutput')
        df3.to_excel(writer, sheet_name='Profit')
        df4.to_excel(writer,sheet_name='Chain')

        writer.save()

    ########################################################### Reset all global variables used to calculate the simulation results ###########################################################################################
    def reset():
        Results.totalBlocks=0
        Results.totalUncles=0
        Results.mainBlocks= 0
        Results.uncleBlocks=0
        Results.staleBlocks=0
        Results.uncleRate=0
        Results.staleRate=0
        Results.blockData=[]
