class Block(object):
    
    """ Defines the base Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0):

        self.depth = depth
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions or []
        self.size = size
