class Pool():

    def __init__(self, _id, strategy, fee):
        self.id = _id
        self.strategy = strategy
        self.blocks= 0#
        self.fee = fee
        self.nodes = []
        self.hashPower = 0
        self.balance = 0
