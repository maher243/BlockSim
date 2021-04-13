from datetime import datetime
from InputsConfig import InputsConfig as p
from Event import Event, Queue
from Scheduler import Scheduler
from Statistics import Statistics

if p.model == 3:
    from Models.AppendableBlock.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.AppendableBlock.Transaction import FullTransaction as FT
    from Models.AppendableBlock.Node import Node
    from Models.Incentives import Incentives
    from Models.AppendableBlock.Statistics import Statistics
    from Models.AppendableBlock.Verification import Verification

elif p.model == 2:
    from Models.Ethereum.BlockCommit import BlockCommit
    from Models.Ethereum.Consensus import Consensus
    from Models.Ethereum.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Ethereum.Node import Node
    from Models.Ethereum.Incentives import Incentives

elif p.model == 1:
    from Models.Bitcoin.BlockCommit import BlockCommit
    from Models.Bitcoin.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Bitcoin.Node import Node
    from Models.Bitcoin.Pool import Pool
    from Models.Incentives import Incentives

elif p.model == 0:
    from Models.BlockCommit import BlockCommit
    from Models.Consensus import Consensus
    from Models.Transaction import LightTransaction as LT, FullTransaction as FT
    from Models.Node import Node
    from Models.Incentives import Incentives

########################################################## Start Simulation ##############################################################


def main():
    for i in range(p.Runs):
        print('-'*10, f'Run: {i+1}', '-'*10)
        print(p.sim_type)
        print('No. of Miners:', len(p.NODES))

        hash_power = 0
        # Giving every pool a reference to the nodes it contains. Also, update the total hashrate of a pool.
        print('SOLO Nodes: ', end='')
        for node in p.NODES:
            hash_power += node.hashPower
            if node.pool:
                node.pool.nodes.append(node)
                node.pool.hash_power += node.hashPower
            else:
                print(node.id, end=', ')
        print()

        print('Pools:')
        for pool in p.POOLS:
            print(' -', pool.id, pool.strategy, 'Fee Rate:', pool.fee_rate, 'Nodes:', [node.id for node in pool.nodes], 'Hash power:', pool.hash_power)
        print('Total hash power:', hash_power, '\n')

        clock = 0  # set clock to 0 at the start of the simulation
        if p.hasTrans:
            if p.Ttechnique == "Light":
                LT.create_transactions()  # generate pending transactions
            elif p.Ttechnique == "Full":
                FT.create_transactions()  # generate pending transactions

        Node.generate_gensis_block()  # generate the gensis block for all miners
        # initiate initial events >= 1 to start with
        BlockCommit.generate_initial_events()

        while not Queue.isEmpty() and clock <= p.simTime:
            next_event = Queue.get_next_event()
            clock = next_event.time  # move clock to the time of the event
            BlockCommit.handle_event(next_event)
            Queue.remove_event(next_event)

        # for the AppendableBlock process transactions and
        # optionally verify the model implementation
        if p.model == 3:
            BlockCommit.process_gateway_transaction_pools()

            if i == 0 and p.VerifyImplemetation:
                Verification.perform_checks()

        Consensus.fork_resolution()  # apply the longest chain to resolve the forks
        # distribute the rewards between the particiapting nodes
        Incentives.distribute_rewards()
        # calculate the simulation results (e.g., block statstics and miners' rewards)
        Statistics.calculate(i)

        if p.model == 3:
            Statistics.print_to_excel(i, True)
            Statistics.reset()
        else:
            ########## reset all global variable before the next run #############
            Statistics.reset()  # reset all variables used to calculate the results
            Node.resetState()  # reset all the states (blockchains) for all nodes in the network
            Pool.resetState()  # reset all pools in the network

    # set file name for results
    fname = f"{p.sim_type}_{int(p.simTime/(24*60*60))}days_{datetime.now()}.xlsx".replace(':', '_')
    # fname = f"(Allverify)1day_{p.Bsize/1000000}M_{p.Tn/1000}K-{i}-{datetime.now()}.xlsx".replace(':', '_')
    # print all the simulation results in an excel file
    Statistics.print_to_excel(fname)
    # Statistics.reset2()  # reset profit results

######################################################## Run Main method #####################################################################

if __name__ == '__main__':
    main()
