class Pool():

    def __init__(self, _id, strategy, fee_rate, block_window=None):
        # initialise pool parameters
        self.id = _id
        self.strategy = strategy  # PPS, PPLNS, PPS+, FPPS
        self.fee_rate = fee_rate
        self.nodes = []  # nodes currently minnig in the pool
        self.hash_power = 0  # % of hash power controlled by pool
        self.blocks = 0  # number of blocks mined by miners in pool
        self.block_fee = 0  # total transaction fee kept by pool
        self.balance = 0  # pool balance
        self.block_window = block_window  # block window in case of PPLNS and PPS+ pools

    def resetState():
        from InputsConfig import InputsConfig as p
        # reset pool attribures after each run
        for pool in p.POOLS:
            pool.blocks = 0  # total number of blocks mined in the main chain
            pool.block_fee = 0  # total transaction fee recieved from mined block
            pool.balance = 0  # to count all reward that a miner made
            pool.nodes = []
            pool.hash_power = 0
