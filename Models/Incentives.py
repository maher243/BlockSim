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

            # save node miner object
            miner = p.NODES[bc.miner]
            # increment miner block count
            miner.blocks += 1

            # in case miner belongs to a pool, update pool attributes
            if miner.pool:
                miner_pool = miner.pool
                miner_pool.blocks += 1
                miner.blocks_list[-1] += 1
                # pool gets block reward when a block is found
                miner_pool.balance += p.Breward


            windows = {}
            cumulative_shares = {}
            # calculating sum of shares for PPLNS and PPS+ pools since block window or the join time
            for pool in p.POOLS:
                if pool.strategy not in ['PPLNS', 'PPS+']:
                    continue

                N = pool.block_window
                # extract timestamp of earliest block within window
                if i > N:
                    window_timestamp = c.global_chain[i-N-1].timestamp
                else:
                    window_timestamp = 0

                shares = 0
                for pool_node in pool.nodes:
                    # select the latest timestamp from the pool join time and block windows
                    latest_window_time = max(pool_node.join_time, window_timestamp)
                    # calculate shares contributed since the latest time
                    shares += (current_time - latest_window_time) * pool_node.hashPower

                # save window timestamp and total shares for later use
                windows[pool] = window_timestamp
                cumulative_shares[pool] = shares


            for m in p.NODES:

                # for solo miners, pay miner directly in case block found
                if not m.pool:
                    if miner == m:
                        m.balance += p.Breward  # increase the miner balance by the block reward
                        m.fee += bc.fee
                        m.balance += bc.fee  # add transaction fees to balance


                elif m.pool.strategy == 'PPS':

                    reward = m.hashPower/100 * p.Breward
                    # miners get a constant payout after deducting pool fee
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    # decrease pool balance and increase miner balance
                    m.pool.balance -= reward
                    m.balance += reward
                    m.balance_list[-1] += reward
                    m.reward_list[-1] += reward

                    if miner == m:
                        # pool keeps transaction fee
                        miner_pool.block_fee += bc.fee
                        miner_pool.balance += bc.fee


                elif m.pool.strategy == 'FPPS':

                    reward = m.hashPower/100 * p.Breward
                    # miners get a constant payout after deducting pool fee
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    # decrease pool balance and increase miner balance
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

                        for node in miner_pool.nodes:
                            # once again, calculate the latest time to be considered calculating miner shares
                            latest_window_time = max(node.join_time, windows[miner_pool])
                            # calculate miner shares as a fraction of total shares
                            frac = (current_time - latest_window_time) * node.hashPower/cumulative_shares[miner_pool]
                            # transaction fee and reward distributed as per fraction of time and hashpower spent
                            node.balance += frac * reward
                            node.fee += frac * bc.fee
                            node.balance += frac * bc.fee

                            node.reward_list[-1] + frac * reward
                            node.balance_list[-1] += frac * (bc.fee + reward)


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
                    # miner gets a constant payout of block reward after deducting pool fee (PPS)
                    reward = (100 - m.pool.fee_rate)/100 * reward
                    m.pool.balance -= reward
                    m.balance += reward

                    if miner == m:

                        for node in miner_pool.nodes:
                            # calculate the latest time to be considered calculating miner shares
                            latest_window_time = max(node.join_time, windows[miner_pool])
                            # calculate miner shares as a fraction of total shares
                            frac = (current_time - latest_window_time) * node.hashPower/cumulative_shares[miner_pool]
                            # transaction fee shared by PPLNS method as per fraction of time and hashpower
                            node.fee += frac * bc.fee
                            node.balance += frac * bc.fee


            # increment total transactions and calculate average transactions per block, S
            total_transactions += len(bc.transactions)
            S = round(total_transactions/(i+1), 2)

            avg_payout = 0
            pool_payout = {}
            # calculate expected payout for each pool
            for pool in p.POOLS:
                # print('pool', pool.id, [node.id for node in pool.nodes])
                if pool.nodes and pool.strategy in ['PPS', 'PPLNS']:
                    mu = ((100 - pool.fee_rate)/100) * ((p.Breward + p.Tfee * S)/len(pool.nodes)) * pool.hash_power/100
                    pool_payout[pool] = mu
                    avg_payout += mu

            if len(pool_payout) == 0:
                continue

            avg_payout /= len(pool_payout)
            # print([(pool.id, pool.strategy, pay) for pool, pay in pool_payout.items()])

            # implementation of pool hopping
            for node in p.NODES:
                if node.node_type == 'selfish' and node.pool.strategy in ['PPS', 'PPLNS']:

                    mu = pool_payout[node.pool]

                    # if current payout is lesser than average payout over all pools then the difference
                    # between average and current pool payouts decides probability of pool hopping
                    if mu < avg_payout and random.random() < (avg_payout - mu)/avg_payout:
                        # print(node.id, ':', node.pool.id, end=' ')

                        # remove miner and hash power from current pool
                        node.pool.hash_power -= node.hashPower
                        node.pool.nodes.remove(node)

                        # implement node hopping strategies
                        if node.node_strategy == 'best':
                            node.pool = max(pool_payout, key=pool_payout.get)

                        # elif node.node_strategy == 'best by strategy':
                        #     strategy_pools = [pool for pool in sorted(pool_payout, key=pool_payout.get) if pool.strategy == node.pool.strategy and pool != node.pool]
                        #     node.pool = strategy_pools[0]

                        elif node.node_strategy == "strategy based":
                            strategy_pools = [pool for pool in p.POOLS if pool.strategy == node.pool.strategy and pool != node.pool]
                            choosenPool = random.randint(0, len(strategy_pools) - 1)
                            node.pool = strategy_pools[choosenPool]

                        elif node.node_strategy == "random":
                            strategy_pools = [pool for pool in p.POOLS if pool.strategy in ['PPS', 'PPLNS'] and pool != node.pool]
                            choosenPool = random.randint(0, len(strategy_pools) - 1)
                            node.pool = strategy_pools[choosenPool]

                        # TODO improve time assignment
                        # c.global_chain[i-1].timestamp + 0.432 * random.expovariate(hashPower * 1/p.Binterval)

                        # update node join time and add miner to new pool
                        node.join_time = current_time
                        node.pool.hash_power += node.hashPower
                        node.pool.nodes.append(node)
                        node.pool_list.append(node.pool.id)
                        # print('--->', node.pool.id, [n.id for n in node.pool.nodes])
                        # add 0 to all pool tracker to begin tracking new pool counts
                        node.blocks_list.append(0)
                        node.balance_list.append(0)
                        node.reward_list.append(0)
