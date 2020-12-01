#######################################################################################
#
# This class is used to collect simulation data and to produce an Excel report with
# several worksheets as required by the AppendableBlock model.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################


from InputsConfig import InputsConfig as p
from Models.Consensus import Consensus as c
from Models.Incentives import Incentives
import pandas as pd
from Models.AppendableBlock.Block import Block as block
import numpy as np
from datetime import datetime


class Statistics:

    # Hold various calculations
    total_blocks = 0
    chains = []
    transactions = []
    transaction_latencies = []
    average_transaction_latency = 0.0
    transaction_throughput = 0.0
    simulation_duration = 0.0

    # Gathers simulation data and calculates the results
    def calculate():
        Statistics.gateway_chains()
        Statistics.gateway_transactions()
        Statistics.transaction_latency()
        Statistics.results()

    # Gathers information relating to the gateway chains
    def gateway_chains():
        for gateway_node in p.NODES[0:p.Gn]:
            for b in gateway_node.blockchain:
                info = [gateway_node.id, b.depth, b.id, b.previous,
                        b.timestamp, len(b.transactions)]
                Statistics.chains += [info]

    # Gathers transaction data from the gateway blockchains
    def gateway_transactions():
        for gateway_node in p.NODES[0:p.Gn]:
            for b in gateway_node.blockchain:
                for tx in b.transactions:
                    info = [gateway_node.id, tx.id, tx.sender, tx.to,
                            tx.timestamp[0], tx.timestamp[1], tx.timestamp[2]]
                    Statistics.transactions += [info]

    # Calculates transaction latencies
    def transaction_latency():
        sorted_tx = []
        sorted_tx = Statistics.transactions.copy()
        sorted_tx.sort(key=lambda tx: tx[1])
        max_insertion_time = 0.0
        tx_count = 0

        for tx in sorted_tx:
            tx_count += 1
            if tx[6] > max_insertion_time:
                max_insertion_time = tx[6]
            if tx_count % p.Gn == 0:
                latency = max_insertion_time-tx[4]
                info = [tx[1], latency]
                Statistics.transaction_latencies.append(info)
                max_insertion_time = 0.0

    # Calculates the results
    def results():
        # Calculate average transcation latency
        latancies = []
        for l in Statistics.transaction_latencies:
            latancies.append(l[1])
        Statistics.average_transaction_latency = np.mean(latancies)

        # Obtain the earliest transaction creation time
        # and the latest transaction insertion time
        earliest_tx_creation_time = 9999999999.0
        latest_tx_insertion_time = 0.0
        for tx in Statistics.transactions:
            if tx[4] < earliest_tx_creation_time:
                earliest_tx_creation_time = tx[4]

            if tx[6] > latest_tx_insertion_time:
                latest_tx_insertion_time = tx[6]

        # Calculate the simulation duration
        Statistics.simulation_duration = latest_tx_insertion_time - earliest_tx_creation_time

        # Calculate transaction throughput (transactions per second)
        number_of_tx = float(p.Dn * p.Gn * p.Tn)
        Statistics.transaction_throughput = number_of_tx/Statistics.simulation_duration

    # Produce results report as an Excel worksheet
    def print_to_excel(simulationRunNumber, detail_report):
        # Create the worksheets
        df1 = pd.DataFrame({'No. of Gateways': [p.Gn], 'Total No. of Devices': [
            p.Gn * p.Dn], 'Total No. of Blocks': [Statistics.total_blocks], 'Blocks per Chain': [Statistics.total_blocks/p.Gn], 'Max TX List Size': [p.maxTxListSize], 'Total Transcations': [p.Gn*p.Dn*p.Tn], 'Average Transaction Latency': [Statistics.average_transaction_latency], 'Transaction Throughput': [
            Statistics.transaction_throughput], 'Simulation Duration (secs)': [Statistics.simulation_duration]})

        df2 = pd.DataFrame({'No. of Gateways': [p.Gn], 'No. of Devices per Gateway': [
            p.Dn], 'Total No. of Devices': [p.Gn*p.Dn], 'Total No. of Nodes': [p.Nn], 'Transactions per Device': [p.Tn]})

        if detail_report:
            df3 = pd.DataFrame(Statistics.chains)
            df3.columns = ['Gateway Node ID', 'Block Depth', 'Block ID',
                           'Previous Block ID', 'Block Timestamp', 'No. of Transactions']

            df4 = pd.DataFrame(Statistics.transactions)
            df4.columns = ['Gateway Node ID', 'Tx ID', 'Sender Node ID',
                           'Receiver Node ID', 'Tx Creation Time', 'Tx Reception Time', 'Tx Insertion Time']

            df5 = pd.DataFrame(Statistics.transaction_latencies)
            df5.columns = ['TxID', 'Latency']

        # Setup the filename
        fname = "Statistics-{0}-{1}.xlsx".format(
            datetime.now().strftime("%d.%m.%Y-%H.%M.%S"), (simulationRunNumber + 1))

        # Save worksheets into the workbook
        writer = pd.ExcelWriter(fname, engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='Results')
        df2.to_excel(writer, sheet_name='InputConfig')
        if detail_report:
            df3.to_excel(writer, sheet_name='GatewayBlockchains')
            df4.to_excel(writer, sheet_name='GatewayTransactions')
            df5.to_excel(writer, sheet_name='transaction_latencies')
        writer.save()

    # Reset the statistics data and clear global variables ready for the next simulation run
    def reset():
        # Initialise class variables
        Statistics.total_blocks = 0
        Statistics.chains.clear()
        Statistics.transactions.clear()
        Statistics.transaction_latencies.clear()
        Statistics.average_transaction_latency = 0.0
        Statistics.transaction_throughput = 0.0
        Statistics.simulation_duration = 0.0

        # Initialise gateway node variables
        for node in p.NODES[0:p.Gn]:
            node.reset_state()
