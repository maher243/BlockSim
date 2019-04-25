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


    def create_transactions():
        Transaction.pending_transactions=[]

        count=0
        id=0
        n= (p.Tn * p.Binterval)*4  # Eth 400 tx || BTC 2500
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


    ##### Select and execute a number of transactions to be added in the next block #####
    def execute_transactions():
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
