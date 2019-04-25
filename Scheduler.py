
from InputsConfig import InputsConfig as p
import random
from Transaction import Transaction
from Block import Block
from Event import Event
from Queue import Queue
from Node import Node
from Consensus import Consensus as c
###################################### A class to schedule future events ########################################
class Scheduler:

    # ##### Time methods #####
    # def PoW_completion_time(hashPower):
    #     return random.expovariate(hashPower * 1/p.Binterval)
    def receive_block_time():
        return random.expovariate(1/p.Bdelay)
    # ##### Start solving a fresh PoW on top of last block appended #####
    # def solve_PoW(miner):
    #     TOTAL_HASHPOWER = sum([miner.hashPower for miner in p.NODES])
    #     hashPower = miner.hashPower/TOTAL_HASHPOWER
    #     return Scheduler.PoW_completion_time(hashPower)
    ##### Schedule initial events and add them to the event list #####
    def initial_events():
        currentTime = 0 # at the start of the simualtion, time will be zero
        for node in p.NODES:
            if node.hashPower >0: # only if hashPower >0, the node will be eligiable for mining
                Scheduler.create_block_event(node,currentTime)

    ##### Schedule a block creation event and add it to the event list #####
    def create_block_event(miner,currentTime):
        if miner.hashPower > 0:
            # blockTime = currentTime + Scheduler.solve_PoW(miner)
            blockTime = currentTime + c.PoW(miner)
            eventTime = blockTime
            eventType = "create_block"

            if eventTime <= p.simTime: ##### create the event + add it to the event list #####
                # prepare attributes for the event
                minerId= miner.id
                blockDepth = len(miner.blockchain)
                blockId= random.randrange(100000000000)
                blockPrev= miner.last_block().id

                block = Block(blockDepth,blockId,blockPrev,blockTime,minerId,[],0,[]) # event content: transctions, uncles and blockSize is not set yet -> they will be set once the event is created
                event = Event(eventType,minerId,eventTime,block) # create the event
                Queue.add_event(event) # add the event to the queue

    ##### Schedule block receiving events for all other nodes and add those events to the event list #####
    def receive_block_event(event):
        miner= event.node
        blockDepth = event.block.depth
        blockId = event.block.id
        blockTrans = event.block.transactions
        blockPrev= event.block.previous
        bockSize = event.block.size
        blockTimestamp = event.time
        blockUncles= event.block.uncles

        for recipient in p.NODES:
            if recipient.id != miner:
                receive_block_time = event.time + Scheduler.receive_block_time() # draw time for node i to receive the block
                if receive_block_time <= p.simTime:
                    block = Block(blockDepth,blockId,blockPrev,blockTimestamp,miner,blockTrans,bockSize,blockUncles)
                    e = Event("receive_block", recipient.id, receive_block_time, block)
                    Queue.add_event(e)
