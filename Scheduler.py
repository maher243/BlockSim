from InputsConfig import InputsConfig as p
import random
from Event import Event, Queue
if p.model == 2:
    from Models.Ethereum.Block import Block
elif p.model == 3:
    from Models.AppendableBlock.Block import Block as AB
    from Models.AppendableBlock.Node import Node
else:
    from Models.Block import Block


class Scheduler:

    # Schedule a block creation event for a miner and add it to the event list
    def create_block_event(miner, eventTime):
        eventType = "create_block"
        if eventTime <= p.simTime:
            # prepare attributes for the event
            block = Block()
            block.miner = miner.id
            block.depth = len(miner.blockchain)
            block.id = random.randrange(100000000000)
            block.previous = miner.last_block().id
            block.timestamp = eventTime

            event = Event(eventType, block.miner, eventTime,
                          block)  # create the event
            Queue.add_event(event)  # add the event to the queue

    # Schedule a block receiving event for a node and add it to the event list
    def receive_block_event(recipient, block, blockDelay):
        receive_block_time = block.timestamp + blockDelay
        if receive_block_time <= p.simTime:
            e = Event("receive_block", recipient.id, receive_block_time, block)
            Queue.add_event(e)

    # Schedule a block creation event for a gateway - AppendableBlock model
    def create_block_event_AB(node, eventTime, receiverGatewayId):
        eventType = "create_block"
        if eventTime <= p.simTime:
            # Populate event attributes
            block = AB()
            block.id = random.randrange(100000000000)
            block.timestamp = eventTime
            block.nodeId = node.id
            block.gatewayIds = node.gatewayIds
            block.receiverGatewayId = receiverGatewayId
            event = Event(eventType, node.id, eventTime, block)
            Queue.add_event(event)  # add the event to the queue

    # Schedule a create transaction list event for a gateway
    def append_tx_list_event(txList, gatewayId, tokenTime, eventTime):
        eventType = "append_tx_list"
        if eventTime <= p.simTime:
            block = AB()
            block.transactions = txList.copy()
            block.timestamp = tokenTime
            event = Event(eventType, gatewayId, eventTime, block)
            Queue.add_event(event)

    # Schedule a transaction list receiving event for a gateway
    def receive_tx_list_event(txList, gatewayId, tokenTime, eventTime):
        eventType = "receive_tx_list"
        if eventTime <= p.simTime:
            block = AB()
            block.transactions = txList.copy()
            block.timestamp = tokenTime
            event = Event(eventType, gatewayId, eventTime, block)
            Queue.add_event(event)
