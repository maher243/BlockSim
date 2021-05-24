from Models.Block import Block
from Models.Node import Node as BaseNode


class Node(BaseNode):
    def __init__(self, id, hashPower, pool=None, join_time=0, node_type='honest', node_strategy=None):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        super().__init__(id)  # blockchain, transactionsPool, blocks, balance
        self.hashPower = hashPower
        self.pool = pool
        self.node_type = node_type # honest or selfish
        self.node_strategy = node_strategy  # best, strategy_based, random

        # initialise attributes to track pool related information
        if self.pool:
            self.join_time = join_time
            self.original_pool = self.pool
            # the following lists are used to maintain a record of
            # multiple pools when pool hopping occurs
            self.pool_list = [pool.id]
            self.blocks_list = [0]
            self.reward_list = [0]
            self.balance_list = [0]

    def resetState():
        from InputsConfig import InputsConfig as p

        for node in p.NODES:
            node.blockchain = []  # reset array for each miner to store chain state locally
            node.transactionsPool = []  # reset transaction pool
            node.blocks = 0  # reset total number of blocks mined in the main chain
            node.fee = 0  # reset total transaction fee recieved from mined block
            node.balance = 0  # reset miner reward

            # reset all pool related information
            if node.pool:
                node.pool = node.original_pool
                node.pool_list = [node.original_pool.id]
                node.blocks_list = [0]
                node.reward_list = [0]
                node.balance_list = [0]
