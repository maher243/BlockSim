import numpy as np
from InputsConfig import InputsConfig as p
from Node import Node
import random

class Consensus:
    global_chain=[] # the accpted global chain after resovling the forks


    def PoW(miner):
        ##### Start solving a fresh PoW on top of last block appended #####
        TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
        hashPower = miner.hashPower/TOTAL_HASHPOWER
        return random.expovariate(hashPower * 1/p.Binterval)

    def longest_chain():
        Consensus.global_chain = [] # reset the global chain before filling it

        a=[]
        for i in p.NODES:
            a+=[i.blockchain_length()]
        x = max(a)

        b=[]
        z=0
        for i in p.NODES:
            if i.blockchain_length() == x:
                b+=[i.id]
                z=i.id

        if len(b) > 1:
            c=[]
            for i in p.NODES:
                if i.blockchain_length() == x:
                    c+=[i.last_block().miner]
            z = np.bincount(c)
            z= np.argmax(z)

        for i in p.NODES:
            if i.blockchain_length() == x and i.last_block().miner == z:
                for bc in range(len(i.blockchain)):
                    Consensus.global_chain.append(i.blockchain[bc])
                break
