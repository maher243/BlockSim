from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c
from Models.Incentives import Incentives as BaseIncentives
from Statistics import Statistics


class Incentives(BaseIncentives):

    """
	 Defines the rewarded elements (block + transactions), calculate and distribute the rewards among the participating nodes
    """

    def uncle_rewards(bc):
         for uncle in bc.uncles:
                for k in p.NODES:
                       if uncle.miner == k.id:
                             Statistics.totalUncles +=1
                             uncle_height = uncle.depth # uncle depth
                             block_height = bc.depth# block depth
                             k.uncles+=1
                             k.balance += ((uncle_height - block_height + 8) * p.Breward / 8) # Reward for mining an uncle block

    ''' rewards for the miner who included in the incle block in his block '''
    def uncle_inclusion_rewards(bc):
         Ru=0 # uncle reward is set to 0
         for uncle in bc.uncles:
            Ru += p.UIreward
         return Ru

    def distribute_rewards():
        for bc in c.global_chain:
            for m in p.NODES:
                if bc.miner == m.id:
                    m.blocks +=1
                    m.balance += p.Breward # increase the miner balance by the block reward
                    tx_fee= Incentives.transactions_fee(bc)
                    m.balance += tx_fee # add transaction fees to balance
                    m.balance += Incentives.uncle_inclusion_rewards(bc) # add uncle inclusion rewards to balance
            Incentives.uncle_rewards(bc) # add uncle generation rewards for the miner who build the uncle block
