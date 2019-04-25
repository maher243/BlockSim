from InputsConfig import InputsConfig as p
from Queue import Queue
from Transaction import Transaction
from Event import Event
from Consensus import Consensus
from Scheduler import Scheduler
from Results import Results
from Node import Node
from VerifTest import VerifTest
import scipy as sp
import numpy as np
import math
import statistics

########################################################## Start Simulation ##############################################################
def main():
    for i in range (p.Runs):
        clock =0 # set clock to 0 at the start of the simulation
        if p.hasTrans:
            if p.Ttechnique == "Light":
                LightTransaction.create_transactions() # generate pending transactions
            elif p.Ttechnique == "Full":
                Transaction.create_transactions_full() # generate pending transactions

        Node.generate_gensis_block() # generate the gensis block for all miners
        Scheduler.initial_events() # initiate initial events to start with

        while  not Queue.isEmpty() and clock <= p.simTime:
            next_event = Queue.get_next_event()
            clock = next_event.time # move clock to the time of the event
            Event.run_event(next_event)
            Queue.remove_event(next_event)

        Consensus.longest_chain() # apply the longest chain to resolve the forks
        Results.calculate() # calculate the simulation results (e.g., block statstics and miners' rewards)

        ########## reset all global variable before the next run #############
        Results.reset() # reset all variables used to calculate the results
        Node.resetState() # reset all the states (blockchains) for all nodes in the network

    Results.print_to_excel() # print all the simulation results in an excel file



######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
