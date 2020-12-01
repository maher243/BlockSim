from Models.Transaction import Transaction as BaseTransaction
from Models.AppendableBlock.Network import Network
from InputsConfig import InputsConfig as p
import random
import numpy as np
import operator

#######################################################################################
#
# This class inherits the Transaction class and is used to create transaction
# objects as required by  the AppendableBlock model.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################


class Transaction(BaseTransaction):
    def __init__(self, previous=-1):
        super().__init__()

        # Previous transaction used to chain transaction
        self.previous = previous

#######################################################################################
#
# This class is used to generate the transactions for all the devices in the network
# as required by the AppendableBlock model. Each transaction is first created and then
# it is propogated to the device's gateway.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################


class FullTransaction():

    def create_transactions():
        # Generate Tn transaction from each device
        for i in range(p.Tn):
            # Each device generates a transaction per second to be sent to its gateway
            for j in range(p.Gn * p.Dn):
                tx = Transaction()
                tx.id = random.randrange(100000000000)
                creation_time = random.uniform(i, i + 1)
                receive_time = creation_time
                insert_time = receive_time
                tx.timestamp = [creation_time, receive_time, insert_time]
                nodeIndex = p.Gn + j
                sender = p.NODES[nodeIndex]
                tx.sender = sender.id
                tx.to = sender.gatewayIds
                FullTransaction.propagate_transaction(tx)

    # Propogate transaction to its gateway
    def propagate_transaction(tx):
        index = p.GATEWAYIDS.index(tx.to)
        tx.timestamp[1] = tx.timestamp[1] + Network.tx_prop_delay()
        p.NODES[index].transactionsPool.append(tx)
