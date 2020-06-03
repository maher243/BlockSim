from InputsConfig import InputsConfig as p

class BlockCommit:

    # Handling and running Events
    def handle_event(event):
        if event.type == "create_block":
            BlockCommit.generate_block(event)
        elif event.type == "receive_block":
            BlockCommit.receive_block(event)

    # Block Creation Event
    def generate_block (event):
        pass

    # Block Receiving Event
    def receive_block (event):
        pass

    # Select a new miner to build a new block
    def generate_next_block(node,currentTime):
        pass
    # Generate initial blocks to start the simulation with
    def generate_initial_events():
        pass
    # Propagate the genrated block to other nodes in the network
    def propagate_block (block):
        pass
    # Update local blockchain, if necessary, upon receiving a new valid block
    def update_local_blockchain(node,miner,depth):
        # the node here is the one that needs to update its blockchain, while miner here is the one who owns the last block generated
        # the node will update its blockchain to mach the miner's blockchain
        i=0
        while (i < depth):
            if (i < len(node.blockchain)):
                if (node.blockchain[i].id != miner.blockchain[i].id): # and (self.node.blockchain[i-1].id == Miner.blockchain[i].previous) and (i>=1):
                    #node.unclechain.append(node.blockchain[i]) # move block to unclechain
                    newBlock = miner.blockchain[i]
                    node.blockchain[i]= newBlock
                    if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            else:
                newBlock = miner.blockchain[i]
                node.blockchain.append(newBlock)
                if p.hasTrans and p.Ttechnique == "Full": BlockCommit.update_transactionsPool(node,newBlock)
            i+=1

    # Update local blockchain, if necessary, upon receiving a new valid block. This method is only triggered if Full technique is used
    def update_transactionsPool(node,block):
        j=0
        while j < len(block.transactions):
            for t in node.transactionsPool:
                if  block.transactions[j].id == t.id:
                    del t
                    break
            j+=1
