from Models.Ethereum.Block import Block
from Models.Node import Node as BaseNode


#from ImportClasses import Block
class Node(BaseNode):
    def __init__(self,id,hashPower): #blockchain=[],transactionsPool=[],unclechain=[],blocks=0,balance=0,uncles=0,hashPower=0.0):

        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)#,blockchain,transactionsPool,blocks,balance)
        self.hashPower = hashPower
        self.unclechain = []
        self.uncles= 0 # total number of uncle blocks included in the main chain
        self.blockchain= []# create an array for each miner to store chain state locally
        self.transactionsPool= []
        self.blocks= 0# total number of blocks mined in the main chain
        self.balance= 0# to count all reward that a miner made, including block rewards + uncle rewards + transactions fees


    def generate_gensis_block():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain.append(Block())
            
    # This to allow miners to include uncle blocks in their main blocks
    def add_uncles(miner):
        from InputsConfig import InputsConfig as p
        maxUncles = p.Buncles
        uncles=[]

        j=0
        while j < len (miner.unclechain):
            uncleDepth = miner.unclechain[j].depth
            blockDepth = miner.last_block().depth
            if maxUncles>0 and uncleDepth > blockDepth - p.Ugenerations : # to check if uncle block is received and there is space to include it, also check within 6 generation
                uncles.append(miner.unclechain[j])
                del miner.unclechain[j] # delete uncle after inclusion
                j-=1
                maxUncles-=1 # decrease allowable uncles by 1
            j+=1

        return uncles


    ########################################################### reset the state of blockchains for all nodes in the network (before starting the next run) ###########################################################################################
    def resetState():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain= [] # create an array for each miner to store chain state locally
            node.transactionsPool= []
            node.unclechain = []
            node.blocks=0 # total number of blocks mined in the main chain
            node.uncles=0 # total number of uncle blocks included in the main chain
            node.balance= 0 # to count all reward that a miner made
