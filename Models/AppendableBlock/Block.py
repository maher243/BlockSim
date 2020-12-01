#######################################################################################
#
# This class inherits the Block class and is used to create Block objects as required
# by the AppendableBlock model.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################

from Models.Block import Block as BaseBlock


class Block(BaseBlock):

    def __init__(self,
                 depth=0,
                 id=0,
                 previous=-1,
                 timestamp=0,
                 miner=None,
                 transactions=[],
                 size=1.0,
                 nodeId=0,
                 gatewayIds="x",
                 receiverGatewayId="x"):

        super().__init__(depth, id, previous, timestamp, miner, transactions, size)
        self.nodeId = nodeId
        self.gatewayIds = gatewayIds
        self.receiverGatewayId = receiverGatewayId
