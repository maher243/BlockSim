from Node import Node
import random

class InputsConfig(object):
    #################################################################### simulation parameters that needs to be set up #####################################################################

    ##### Blocks parameters #####
    Binterval = 12.42 #596 # Average time (in seconds)for creating a block in the blockchain
    Bsize = 7997148 #875225 the block limit in Gas/ byte
    Bdelay = 2.3#0.42 # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
    Breward = 3 # Reward for mining a block

    ##### Transactions parameters #####
    hasTrans = False  # True/False to enable/disable transactions in the simulator
    Ttechnique = "Full" # Full/Light to specify the way of modelling transactions
    Type="ETH" # style ETH or BTC
    Tn=5 # rate of the number of transactions created per second
    Tdelay = 5.1 # average transaction propagation delay in seconds (Only if Full technique is used)
    Tfee = 0.000000021 # average transaction fee per size unit
    Tsize = 546 # average transaction size  in byte
    ## note: the transaction fee (the submitter of the transaction has to pay) is Tfee * Tsize

    ##### Uncles parameters #####
    hasUncles = True # boolean variable to indicate use of uncle mechansim or not
    Buncles=2 # maximum number of uncle blocks allowed per block
    Ugenerations = 7 # the depth in which an uncle can be included in a block
    Ureward =0
    UIreward = Breward / 32 # Reward for including an uncle

    ##### Nodes parameters #####
    Nn = 16 # the total number of nodes in the network
    # the id & hash power for each node in the network -> id should be strat from 0
    NODES = []
    for i in range(Nn):
        hashPower =  random.uniform(0,30) # generate a random hash power for node i between 0% and 30%
        NODES += [Node(i,hashPower)]

    ######### if you want to configure the hash power of each node as you prefer use this instead of randomly assign hash powers to nodes ############
    # NODES = [
    # Node(0,15.2),
    #     Node(1,13.8),
    #     Node(2,13.5),
    #     Node(3,12.6),
    #     Node(4,11.3),
    #     Node(5,10.30),
    #     Node(6,9.2),
    #     Node(7,6.1),
    #     Node(8,2.5),
    #     Node(9,1.3),
    #     Node(10,1),
    #     Node(11,0.8),
    #     Node(12,0.8),
    #     Node(13,0.8),
    #     Node(14,0.6),
    #     Node(15,2),
    # ]

    ##### Simulation parameters ####
    simTime= 1000 # the simulation length (in seconds)
    Runs=5# Number of simulation runs

    ########################################################### The distribution for transactions' attributes in the Ethereum network (gathered from real Ethereum)  ###########################################################################################
    def random_Gaslimit():
        global glimit
        rand = random.uniform(0,1)
        if rand <= 0.15:
            glimit = 21000
        elif rand <= 0.32:
            glimit = random.randint(21001,50000)
        elif rand <= 0.71:
            glimit = random.randint(50001,100000)
        elif rand <= 0.93:
            glimit = random.randint(100001,250000)
        elif rand <= 0.98:
            glimit = random.randint(250001,1000000)
        elif rand <= 1:
            glimit = random.randint(1000001,7919992)
        return glimit

    def random_Usedgas():
        global ugas
        rand = random.uniform(0,1)
        if rand <= 0.14:
            ugas = random.uniform(0.0,0.25)
        elif rand <= 0.38:
            ugas = random.uniform(0.26,0.50)
        elif rand <= 0.65:
            ugas = random.uniform(0.51,0.75)
        elif rand <= 1:
            ugas = random.uniform(0.76,1)
        return ugas

    def random_GasPrice():
        global gprice
        rand = random.uniform(0,1)
        if rand <= 0.13:
            gprice = random.uniform(0.000000000,0.000000004)
        elif rand <= 0.46:
            gprice = random.uniform(0.000000005,0.00000001)
        elif rand <= 0.72:
            gprice = random.uniform(0.000000011,0.00000002)
        elif rand <= 0.89:
            gprice = random.uniform(0.000000021,0.00000004)
        elif rand <= 1:
            gprice = random.uniform(0.000000041,0.000000134)
        return gprice
