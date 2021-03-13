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
                    m.blocks += 1

                if not m.pool:
                    if bc.miner == m.id:
                        m.balance += p.Breward  # increase the miner balance by the block reward
                        m.fee += bc.fee
                        m.balance += bc.fee  # add transaction fees to balance

                elif m.pool.strategy == 'PPS':

                    reward = m.hashPower/100 * p.Breward

                    m.balance += (100-m.pool.fee)/100 * reward
                    m.pool.balance += m.pool.fee/100 * reward

                    if bc.miner == m.id:
                        m.pool.balance += bc.fee

                elif m.pool.strategy == 'FPPS':

                    if bc.miner == m.id:
                        reward = p.Breward
                        m.pool.balance += m.pool.fee/100 * reward
                        reward = (100 - m.pool.fee)/100 * reward

                        for node in m.pool.nodes:
                            node_fee = node.hashPower/m.pool.hashPower * bc.fee
                            node.fee += node_fee
                            node.balance += node.hashPower/m.pool.hashPower * reward
                            node.balance += node_fee

                elif m.pool.strategy == 'PPS+':
                    reward = m.hashPower/100 * p.Breward

                    m.balance += (100-m.pool.fee)/100 * reward
                    m.pool.balance += m.pool.fee/100 * reward

                    if bc.miner == m.id:
                        for node in m.pool.nodes:
                            node.fee += node.hashPower/m.pool.hashPower * bc.fee
