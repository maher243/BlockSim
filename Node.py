from Block import Block
#import time

class Node(object):
    def __init__(self,id, hashPower):
        '''Initialize a new miner named name with hashrate measured in hashes per second.'''
        self.id= id
        self.hashPower = hashPower
        self.blockchain= [] # create an array for each miner to store chain state locally
        self.transactionsPool= []
        self.unclechain = []
        self.blocks=0 # total number of blocks mined in the main chain
        self.uncles=0 # total number of uncle blocks included in the main chain
        self.balance= 0 # to count all reward that a miner made

    def generate_gensis_block():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain.append(Block(0,0,-1,0,None,[],0,[]))

    def add_uncles(miner):
        from InputsConfig import InputsConfig as p
        maxUncles = p.Buncles
        uncles=[]

        j=0
        while j < len (miner.unclechain):
            uncleDepth = miner.unclechain[j].depth
            blockDepth = miner.last_block().depth
            if maxUncles>0 and uncleDepth > blockDepth - p.Ugenerations : # to check if uncle block is received and there is space to include it, also check within 6 generation
                uncles.append(miner.unclechain[j])
                del miner.unclechain[j] # delete uncle after inclusion
                j-=1
                maxUncles-=1 # decrease allowable uncles by 1
            j+=1

        return uncles

    def update_local_blockchain(node,miner,depth):
        # the node here is the one that needs to update its blockchain, while miner here is the one who owns the last block generated
        # the node will update its blockchain to mach the miner's blockchain
        from InputsConfig import InputsConfig as p
        i=0
        while (i < depth):
            if (i < len(node.blockchain)):
                if (node.blockchain[i].id != miner.blockchain[i].id): # and (self.node.blockchain[i-1].id == Miner.blockchain[i].previous) and (i>=1):
                    node.unclechain.append(node.blockchain[i]) # move block to unclechain
                    newBlock = miner.blockchain[i]
                    node.blockchain[i]= newBlock
                    if p.hasTrans and p.Ttechnique == "Full": Node.update_transactionsPool(node,newBlock)
            else:
                newBlock = miner.blockchain[i]
                node.blockchain.append(newBlock)
                if p.hasTrans and p.Ttechnique == "Full": Node.update_transactionsPool(node,newBlock)
            i+=1

    def update_unclechain(node):
        ### remove all duplicates uncles in the miner's unclechain
        a = set()
        x=0
        while x < len(node.unclechain):
            if node.unclechain[x].id in a:
                del node.unclechain[x]
                x-=1
            else:
                a.add(node.unclechain[x].id)
            x+=1

        j=0
        while j < len (node.unclechain):
            for k in node.blockchain:
                if node.unclechain[j].id == k.id:
                    del node.unclechain[j] # delete uncle after inclusion
                    j-=1
                    break
            j+=1

        j=0
        while j < len (node.unclechain):
            c="t"
            for k in node.blockchain:
                u=0
                while u < len(k.uncles):
                    if node.unclechain[j].id == k.uncles[u].id:
                        del node.unclechain[j] # delete uncle after inclusion
                        j-=1
                        c="f"
                        break
                    u+=1
                if c=="f":
                    break
            j+=1


    def update_transactionsPool(node,block):
        j=0
        while j < len(block.transactions):
            for t in node.transactionsPool:
                if  block.transactions[j].id == t.id:
                    del t
                    break
            j+=1

    def last_block(self):
        return self.blockchain[len(self.blockchain)-1]
        
    def blockchain_length(self):
        return len(self.blockchain)-1

    ########################################################### reset the state of blockchains for all nodes in the network (before starting the next run) ###########################################################################################
    def resetState():
        from InputsConfig import InputsConfig as p
        for node in p.NODES:
            node.blockchain= [] # create an array for each miner to store chain state locally
            node.transactionsPool= []
            node.unclechain = []
            node.blocks=0 # total number of blocks mined in the main chain
            node.uncles=0 # total number of uncle blocks included in the main chain
            node.balance= 0 # to count all reward that a miner made
