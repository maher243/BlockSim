from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c


class Incentives:

    """
    Defines the rewarded elements (block + transactions), calculate and distribute the rewards among the participating nodes
    """
    def distribute_rewards():
        for bc in c.global_chain:
            for m in p.NODES:

                if not m.pool:
                    if bc.miner == m.id:
                        m.blocks += 1
                        m.balance += p.Breward  # increase the miner balance by the block reward
                        m.fee += bc.fee
                        m.balance += bc.fee  # add transaction fees to balance

                elif m.pool.strategy == 'PPS':

                    reward = m.hashPower/100 * p.Breward
                    # constant payout after deducting pool fee
                    m.balance -= m.pool.fee_rate/100 * reward
                    m.pool.balance += m.pool.fee_rate/100 * reward
                    m.pool.balance -= (100 - m.pool.fee_rate)/100 * reward
                    m.balance += (100 - m.pool.fee_rate)/100 * reward

                    if bc.miner == m.id:
                        m.blocks += 1
                        m.pool.blocks += 1
                        # pool keeps block reward and transaction fee
                        m.pool.balance += p.Breward
                        m.pool.block_fee += bc.fee
                        m.pool.balance += bc.fee

                elif m.pool.strategy == 'FPPS':

                    if bc.miner == m.id:
                        m.blocks += 1
                        m.pool.blocks += 1
                        # deducting pool fee
                        reward = (100 - m.pool.fee_rate)/100 * p.Breward
                        m.pool.balance += m.pool.fee_rate/100 * p.Breward

                        # all nodes share block reward and transaction fee
                        for node in m.pool.nodes:
                            node.balance += node.hashPower/m.pool.hashPower * reward
                            node_fee = node.hashPower/m.pool.hashPower * bc.fee
                            node.fee += node_fee
                            node.balance += node_fee

                elif m.pool.strategy == 'PPS+':

                    reward = m.hashPower/100 * p.Breward

                    # constant payout after deducting pool fee
                    m.balance -= m.pool.fee_rate/100 * reward
                    m.pool.balance += m.pool.fee_rate/100 * reward
                    m.pool.balance -= (100 - m.pool.fee_rate)/100 * reward
                    m.balance += (100 - m.pool.fee_rate)/100 * reward

                    # transaction fee shared by all nodes
                    if bc.miner == m.id:
                        m.blocks += 1
                        m.pool.blocks += 1
                        # pool keeps block reward while the transaction fee is shared
                        m.pool.balance += p.Breward
                        for node in m.pool.nodes:
                            node.fee += node.hashPower/m.pool.hashPower * bc.fee
                            node.balance += node.hashPower/m.pool.hashPower * bc.fee
