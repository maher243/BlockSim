#######################################################################################
#
# This class is responsible for generating and handling various events relating to
# blocks and transaction as required for the AppendableBlock model.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################

from Event import Event, Queue
from Models.BlockCommit import BlockCommit as BaseBlockCommit
from Scheduler import Scheduler
from InputsConfig import InputsConfig as p
from Models.AppendableBlock.Node import Node
from Models.AppendableBlock.Statistics import Statistics
from Models.AppendableBlock.Transaction import FullTransaction as FT
from Models.AppendableBlock.Transaction import Transaction as Transaction
from Models.AppendableBlock.Network import Network
import random
import copy


class BlockCommit(BaseBlockCommit):

    # Handles all the event types
    def handle_event(event):
        if event.type == "create_block":
            BlockCommit.handle_create_block(event)
        elif event.type == "append_tx_list":
            BlockCommit.handle_append_tx_list(event)
        elif event.type == "receive_tx_list":
            BlockCommit.handle_receive_tx_list(event)

     # Generates and appends a block to specified gateway's chain
    def handle_create_block(event):
        Statistics.total_blocks += 1
        index = p.GATEWAYIDS.index(event.block.receiverGatewayId)
        node = p.NODES[index]
        event.block.previous = node.last_block().id
        node.blockchain.append(event.block)

    # Append specified transcation to specified block ledger
    def append_tx(tx, block_ledger):
        tx_count = len(block_ledger)
        if tx_count > 0:
            tx.previous = block_ledger[tx_count-1].id
        block_ledger.append(tx)

    # Appends a transaction list to the speicfied gateway's block ledger
    def handle_append_tx_list(event):
        index = p.GATEWAYIDS.index(event.node)
        gateway_node = p.NODES[index]
        tx_insertion_delay = random.expovariate(1/p.insertTxDelay)
        tx_insertion_delay_increment = tx_insertion_delay
        tx_count = 1
        for tx in event.block.transactions:
            t = copy.deepcopy(tx)
            t.timestamp[2] = event.block.timestamp + \
                tx_insertion_delay_increment
            BlockCommit.append_tx(t,
                                  gateway_node.blockchain[tx.sender + p.Gn].transactions)

            tx_count += 1
            tx_insertion_delay_increment += tx_count * \
                (tx_insertion_delay/p.txListSize)

    # Receives and appends a transaction list to the speicfied gateway's block ledger
    def handle_receive_tx_list(event):
        index = p.GATEWAYIDS.index(event.node)
        gateway_node = p.NODES[index]
        gateway_prop_delay = Network.tx_list_prop_delay()
        tx_insertion_delay = random.expovariate(1/p.insertTxDelay)
        tx_insertion_delay_increment = tx_insertion_delay
        tx_count = 1
        for tx in event.block.transactions:
            t = copy.deepcopy(tx)
            t.timestamp[2] = event.block.timestamp + \
                gateway_prop_delay + tx_insertion_delay_increment

            BlockCommit.append_tx(
                t, gateway_node.blockchain[tx.sender + p.Gn].transactions)

            tx_count += 1
            tx_insertion_delay_increment += tx_count * \
                (tx_insertion_delay/p.txListSize)

    # Shedules a "receive transcation list" event for the specified gateways
    def schedule_event_prop_tx_list(tx_list, gatewayIds, tx_token_time):
        for gateway_id in gatewayIds:
            listTime = 0
            Scheduler.receive_tx_list_event(
                tx_list, gateway_id, tx_token_time, listTime)

    # Generates and schedule the initial simulation events
    def generate_initial_events():
        for gateway_id in p.GATEWAYIDS:
            for node in p.NODES:
                Scheduler.create_block_event_AB(node, 0, gateway_id)

    # Checks if all the transactions are processed
    def transcations_procesed():
        processed = True
        for gateway_node in p.NODES[0:p.Gn]:
            if len(gateway_node.transactionsPool) > 0:
                processed = False
                break

        return processed

    # Processes all the transcation events in the queue
    def process_queue():
        while not Queue.isEmpty():
            next_event = Queue.get_next_event()
            BlockCommit.handle_event(next_event)
            Queue.remove_event(next_event)

    # Processes all the gateway transaction pools
    def process_gateway_transaction_pools():
        tx_token_time = 0.0

        # Loop processing all the transaction in the system
        while not BlockCommit.transcations_procesed():

            tx_list_inserted = False

            # Randomly allocate transcation token to a gateway
            gateway_node = random.choice(p.NODES[0:p.Gn])

            # Sort the transaction by receive time in ascending order
            gateway_node.transactionsPool.sort(key=lambda tx: tx.timestamp[1])
            tx_pool_size = len(gateway_node.transactionsPool)
            tx_list = []

            # Any transcations in the pool
            if tx_pool_size > 0:
                tx_count = min(p.txListSize, tx_pool_size)

                # Append any valid transaction to the transaction list
                for tx in gateway_node.transactionsPool[0:tx_count]:
                    if tx.timestamp[1] <= tx_token_time:
                        tx_list.append(tx)

                # If there are transactions in the list schedule append and propagation events
                if len(tx_list) > 0:
                    Scheduler.append_tx_list_event(
                        tx_list, gateway_node.id, tx_token_time, 0)
                    BlockCommit.schedule_event_prop_tx_list(
                        tx_list, gateway_node.gatewayIds, tx_token_time)

                    # Remove transactions from local transaction pool
                    for tx in tx_list:
                        gateway_node.transactionsPool.remove(tx)

                    if p.maxTxListSize < len(tx_list):
                        p.maxTxListSize = len(tx_list)
                    tx_list_inserted = True

            # Release the transaction token
            if tx_list_inserted:
                tx_token_time = tx_token_time + Network.tx_list_prop_delay() + \
                    Network.tx_token_release_delay()
            else:
                tx_token_time = tx_token_time + Network.tx_token_release_delay()

        # Process all the transaction events in the queue
        BlockCommit.process_queue()
