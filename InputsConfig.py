import random
from Models.Bitcoin.Pool import Pool
from Models.Bitcoin.Node import Node

class InputsConfig:

    """ Seclect the model to be simulated.
    0 : The base model
    1 : Bitcoin model
    2 : Ethereum model
    3 : AppendableBlock model
    """
    model = 1

    ''' Input configurations for the base model '''
    if model == 0:

        ''' Block Parameters '''
        Binterval = 600  # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0  # The block size in MB
        Bdelay = 0.42  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 12.5  # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        Tn = 10  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 5.1
        Tfee = 0.000062  # The average transaction fee
        Tsize = 0.000546  # The average transaction size  in MB

        ''' Node Parameters '''
        Nn = 3  # the total number of nodes in the network
        NODES = []
        from Models.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one
        NODES = [Node(id=0), Node(id=1)]

        ''' Simulation Parameters '''
        simTime = 1000  # the simulation length (in seconds)
        Runs = 2  # Number of simulation runs

    ''' Input configurations for Bitcoin model '''
    if model == 1:
        ''' Block Parameters '''
        Binterval = 600  # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0  # The block size in MB
        Bdelay = 0.42  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 6.25  # Reward for mining a block
        Bprice = 58000
        jump_threshold = 0.02

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        Tn = 10  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 5.1
        Tfee = 0.00029  # The average transaction fee
        Tsize = 0.000546  # The average transaction size  in MB

        ''' Node Parameters '''
        Nn = 3  # the total number of nodes in the network

        pool_types = {
            'F2Pool': ('PPS+', 2),
            'Poolin': ('PPS+', 2),
            'BTC.com': ('FPPS', 2),
            'AntPool': ('PPLNS', 2),
            'Huobi': ('PPLNS', 1),
            'Binance Pool': ('PPS', 3),
            'ViaBTC': ('PPS', 4),
            '1THash': ('FPPS', 4),
            # 'OKExPool':,
            # 'SlushPool': '',
            # 'BTC Guild': 'PPLNS',
            # 'GHash.IO':,
            # 'BitFury':,
            # 'BTCC': 'PPS'
        }

        ''' Simulation Parameters '''
        simTime = 1 * 24 * 60 * 60  # the simulation length (in seconds)
        Runs = 1  # Number of simulation runs

        # choose which sim to run
        sim_type = 'honest'
        # sim_type = 'hopping'

        i = 0  # counter to track pool objects
        j = 0  # counter to track node objects
        NODES = []  # list of node objects
        POOLS = []  # list of pool objects

        # function to assign nodes with decreasing hash power to pools
        def create_nodes(node_id, pool, hash_power, NODES=NODES):
            n = random.randint(7, 10)
            for _ in range(n):
                hash_power /= 2
                NODES.append(Node(id=node_id, pool=pool, hashPower=hash_power))
                node_id += 1
            return node_id

        # function to create miner nodes for the selfish sim
        def create_selfish_nodes(node_id, pool, hash_power, NODES=NODES):
            n = random.randint(7, 10)
            for _ in range(n):
                hash_power /= 2
                r = random.random()
                # each hopping strategy (honest, best, strategy-based, random) has a 25% chance of being adopted by a node
                if r < 0.25:
                    NODES.append(Node(id=node_id, pool=pool, hashPower=hash_power, node_type='selfish', node_strategy='best'))
                elif r < 0.5:
                    NODES.append(Node(id=node_id, pool=pool, hashPower=hash_power, node_type='selfish', node_strategy='strategy based'))
                elif r < 0.75:
                    NODES.append(Node(id=node_id, pool=pool, hashPower=hash_power, node_type='selfish', node_strategy='random'))
                else:
                    NODES.append(Node(id=node_id, pool=pool, hashPower=hash_power))
                node_id += 1
            return node_id

        # initialising base fee rates
        base_rate = {'PPS': 2.5, 'FPPS': 2.5, 'PPS+': 2.5, 'PPLNS': 0}

        if sim_type == 'honest':
            hopping = False
            # for each kind of strategy instantiate node and pool objects
            for pool_type in ['SOLO', 'PPS', 'FPPS', 'PPLNS', 'PPS+']:

                if pool_type == 'SOLO':
                    hp = 12
                    # 10 solo miners with monotonically decreasing hash rates
                    for _ in range(10):
                        hp /= 2
                        NODES.append(Node(id=j, hashPower=hp))
                        j += 1
                else:
                    rate = base_rate[pool_type]

                    # 4 pools for PPS and FPPS strategies each
                    if pool_type in ['PPS', 'FPPS']:
                        for f in range(4):
                            hp = 4
                            pool = Pool(_id=i, strategy=pool_type, fee_rate=rate)
                            POOLS.append(pool)
                            j = create_nodes(j, pool, hp)
                            i += 1
                            rate += 0.5


                    else:
                        for w in range(4):
                            if rate in [1, 3]:
                                # for PPS+ and PPLNS pools we vary block window as well
                                for bw in [6, 8, 10, 12]:
                                    hp = 4
                                    pool = Pool(_id=i, strategy=pool_type, fee_rate=rate, block_window=bw)
                                    POOLS.append(pool)
                                    j = create_nodes(j, pool, hp)
                                    i += 1
                                rate += 0.5

                            else:
                                hp = 4
                                pool = Pool(_id=i, strategy=pool_type, fee_rate=rate, block_window=8)
                                POOLS.append(pool)
                                j = create_nodes(j, pool, hp)
                                i += 1
                                rate += 0.5

        else:
            hopping = True
            # hopping sim only considers PPS and PPLNS
            for pool_type in ['PPS', 'PPLNS']:

                # using the same base fee rates as the honest sim
                rate = base_rate[pool_type]

                # create PPS pools of varying fee rate
                if pool_type in ['PPS']:
                    for f in range(4):
                        hp = 5
                        pool = Pool(_id=i, strategy=pool_type, fee_rate=rate)
                        POOLS.append(pool)
                        j = create_selfish_nodes(j, pool, hp)
                        i += 1
                        rate += 0.5

                else:
                    # in case of PPLNS, we vary the block window as well
                    for w in range(4):
                        for bw in [6, 8, 10, 12]:
                            hp = 5
                            pool = Pool(_id=i, strategy=pool_type, fee_rate=rate, block_window=bw)
                            POOLS.append(pool)
                            j = create_selfish_nodes(j, pool, hp)
                            i += 1
                        rate += 0.5


        # sim_type = 'baseline'
        # for pool, (strat, fee) in pool_types.items():
        #     if strat in ['PPLNS', 'PPS+']:
        #         POOLS.append(Pool(_id=pool, strategy=strat, fee_rate=fee, block_window=8))
        #     else:
        #         POOLS.append(Pool(_id=pool, strategy=strat, fee_rate=fee))

        # for i, pool in enumerate(POOLS):
        #     NODES.append(
        #     Node(id=i, pool=pool, hashPower=12.5))

        # sim_type = 'solo'

        # hp = 100
        # for i in range(8):
        #     hp /= 2
        #     NODES.append(Node(id=i, hashPower=hp))

        # sim_type = 'pps'

        # for i, name in enumerate(pool_types):
        #     POOLS.append(Pool(_id=name, strategy='PPS', fee_rate=i))

        # hp = 100
        # for i, pool in enumerate(POOLS):
        #     hp /= 2
        #     NODES.append(Node(id=i, pool=pool, hashPower=hp))

        # sim_type = 'fpps'

        # for i, name in enumerate(pool_types):
        #     POOLS.append(Pool(_id=name, strategy='FPPS', fee_rate=i))

        # hp = 100
        # for i, pool in enumerate(POOLS):
        #     hp /= 2
        #     NODES.append(Node(id=i, pool=pool, hashPower=hp))

        # sim_type = 'pplns'

        # for i, name in enumerate(pool_types):
        #     POOLS.append(Pool(_id=name, strategy='PPLNS', fee_rate=i, block_window=8))

        # hp = 100
        # for i, pool in enumerate(POOLS):
        #     hp /= 2
        #     NODES.append(Node(id=i, pool=pool, hashPower=hp))

        # sim_type = 'pplns_windows'

        # for i, name in enumerate(pool_types):
        #     POOLS.append(Pool(_id=name, strategy='PPLNS', fee_rate=2, block_window=i+2))

        # hp = 100
        # for i, pool in enumerate(POOLS):
        #     hp /= 2
        #     NODES.append(Node(id=i, pool=pool, hashPower=hp))

        # sim_type = 'pps+'

        # for i, name in enumerate(pool_types):
        #     POOLS.append(Pool(_id=name, strategy='PPS+', fee_rate=i, block_window=8))

        # hp = 100
        # for i, pool in enumerate(POOLS):
        #     hp /= 2
        #     NODES.append(Node(id=i, pool=pool, hashPower=hp))

        # sim_type = 'pps+_windows'

        # for i, name in enumerate(pool_types):
        #     POOLS.append(Pool(_id=name, strategy='PPS+', fee_rate=3, block_window=i+2))

        # hp = 100
        # for i, pool in enumerate(POOLS):
        #     hp /= 2
        #     NODES.append(Node(id=i, pool=pool, hashPower=hp))


        # Creating the mining pools
        # POOLS = [
        #     Pool(_id=0, strategy='PPS', fee_rate=3),
        #     Pool(_id=1, strategy='FPPS', fee_rate=3),
        #     Pool(_id=2, strategy='PPS+', fee_rate=3, block_window=8),
        #     Pool(_id=3, strategy='PPLNS', fee_rate=1, block_window=8),
        #     Pool(_id=4, strategy='PPLNS', fee_rate=2, block_window=6),
        #     Pool(_id=5, strategy='PPS', fee_rate=3),
        #     Pool(_id=6, strategy='FPPS', fee_rate=4),
        #     Pool(_id=7, strategy='PPS+', fee_rate=1, block_window=10),
        #     Pool(_id=8, strategy='PPS', fee_rate=3),
        # ]

        # # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        # NODES = [
        #     Node(id=0, pool=POOLS[0], hashPower=7),
        #     Node(id=1, pool=POOLS[1], hashPower=5),
        #     Node(id=2, pool=POOLS[2], hashPower=5),
        #     Node(id=3, pool=POOLS[6], hashPower=8),
        #     Node(id=4, pool=POOLS[7], hashPower=5),
        #     Node(id=5, pool=POOLS[4], hashPower=8),
        #     Node(id=6, pool=POOLS[4], hashPower=5),
        #     Node(id=7, pool=POOLS[3], hashPower=5),
        #     Node(id=8, pool=POOLS[6], hashPower=5),
        #     Node(id=9, pool=POOLS[0], hashPower=7, node_type='selfish', node_strategy='strategy_based'),
        #     Node(id=10, pool=POOLS[3], hashPower=6, node_type='selfish', node_strategy='strategy_based'),
        #     Node(id=11, pool=POOLS[4], hashPower=8, node_type='selfish', node_strategy='strategy_based'),
        #     Node(id=12, pool=POOLS[5], hashPower=5, node_type='selfish', node_strategy='strategy_based'),
        #     Node(id=13, pool=POOLS[7], hashPower=2),
        #     Node(id=14, pool=POOLS[1], hashPower=3),
        #     Node(id=15, hashPower=1),
        #     Node(id=16, hashPower=1),
        #     Node(id=17, hashPower=1),
        #     Node(id=18, hashPower=2),
        #     Node(id=19, pool=POOLS[5], hashPower=2),
        #     Node(id=20, pool=POOLS[5], hashPower=2, node_type='selfish', node_strategy='strategy_based'),
        #     Node(id=21, hashPower=1),
        #     Node(id=22, pool=POOLS[8], hashPower=3, node_type='selfish', node_strategy='strategy_based'),
        #     Node(id=23, pool=POOLS[8], hashPower=2),
        #     Node(id=24, pool=POOLS[8], hashPower=1),
        # ]

    ''' Input configurations for Ethereum model '''
    if model == 2:

        ''' Block Parameters '''
        Binterval = 12.42  # Average time (in seconds)for creating a block in the blockchain
        Bsize = 1.0  # The block size in MB
        Blimit = 8000000  # The block gas limit
        Bdelay = 6  # average block propogation delay in seconds, #Ref: https://bitslog.wordpress.com/2016/04/28/uncle-mining-an-ethereum-consensus-protocol-flaw/
        Breward = 2  # Reward for mining a block

        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator
        Ttechnique = "Light"  # Full/Light to specify the way of modelling transactions
        Tn = 20  # The rate of the number of transactions to be created per second
        # The average transaction propagation delay in seconds (Only if Full technique is used)
        Tdelay = 3
        # The transaction fee in Ethereum is calculated as: UsedGas X GasPrice
        Tsize = 0.000546  # The average transaction size  in MB

        ''' Drawing the values for gas related attributes (UsedGas and GasPrice, CPUTime) from fitted distributions '''

        ''' Uncles Parameters '''
        hasUncles = True  # boolean variable to indicate use of uncle mechansim or not
        Buncles = 2  # maximum number of uncle blocks allowed per block
        Ugenerations = 7  # the depth in which an uncle can be included in a block
        Ureward = 0
        UIreward = Breward / 32  # Reward for including an uncle

        ''' Node Parameters '''
        Nn = 3  # the total number of nodes in the network
        NODES = []
        from Models.Ethereum.Node import Node
        # here as an example we define three nodes by assigning a unique id for each one + % of hash (computing) power
        NODES = [Node(id=0, hashPower=50), Node(
            id=1, hashPower=20), Node(id=2, hashPower=30)]

        ''' Simulation Parameters '''
        simTime = 500  # the simulation length (in seconds)
        Runs = 2  # Number of simulation runs

    ''' Input configurations for AppendableBlock model '''
    if model == 3:
        ''' Transaction Parameters '''
        hasTrans = True  # True/False to enable/disable transactions in the simulator

        Ttechnique = "Full"

        # The rate of the number of transactions to be created per second
        Tn = 10

        # The maximum number of transactions that can be added into a transaction list
        txListSize = 100

        ''' Node Parameters '''
        # Number of device nodes per gateway in the network
        Dn = 10
        # Number of gateway nodes in the network
        Gn = 2
        # Total number of nodes in the network
        Nn = Gn + (Gn*Dn)
        # A list of all the nodes in the network
        NODES = []
        # A list of all the gateway Ids
        GATEWAYIDS = [chr(x+97) for x in range(Gn)]
        from Models.AppendableBlock.Node import Node

        # Create all the gateways
        for i in GATEWAYIDS:
            otherGatewayIds = GATEWAYIDS.copy()
            otherGatewayIds.remove(i)
            # Create gateway node
            NODES.append(Node(i, "g", otherGatewayIds))

        # Create the device nodes for each gateway
        deviceNodeId = 1
        for i in GATEWAYIDS:
            for j in range(Dn):
                NODES.append(Node(deviceNodeId, "d", i))
                deviceNodeId += 1

        ''' Simulation Parameters '''
        # The average transaction propagation delay in seconds
        propTxDelay = 0.000690847927

        # The average transaction list propagation delay in seconds
        propTxListDelay = 0.00864894

        # The average transaction insertion delay in seconds
        insertTxDelay = 0.000010367235

        # The simulation length (in seconds)
        simTime = 500

        # Number of simulation runs
        Runs = 5

        ''' Verification '''
        # Varify the model implementation at the end of first run
        VerifyImplemetation = True

        maxTxListSize = 0
