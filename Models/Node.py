from Models.Block import Block

class Node(object):

    """ Defines the base Node model.

        :param int id: the uinque id of the node
        :param list blockchain: the local blockchain (a list to store chain state locally) for the node
        :param list transactionsPool: the transactions pool. Each node has its own pool if and only if Full technique is chosen
        :param int blocks: the total number of blocks mined in the main chain
        :param int balance: the amount of cryptocurrencies a node has
    """
    def __init__(self,id):
        self.id= id
        self.blockchain= []
        self.transactionsPool= []
        self.blocks= 0#
        self.balance= 0

    # Generate the Genesis block and append it to the local blockchain for all nodes
    def generate_gensis_block():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain.append(Block())

    # Get the last block at the node's local blockchain
    def last_block(self):
        return self.blockchain[len(self.blockchain)-1]

    # Get the length of the blockchain (number of blocks)
    def blockchain_length(self):
        return len(self.blockchain)-1

    # reset the state of blockchains for all nodes in the network (before starting the next run) 
    def resetState():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain= [] # create an array for each miner to store chain state locally
            node.transactionsPool= []
            node.blocks=0 # total number of blocks mined in the main chain
            node.balance= 0 # to count all reward that a miner made
