from InputsConfig import InputsConfig as p
from Event import Event, Queue
from Scheduler import Scheduler
from Statistics import Statistics

if p.model==2:
	from Models.Ethereum.BlockCommit import BlockCommit
	from Models.Ethereum.Consensus import Consensus
	from Models.Ethereum.Transaction import LightTransaction as LT, FullTransaction as FT
	from Models.Ethereum.Node import Node
	from Models.Ethereum.Incentives import Incentives

elif p.model==1:
	from Models.Bitcoin.BlockCommit import BlockCommit
	from Models.Bitcoin.Consensus import Consensus
	from Models.Transaction import LightTransaction as LT, FullTransaction as FT
	from Models.Bitcoin.Node import Node
	from Models.Incentives import Incentives

elif p.model==0:
	from Models.BlockCommit import BlockCommit
	from Models.Consensus import Consensus
	from Models.Transaction import LightTransaction as LT, FullTransaction as FT
	from Models.Node import Node
	from Models.Incentives import Incentives

########################################################## Start Simulation ##############################################################
def main():
    for i in range (p.Runs):
        clock =0 # set clock to 0 at the start of the simulation
        if p.hasTrans:
            if p.Ttechnique == "Light": LT.create_transactions() # generate pending transactions
            elif p.Ttechnique == "Full": FT.create_transactions() # generate pending transactions

        Node.generate_gensis_block() # generate the gensis block for all miners
        BlockCommit.generate_initial_events() # initiate initial events >= 1 to start with

        while  not Queue.isEmpty() and clock <= p.simTime:
            next_event = Queue.get_next_event()
            clock = next_event.time # move clock to the time of the event
            BlockCommit.handle_event(next_event)
            Queue.remove_event(next_event)

        Consensus.fork_resolution() # apply the longest chain to resolve the forks
        Incentives.distribute_rewards()# distribute the rewards between the particiapting nodes
        Statistics.calculate() # calculate the simulation results (e.g., block statstics and miners' rewards)

		########## reset all global variable before the next run #############
        Statistics.reset() # reset all variables used to calculate the results
        Node.resetState() # reset all the states (blockchains) for all nodes in the network
    fname= "(Allverify)1day_{0}M_{1}K.xlsx".format(p.Bsize/1000000, p.Tn/1000)
    Statistics.print_to_excel(fname) # print all the simulation results in an excel file
    Statistics.reset2() # reset profit results



######################################################## Run Main method #####################################################################
if __name__ == '__main__':
    main()
