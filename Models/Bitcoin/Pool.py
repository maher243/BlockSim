class Pool():

    def __init__(self, _id, strategy, fee_rate):
        self.id = _id
        self.strategy = strategy
        self.fee_rate = fee_rate
        self.nodes = []
        self.hashPower = 0
        self.blocks = 0
        self.block_fee = 0
        self.balance = 0

    def resetState():
        from InputsConfig import InputsConfig as p
        for pool in p.POOLS:
            pool.blocks = 0  # total number of blocks mined in the main chain
            pool.block_fee = 0  # total transaction fee recieved from mined block
            pool.balance = 0  # to count all reward that a miner made