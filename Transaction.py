import random
import operator
from InputsConfig import InputsConfig as p

class Transaction(object):
    pending_transactions=[]

    def __init__(self,id,timestamp, receiveTime,node,gasLimit,usedGas,gasPrice):
        self.id=id
        self.timestamp=timestamp
        self.receiveTime= receiveTime or 0
        self.node=node
        # self.size= size
        # self.price= price
        # self.fee= self.size * self.price
        ######### for Ethereum only ###########
        self.gasLimit=gasLimit ## no
        self.usedGas = usedGas ## size
        self.gasPrice=gasPrice ## fee


    ##### Craete transactions and store them in the pending_transactions array #####
    # def create_transactions():
    #
    #     if p.Ttechnique == "Full" or "full":
    #         Transaction.create_transactions_full()
    #
    #     elif p.Ttechnique == "Light" or "light":
    #         Transaction.create_transactions_light()
    #
    #     else:
    #         print("You should either seclect Full or Light technique")
    #
    #     # return Transaction.pending_transactions


    def create_transactions_light():
        Transaction.pending_transactions=[]

        count=0
        id=0
        n= 400  # Eth 400 tx || BTC 2500
        for i in range(n):
            gaslimit = p.random_Gaslimit()
            ugas = p.random_Usedgas()
            # gaslimit = random.expovariate(1/p.tx_size)
            gasprice= p.random_GasPrice()
            timestamp = count
            receiveTime= timestamp
            node = random.choice (p.NODES)
            node = node.id
            usedgas = int(ugas * gaslimit)
            if usedgas < 21000:
               usedgas = 21000
            id = id + 1
            Transaction.pending_transactions += [Transaction (id,timestamp,receiveTime,node,gaslimit,usedgas,gasprice)]

    def create_transactions_full():
        count=0
        id=0

        while count < p.simTime:
        #while count < p.Binterval:
            m=int(random.expovariate(1/p.Tn)) # random number of transactions/second (from 1 to 8)
            for i in range(m):
                gaslimit = p.random_Gaslimit()
                ugas = p.random_Usedgas()
                gasprice= p.random_GasPrice()
                timestamp = count
                receiveTime= timestamp
                node = random.choice (p.NODES)
                node = node.id
                usedgas = int(ugas * gaslimit)
                if usedgas < 21000:
                   usedgas = 21000

                id+=1

                tx = Transaction (id,timestamp,receiveTime,node,gaslimit,usedgas,gasprice)
                Transaction.transaction_prop(tx)
            count+=1

        for node in p.NODES:
            node.transactionsPool.sort(key=operator.attrgetter('gasPrice'), reverse=True)



    # Transaction propogation & preparing pending lists for miners
    def transaction_prop(tx):
        # Fill each pending list. This is for transaction propogation
        for i in p.NODES:
            if tx.node != i.id:
                rnd = random.expovariate(1/p.Tdelay)
                receiveTime = tx.receiveTime + rnd # transaction propogation delay in seconds
                i.transactionsPool.append(Transaction(tx.id,tx.timestamp,receiveTime,tx.node,tx.gasLimit,tx.usedGas,tx.gasPrice))
            else:
                i.transactionsPool.append(tx)


    ##### Select and execute a number of transactions to be added in the next block #####
    def execute_transactions_light():
        transactions= []
        blockSize = 0
        count=0
        size = p.Bsize

        Transaction.pending_transactions.sort(key=operator.attrgetter('gasPrice'), reverse=True) # sort all transactions based on the highest price "fee" offered

        while count < len(Transaction.pending_transactions):
            # if  (size >= Transaction.pending_transactions[count].gasLimit and Transaction.pending_transactions[count].timestamp <= clock):
            if  (size >= Transaction.pending_transactions[count].gasLimit): # and Transaction.pending_transactions[count].timestamp <= clock):
                size -= Transaction.pending_transactions[count].usedGas
                transactions += [Transaction.pending_transactions[count]]
                blockSize += Transaction.pending_transactions[count].usedGas
                # del Transaction.pending_transactions[count]
                # count-=1
            count+=1

        return transactions, blockSize

    def execute_transactions_full(miner,currentTime):
        transactions= []
        blockSize = 0
        count=0
        size = p.Bsize

        #miner.transactionsPool.sort(key=operator.attrgetter('gasPrice'), reverse=True)

        while count < len(miner.transactionsPool):
            if  (size >= miner.transactionsPool[count].gasLimit and miner.transactionsPool[count].receiveTime <= currentTime):
                size -= miner.transactionsPool[count].usedGas
                transactions += [miner.transactionsPool[count]]
                blockSize += miner.transactionsPool[count].usedGas
                miner.transactionsPool.remove(miner.transactionsPool[count])
                count-=1
            count+=1

        return transactions, blockSize
