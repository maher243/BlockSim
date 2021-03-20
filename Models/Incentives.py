import random
from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c


class Incentives:

    """
    Defines the rewarded elements (block + transactions), calculate and distribute the rewards among the participating nodes
    """
    def distribute_rewards():
        for i, bc in enumerate(c.global_chain):
            
            current_time = bc.timestamp

            cumulative_times = {}
            for pool in p.POOLS:
                if pool.strategy != 'PPLNS':
                    continue

                N = pool.block_window
                if i > N:
                    window_timestamp = c.global_chain[i-N-1].timestamp
                else:
                    window_timestamp = 0
                        
                resource = 0
                for pool_node in pool.nodes:
                    minimum_window_time = min(current_time - pool_node.joinTime, current_time - window_timestamp)
                    resource +=  minimum_window_time * pool_node.hashPower
                
                cumulative_times[pool] = resource


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
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    m.pool.balance -= reward
                    m.balance += reward

                    if bc.miner == m.id:
                        m.blocks += 1
                        m.pool.blocks += 1
                        # pool keeps block reward and transaction fee
                        m.pool.balance += p.Breward
                        m.pool.block_fee += bc.fee
                        m.pool.balance += bc.fee

                elif m.pool.strategy == 'PPLNS':
                    
                    if bc.miner == m.id:
                        m.blocks += 1
                        m.pool.blocks += 1

                        reward = (100 - m.pool.fee_rate)/100 * p.Breward
                        m.pool.balance += m.pool.fee_rate/100 * p.Breward

                        print('check')
                        for node in m.pool.nodes:
                            N = m.pool.block_window
                            if i > N:
                                window_timestamp = c.global_chain[i-N-1].timestamp
                            else:
                                window_timestamp = 0
                            
                            minimum_window_time = min(current_time - node.joinTime, current_time - window_timestamp)
                            
                            frac = (minimum_window_time * node.hashPower)/cumulative_times[m.pool]
                            print(frac)
                            node.balance += frac * reward
                            node.fee += frac * bc.fee
                            node.balance += frac * bc.fee


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
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    # constant payout after deducting pool fee
                    m.pool.balance -= reward
                    m.balance += reward

                    # transaction fee shared by all nodes
                    if bc.miner == m.id:
                        m.blocks += 1
                        m.pool.blocks += 1
                        # pool keeps block reward while the transaction fee is shared
                        m.pool.balance += p.Breward
                        for node in m.pool.nodes:
                            node.fee += node.hashPower/m.pool.hashPower * bc.fee
                            node.balance += node.hashPower/m.pool.hashPower * bc.fee



            for node in p.NODES:
                if node.node_type == 'selfish':
                    if random.random() < jump_threshold:
                        
                        node.joinTime = current_time  # TODO improve time assignment

                        if node.node_strategy == "random":
                            while True:
                                temp_pool = node.pool
                                choosePool = random.randint(0, len(p.POOLS))
                                node.pool = p.POOLS[choosePool]
                                if node.pool != temp_pool:
                                    break

                        elif node.node_strategy == "sequential":
                            pool_index = p.POOLS.index(node.pool)
                            pool_index = (pool_index + 1)%len(p.POOLS)
                            node.pool = p.POOLS[pool_index]

                        # elif node.node_strategy == 'strategy_based'