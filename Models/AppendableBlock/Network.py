#######################################################################################
#
# This class is used to abstract various network delays for the AppendableBlock model.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################

import random
from InputsConfig import InputsConfig as p


class Network:
    # Delay for propagating transactions in the network
    def tx_prop_delay():
        return random.expovariate(1/p.propTxDelay)

    # Delay for propagating transactions in the network
    def tx_list_prop_delay():
        return random.expovariate(1/p.propTxListDelay)

    # Delay for releasing the token
    def tx_token_release_delay():
        return random.uniform(0.0001, 0.0005)
