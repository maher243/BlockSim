from Models.Block import Block
from Models.Node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, id, hashPower, pool=None):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id, pool)  # ,blockchain,transactionsPool,blocks,balance)
        self.hashPower = hashPower
        # self.blockchain= []# create an array for each miner to store chain state locally
        # self.transactionsPool= []
        # self.blocks= 0# total number of blocks mined in the main chain
        # self.fee = 0
        # self.balance= 0# to count all reward that a miner made, including block rewards + uncle rewards + transactions fee
