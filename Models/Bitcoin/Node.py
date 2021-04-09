from Models.Block import Block
from Models.Node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, id, hashPower, pool=None, join_time=0, node_type='honest', node_strategy=None):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id, pool, join_time)  # ,blockchain,transactionsPool,blocks,balance)
        self.hashPower = hashPower
        self.node_type = node_type
        self.node_strategy = node_strategy  # random, sequential, strategy_based
        if self.pool:
            self.original_pool = self.pool
            self.pool_list = [pool.id]
            self.blocks_list = [0]
            self.reward_list = [0]
            self.balance_list = [0]

    def resetState():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain = []  # create an array for each miner to store chain state locally
            node.transactionsPool = []
            node.blocks = 0  # total number of blocks mined in the main chain
            node.fee = 0  # total transaction fee recieved from mined block
            node.balance = 0  # to count all reward that a miner made
            if node.pool:
                node.pool = node.original_pool
                node.pool_list = [node.original_pool.id]
                node.blocks_list = [0]
                node.reward_list = [0]
                node.balance_list = [0]
