from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c

class Incentives:

    """
	 Defines the rewarded elements (block + transactions), calculate and distribute the rewards among the participating nodes
    """
    def distribute_rewards():
        for bc in c.global_chain:
            for m in p.NODES:
                if bc.miner == m.id:
                    m.blocks +=1
                    m.balance += p.Breward # increase the miner balance by the block reward
                    tx_fee= Incentives.transactions_fee(bc)
                    m.balance += tx_fee # add transaction fees to balance


    def transactions_fee(bc):
        fee=0
        for tx in  bc.transactions:
            fee += tx.fee
        return fee
