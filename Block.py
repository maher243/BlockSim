    # from InputsConfig import InputsConfig as p
class Block(object):
    def __init__(self, depth, id, previous, timestamp, miner, transactions, size, uncles):
        self.depth = depth # should be auto increment e.g., len(miner.blockchain)
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner # the miner who generated the block
        self.transactions = transactions or []
        self.size = size
        self.uncles = uncles or [] #[[0 for x in range(3)] for y in range(p.u)]
