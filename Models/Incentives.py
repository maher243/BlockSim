import random
from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c


class Incentives:

    """
    Defines the rewarded elements (block + transactions), calculate and distribute the rewards among the participating nodes
    """
    def distribute_rewards():

        total_transactions = 0

        for i, bc in enumerate(c.global_chain[1:]):

            current_time = bc.timestamp

            miner = p.NODES[bc.miner]
            miner.blocks += 1

            if miner.pool:
                miner_pool = miner.pool
                miner_pool.blocks += 1
                miner.blocks_list[-1] += 1
                # pool gets block reward
                miner_pool.balance += p.Breward


            windows = {}
            cumulative_times = {}
            # calculating sum of shares for PPLNS and PPS+ pools since the block window, or the join time
            for pool in p.POOLS:
                if pool.strategy not in ['PPLNS', 'PPS+']:
                    continue

                N = pool.block_window
                if i > N:
                    window_timestamp = c.global_chain[i-N-1].timestamp
                else:
                    window_timestamp = 0

                shares = 0
                for pool_node in pool.nodes:
                    latest_window_time = max(pool_node.join_time, window_timestamp)
                    shares += (current_time - latest_window_time) * pool_node.hashPower

                windows[pool] = window_timestamp
                cumulative_times[pool] = shares


            for m in p.NODES:

                if not m.pool:
                    if miner == m:
                        m.balance += p.Breward  # increase the miner balance by the block reward
                        m.fee += bc.fee
                        m.balance += bc.fee  # add transaction fees to balance


                elif m.pool.strategy == 'PPS':

                    reward = m.hashPower/100 * p.Breward
                    # constant payout after deducting pool fee
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    m.pool.balance -= reward
                    m.balance += reward

                    if miner == m:
                        # pool keeps transaction fee
                        miner_pool.block_fee += bc.fee
                        miner_pool.balance += bc.fee


                elif m.pool.strategy == 'FPPS':

                    reward = m.hashPower/100 * p.Breward
                    # constant payout after deducting pool fee
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    m.pool.balance -= reward
                    m.balance += reward

                    # expected transaction fee also paid out at each block
                    fee = m.hashPower/100 * bc.fee
                    m.pool.balance -= fee
                    m.fee += fee
                    m.balance += fee

                    if miner == m:
                        # pool gets transaction fee in case block found
                        miner_pool.block_fee += bc.fee
                        miner_pool.balance += bc.fee


                elif m.pool.strategy == 'PPLNS':

                    # payout only occurs in case pool finds the block
                    if miner == m:
                        # reward to be distributed after deducting pool fee
                        reward = (100 - miner_pool.fee_rate)/100 * p.Breward
                        miner_pool.balance -= reward

                        # print('check')
                        for node in miner_pool.nodes:

                            latest_window_time = max(node.join_time, windows[miner_pool])
                            frac = (current_time - latest_window_time) * node.hashPower/cumulative_times[miner_pool]
                            # print(frac)
                            # transaction fee and reward distributed as per fraction of time and hashpower spent
                            node.balance += frac * reward
                            node.fee += frac * bc.fee
                            node.balance += frac * bc.fee


                # elif m.pool.strategy == 'Proportional':

                #     if bc.miner == m.id:
                #         m.blocks += 1
                #         m.pool.blocks += 1
                #         # deducting pool fee
                #         reward = (100 - m.pool.fee_rate)/100 * p.Breward
                #         m.pool.balance += m.pool.fee_rate/100 * p.Breward

                #         # all nodes share block reward and transaction fee
                #         for node in m.pool.nodes:
                #             node.balance += node.hashPower/m.pool.hash_power * reward
                #             node_fee = node.hashPower/m.pool.hash_power * bc.fee
                #             node.fee += node_fee
                #             node.balance += node_fee


                elif m.pool.strategy == 'PPS+':

                    reward = m.hashPower/100 * p.Breward
                    # constant payout after deducting pool fee (PPS)
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    m.pool.balance -= reward
                    m.balance += reward

                    if miner == m:

                        # print('check2')
                        for node in miner_pool.nodes:

                            latest_window_time = max(node.join_time, windows[miner_pool])
                            frac = (current_time - latest_window_time) * node.hashPower/cumulative_times[miner_pool]
                            # print(frac)
                            # transaction fee shared by PPLNS method as per fraction of time and hashpower
                            node.fee += frac * bc.fee
                            node.balance += frac * bc.fee


            total_transactions += len(bc.transactions)
            S = round(total_transactions/(i+1), 2)
            print(total_transactions, S)
            avg_payout = 0
            pool_payout = {}
            for pool in p.POOLS:
                # print('pool', pool.id, [node.id for node in pool.nodes])
                if pool.nodes and pool.strategy in ['PPS', 'PPLNS']:
                    mu = ((100 - pool.fee_rate)/100) * ((p.Breward + p.Tfee * S)/len(pool.nodes)) * pool.hash_power/100
                    pool_payout[pool] = mu
                    avg_payout += mu

            if len(pool_payout) == 0:
                continue

            avg_payout /= len(pool_payout)
            # print(avg_payout)
            # print([(pool.id, pool.strategy, pay) for pool, pay in pool_payout.items()])

            # pool hopping
            for node in p.NODES:
                if node.node_type == 'selfish' and node.pool.strategy in ['PPS', 'PPLNS']:

                    mu = pool_payout[node.pool]

                    if mu < avg_payout and random.random() < (avg_payout - mu)/avg_payout:
                        print(node.id, ':', node.pool.id, end=' ')

                        node.pool.hash_power -= node.hash_power
                        node.pool.nodes.remove(node)

                        if node.node_strategy == "strategy_based":
                            strategy_pools = [pool for pool in p.POOLS if pool.strategy == node.pool.strategy and pool != node.pool]
                            choosenPool = random.randint(0, len(strategy_pools) - 1)
                            node.pool = strategy_pools[choosenPool]

                        elif node.node_strategy == "across_strategies":
                            strategy_pools = [pool for pool in p.POOLS if pool.strategy in ['PPS', 'PPLNS'] and pool != node.pool]
                            choosenPool = random.randint(0, len(strategy_pools) - 1)
                            node.pool = strategy_pools[choosenPool]

                        # c.global_chain[i-1].timestamp + 0.432 * random.expovariate(hashPower * 1/p.Binterval)  # TODO improve time assignment
                        # TODO random delay
                        node.join_time = current_time
                        node.pool.hash_power += node.hash_power
                        node.pool.nodes.append(node)
                        node.pool_list.append(node.pool.id)
                        print('--->', node.pool.id, [n.id for n in node.pool.nodes])
                        node.blocks_list.append(0)
