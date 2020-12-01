#######################################################################################
#
# This class inherits the class Node and is used to create Node objects as required by
# the AppendableBlock model.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################
from Models.AppendableBlock.Block import Block
from Models.Node import Node as BaseNode


class Node(BaseNode):

    # Construct Node object
    def __init__(self, id, nodeType, gatewayIds):
        super().__init__(id)
        # Defines the node type - "g" for gateway and "d" for device
        self.nodeType = nodeType

        # Holds the gatway ids that this node can connect to
        self.gatewayIds = gatewayIds

        # Used by gateways to hold a local copy of the blockchain
        self.blockchain = []

        # Used by gateway nodes to hold transactions from its device nodes
        self.transactionsPool = []

    # Generates a genesis block and appends it to the local blockchain of all the gateway nodes
    def generate_gensis_block():
        from InputsConfig import InputsConfig as p
        for node in p.NODES[0:p.Gn]:
            node.blockchain.append(Block())

    # Resets the node state
    def reset_state(self):
        self.blockchain.clear()
        self.transactionsPool.clear()
