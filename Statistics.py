from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c
from Models.Incentives import Incentives
import pandas as pd


class Statistics:

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
    profits = [[] for y in range(p.Runs * len(p.NODES))]  # number of miners * number of runs
    pool_profits = []
    chain=[]

    def calculate(run_id):
        Statistics.global_chain(run_id)  # print the global chain
        Statistics.blocks_results(run_id)  # calcuate and print block statistics e.g., # of accepted blocks and stale rate etc
        Statistics.profit_results(run_id)  # calculate and distribute the revenue or reward for miners
        Statistics.pool_results(run_id)

    ########################################################### Calculate block statistics Results ###########################################################################################
    def blocks_results(run_id):
        trans = 0

        Statistics.mainBlocks= len(c.global_chain)-1
        Statistics.staleBlocks = Statistics.totalBlocks - Statistics.mainBlocks
        for b in c.global_chain:
            if p.model==2: Statistics.uncleBlocks += len(b.uncles)
            else: Statistics.uncleBlocks = 0
            trans += len(b.transactions)
        Statistics.staleRate= round(Statistics.staleBlocks/Statistics.totalBlocks * 100, 2)
        if p.model==2: Statistics.uncleRate= round(Statistics.uncleBlocks/Statistics.totalBlocks * 100, 2)
        else: Statistics.uncleRate==0
        Statistics.blockData = [run_id, Statistics.totalBlocks, Statistics.mainBlocks,  Statistics.uncleBlocks, Statistics.uncleRate, Statistics.staleBlocks, Statistics.staleRate, trans]
        Statistics.blocksResults+=[Statistics.blockData]

    ########################################################### Calculate and distibute rewards among the miners ###########################################################################################
    def profit_results(run_id):

        for m in p.NODES:
            i = run_id * len(p.NODES) + m.id
            Statistics.profits[i] = [run_id, m.id, m.node_type]
            if p.hopping:
                if m.pool:
                    Statistics.profits[i] += [m.node_strategy, m.pool_list, m.blocks_list, m.reward_list, m.balance_list]
                else:
                    Statistics.profits[i] += [m.node_strategy, None, None]
            else:
                if m.pool:
                    Statistics.profits[i] += [m.pool.id, m.pool.strategy, m.pool.fee_rate]
                else:
                    Statistics.profits[i] += [None, 'SOLO', None]
            if p.model== 0:
                Statistics.profits[i].append("NA")
            else:
                Statistics.profits[i].append(m.hashPower)
            Statistics.profits[i].append(m.blocks)
            Statistics.profits[i].append(round(m.blocks/Statistics.mainBlocks * 100, 2))
            if p.model==2:
                Statistics.profits[i].append(m.uncles)
                Statistics.profits[i].append(round((m.blocks + m.uncles)/(Statistics.mainBlocks + Statistics.totalUncles) * 100,2))
            else:
                Statistics.profits[i].append(0)
                Statistics.profits[i].append(0)
            Statistics.profits[i].append(m.fee)
            Statistics.profits[i].append(m.balance)
            Statistics.profits[i].append(m.balance * p.Bprice)


    def pool_results(run_id):
        for pool in p.POOLS:
            Statistics.pool_profits.append([run_id, pool.id, pool.strategy, pool.fee_rate, pool.block_window, pool.hash_power, pool.blocks,
            round(pool.blocks/Statistics.mainBlocks * 100, 2), pool.block_fee, pool.balance, pool.balance * p.Bprice])


    ########################################################### prepare the global chain  ###########################################################################################
    def global_chain(run_id):
        if p.model==0 or p.model==1:
                for i in c.global_chain:
                        block= [run_id, i.depth, i.id, i.previous, i.timestamp, i.miner, len(i.transactions), i.fee, i.size]
                        Statistics.chain +=[block]
        elif p.model==2:
                for i in c.global_chain:
                        block= [run_id, i.depth, i.id, i.previous, i.timestamp, i.miner, len(i.transactions), i.fee, i.usedgas, len(i.uncles)]
                        Statistics.chain +=[block]

    ########################################################### Print simulation results to Excel ###########################################################################################
    def print_to_excel(fname):

        df1 = pd.DataFrame({'Block Time': [p.Binterval], 'Block Propagation Delay': [p.Bdelay], 'No. Miners': [len(p.NODES)], 'Simulation Time': [p.simTime]})
        #data = {'Stale Rate': Results.staleRate,'Uncle Rate': Results.uncleRate ,'# Stale Blocks': Results.staleBlocks,'# Total Blocks': Results.totalBlocks, '# Included Blocks': Results.mainBlocks, '# Uncle Blocks': Results.uncleBlocks}

        df2= pd.DataFrame(Statistics.blocksResults)
        df2.columns= ['Run ID', 'Total Blocks', 'Main Blocks', 'Uncle blocks', 'Uncle Rate', 'Stale Blocks', 'Stale Rate', '# transactions']

        df3 = pd.DataFrame(Statistics.profits)
        if p.hopping:
            df3.columns = ['Run ID', 'Miner ID', 'Miner Type', 'Hopping Strategy', 'Pool IDs', 'Blocks per pool', 'Reward per pool', 'Balance per pool', '% Hash Power','# Mined Blocks', '% of main blocks', '# Uncle Blocks','% of uncles', 'Transaction Fee', 'Profit (in crypto)', 'Profit in $']
        else:
            df3.columns = ['Run ID', 'Miner ID', 'Miner Type', 'Pool Id', 'Pool Strategy', 'Pool Fee', '% Hash Power','# Mined Blocks', '% of main blocks', '# Uncle Blocks','% of uncles', 'Transaction Fee', 'Profit (in crypto)', 'Profit in $']

        df4 = pd.DataFrame(Statistics.pool_profits)
        if len(df4) > 0:
            df4.columns = ['Run ID', 'Pool ID', 'Pool Strategy', '% Fee Rate', 'Block Window', '% Hash Power', '# Mined Blocks', '% of main blocks', 'Transaction Fee', 'Profit (in crypto)', 'Profit in $']

        df5 = pd.DataFrame(Statistics.chain)
        if p.model==2:
            df5.columns= ['Run ID', 'Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions', 'Transaction Fee', 'Block Limit', 'Uncle Blocks']
        else:
            df5.columns= ['Run ID', 'Block Depth', 'Block ID', 'Previous Block', 'Block Timestamp', 'Miner ID', '# transactions', 'Transaction Fee', 'Block Size']



        writer = pd.ExcelWriter(fname, engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='InputConfig', startcol=-1)
        df2.to_excel(writer, sheet_name='SimOutput', startcol=-1)
        df3.to_excel(writer, sheet_name='Profit', startcol=-1)
        df4.to_excel(writer, sheet_name='Pools', startcol=-1)
        df5.to_excel(writer, sheet_name='Chain', startcol=-1)

        writer.save()

    ########################################################### Reset all global variables used to calculate the simulation results ###########################################################################################
    def reset():
        Statistics.totalBlocks=0
        Statistics.totalUncles=0
        Statistics.mainBlocks= 0
        Statistics.uncleBlocks=0
        Statistics.staleBlocks=0
        Statistics.uncleRate=0
        Statistics.staleRate=0
        Statistics.blockData=[]

    # def reset2():
    #     Statistics.blocksResults=[]
    #     Statistics.profits= [[] for y in range(p.Runs * len(p.NODES))] # rows number of miners * number of runs, columns =7
    #     Statistics.chain=[]
