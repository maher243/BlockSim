#######################################################################################
#
# This class contains various methods for verifying that the implementation of the
# AppendableBLock model is correct.
#
# Author: Panayiota Theodorou
# Date: March 2020
#
#######################################################################################

from InputsConfig import InputsConfig as p
from Models.AppendableBlock.Block import Block as block
from Models.AppendableBlock.Transaction import Transaction as Transaction
import pandas as pd
import numpy as np
from datetime import datetime


class Verification:

    # Holds all the results from the verification checks
    verification_results = []

    # Performs all the verification checks
    def perform_checks():
        Verification.check_total_nodes()
        Verification.check_gateway_nodes()
        Verification.check_device_nodes()
        Verification.check_total_blocks()
        Verification.check_block_ids()
        Verification.check_genesis_blocks()
        Verification.check_gateway_blocks()
        Verification.check_device_blocks()
        Verification.check_block_chaining()
        Verification.check_total_transactions()
        Verification.check_transaction_pools()
        Verification.check_transactions_ids()
        Verification.check_transaction_sets()
        Verification.check_device_transactions()
        Verification.check_transaction_chaining()
        Verification.check_transaction_latency()
        Verification.check_transaction_throughput()
        Verification.produce_verification_report()

    # Converts the verification check status to a string
    def display_status(check_passed):
        status = []
        if check_passed:
            status = "PASSED"
        else:
            status = "FAILED"

        return status

    # Checks that the total number of nodes created is correct
    def check_total_nodes():
        check_passed = True
        check_info = []
        check_result = []
        expected_nodes = p.Nn
        check_info = "%s nodes found" % (expected_nodes)
        nodes_found = len(p.NODES)

        if nodes_found != expected_nodes:
            check_passed = False
            check_info = "Expecting %s nodes and found %s" % (
                expected_nodes, nodes_found)

        check_result = ["Check Total Nodes",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Returns the number of nodes created of the specified node type
    def get_number_of_nodes(node_type):
        node_count = 0

        if node_type == "g":
            for node in p.NODES[0:p.Gn]:
                if node.nodeType == node_type:
                    node_count += 1
        else:
            for node in p.NODES[p.Gn:]:
                if node.nodeType == node_type:
                    node_count += 1

        return node_count

    # Checks that the number of gateway nodes created is correct
    def check_gateway_nodes():
        check_passed = True
        check_info = []
        check_result = []
        expected_gateways = p.Gn
        check_info = "%s gateway nodes found" % (expected_gateways)
        gateways_found = Verification.get_number_of_nodes("g")
        if gateways_found != expected_gateways:
            check_passed = False
            check_info = "Expecting %s gateway nodes and found %s" % (
                expected_gateways, gateways_found)

        check_result = ["Check Gateway Nodes",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that the number of device nodes created is correct
    def check_device_nodes():
        check_passed = True
        check_info = []
        check_result = []

        expected_devices = p.Gn * p.Dn

        check_info = "%s device nodes found" % (expected_devices)
        devices_found = Verification.get_number_of_nodes("d")

        if devices_found != expected_devices:
            check_passed = False
            check_info = "Expecting %s device nodes and found %s" % (
                expected_devices, devices_found)

        check_result = ["Check Device Nodes",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that the total number of blocks created is correct
    def check_total_blocks():
        check_passed = True
        check_info = []
        check_result = []

        # Check the blocks for each gateway
        # Expected blocks = Genesis block + gateway blocks + device blocks
        expected_blocks_per_gateway = 1 + p.Gn + (p.Gn * p.Dn)
        check_info = "%s blocks found in all the gateway blockchains" % (
            expected_blocks_per_gateway)

        for gateway_node in p.NODES[0:p.Gn]:
            if len(gateway_node.blockchain) != expected_blocks_per_gateway:
                check_passed = False
                check_info = "Expecting %s blocks and found %s in the blockchain of gateway %s" % (
                    expected_blocks_per_gateway, len(gateway_node.blockchain), gateway_node.id)
                break

        check_result = ["Check Total Blocks",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that all the block ids are unique
    def check_block_ids():
        check_passed = True
        check_info = []
        check_result = []
        block_id_set = set()

        check_info = "Block ids are unique for all the gateway blockchains"
        for gateway_node in p.NODES[0:p.Gn]:
            block_id_set.clear()
            for block in gateway_node.blockchain:
                if block.id in block_id_set:
                    check_passed = False
                    check_info = "Block id %s is not unique in the blockchain of gateway %s" % (
                        block.id, gateway_node.id)
                    break
                else:
                    block_id_set.add(block.id)

            if not check_passed:
                break

        check_result = ["Check Block Ids",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that each blockchain has a genesis block
    def check_genesis_blocks():
        check_passed = True
        check_info = []
        check_result = []
        check_info = "One genesis block found in all the gateway blockchains"

        for gateway_node in p.NODES[0:p.Gn]:
            block = gateway_node.blockchain[0]
            if block.id != 0 or block.previous != -1:
                check_passed = False
                check_info = "No genesis block found in the blockchain of gateway %s" % (
                    gateway_node.id)
                break

        check_result = ["Check Genesis Blocks",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that each blockchain has blocks for all the gateways
    def check_gateway_blocks():
        check_passed = True
        check_info = []
        check_result = []
        check_info = "%s gateway blocks found in all the gateway blockchains" % (
            p.Gn)

        for gateway_node in p.NODES[0:p.Gn]:
            block_count = 0
            for b in gateway_node.blockchain[1:p.Gn]:
                if b.nodeId != p.GATEWAYIDS[block_count]:
                    check_passed = False
                    check_info = "Gateway %s has no block for gateway %s in its blockchain" % (gateway_node,
                                                                                               p.GATEWAYIDS[block_count])
                    break
                block_count += 1

            if not check_passed:
                break

        check_result = ["Check Gateway Blocks",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that each blockchain has blocks for all the devices
    def check_device_blocks():
        check_passed = True
        check_info = []
        check_result = []
        expected_device_blocks_per_gateway = p.Gn * p.Dn
        check_info = "%s device blocks found in all the gateway blockchains" % (
            expected_device_blocks_per_gateway)

        for gateway_node in p.NODES[0:p.Gn]:
            for device_node_id in range(1, p.Dn+1):
                if gateway_node.blockchain[p.Gn + device_node_id].nodeId != device_node_id:
                    check_passed = False
                    check_info = "Gateway %s has no block for device %s in its blockchain" % (
                        gateway_node.nodeId, device_node_id)
                    break

            if not check_passed:
                break

        check_result = ["Check Device Blocks",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that each blockchain has its blocks chained correctly
    def check_block_chaining():
        check_passed = True
        check_info = []
        check_result = []
        check_info = "Blocks in all the gateway blockchains are chained correctly"

        for gateway_node in p.NODES[0:p.Gn]:
            previous_block_id = -1
            for block in gateway_node.blockchain:
                if block.previous != previous_block_id:
                    check_passed = False
                    check_info = "In the blockchain of gateway %s block %s is pointing to block %s instead of block %s" % (
                        gateway_node.nodeId, block.id, block.previous, previous_block_id)
                    break
                else:
                    previous_block_id = block.id

            if not check_passed:
                break

        check_result = ["Check Block Chaining",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that each blockchain has the correct number of transactions.
    def check_total_transactions():
        check_passed = True
        check_info = []
        check_result = []

        expected_transactions_per_gateway = p.Dn * p.Gn * p.Tn
        check_info = "%s transaction found in all the gateway blockchains" % (
            expected_transactions_per_gateway)

        for gateway_node in p.NODES[0:p.Gn]:
            total_transactions = 0
            for block in gateway_node.blockchain:
                total_transactions += len(block.transactions)

            if total_transactions != expected_transactions_per_gateway:
                check_passed = False
                check_info = "Expecting %s transaction and found %s in the blockchain of gateway %s" % (
                    expected_transactions_per_gateway, total_transactions, gateway_node.id)
                break

            if not check_passed:
                break

        check_result = ["Check Total Transcations",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that all transaction in each gateway have been processed.
    def check_transaction_pools():
        check_passed = True
        check_info = []
        check_result = []
        check_info = "All gateway transaction pools processed"

        for gateway_node in p.NODES[0:p.Gn]:
            tx_count = len(gateway_node.transactionsPool)
            if tx_count != 0:
                check_passed = False
                check_info = "Transaction pool of gateway %s contains %s transactions" % (
                    gateway_node.id, tx_count)
            break

        check_result = ["Check Transcation Pool",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that the transactions, in each blockchain, have unique ids
    def check_transactions_ids():
        check_passed = True
        check_info = []
        check_result = []
        tx_set = set()

        check_info = "Transactions ids in all the gateway blockchain are unique"
        for gateway_node in p.NODES[0:p.Gn]:
            tx_set.clear()
            for block in gateway_node.blockchain:
                for tx in block.transactions:
                    if tx.id in tx_set:
                        check_passed = False
                        check_info = "Transaction id %s is not unique in the blockchain of gateway %s" % (
                            tx.id, gateway_node.id)
                        break
                    else:
                        tx_set.add(tx.id)

                if not check_passed:
                    break

            if not check_passed:
                break

        check_result = ["Check Transcation Ids",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Creates a set of transactions for the specified blockchain
    def create_blockchain_tx_set(tx_set, BlockChain):
        for block in BlockChain:
            for tx in block.transactions:
                if not (tx.id in tx_set):
                    tx_set.add(tx.id)

    # Checks that all the blockchains have the same set of transactions
    def check_transaction_sets():
        check_passed = True
        check_info = []
        check_result = []
        first_gateway_tx_set = set()
        check_info = "All gateway blockchains have the same set of transactions"
        Verification.create_blockchain_tx_set(
            first_gateway_tx_set, p.NODES[0].blockchain)
        for gateway_node in p.NODES[1:p.Gn]:
            gateway_tx_set = set()
            Verification.create_blockchain_tx_set(
                gateway_tx_set, gateway_node.blockchain)
            if gateway_tx_set != first_gateway_tx_set:
                check_passed = False
                check_info = "The transactions in the blockchain of gateway %s are different from those in the blockchain of gateway %s" % (
                    gateway_node.id, p.NODES[0].id)
                break

        check_result = ["Check Transcations Sets",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that device transactions are inserted into the correct blocks
    def check_device_transactions():
        check_passed = True
        check_info = []
        check_result = []
        check_info = "Transactions from all devices are inserted into all the gateway blockchains correctly"

        for gateway_node in p.NODES[0:p.Gn]:
            device_id = 0
            for block in gateway_node.blockchain[1+p.Gn:]:
                device_id += 1
                for tx in block.transactions:
                    if tx.sender != device_id:
                        check_passed = False
                        check_info = "Transaction %s from device %s found in block for devive %s in the blockchain of gateway %s" % (
                            tx.id, tx.sender, device_id,  gateway_node.id)
                        break
                if not check_passed:
                    break
            if not check_passed:
                break

        check_result = ["Check Device Transcations",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that transactions in all block ledgers are chained correctly
    def check_transaction_chaining():
        check_passed = True
        check_info = []
        check_result = []
        check_info = "Transactions in all block ledgers are chained correctly"

        for gateway_node in p.NODES[0:p.Gn]:
            device_id = 0
            for block in gateway_node.blockchain[1+p.Gn:]:
                device_id += 1
                previous_tx_id = -1
                for tx in block.transactions:
                    if tx.previous != previous_tx_id:
                        check_passed = False
                        check_info = "In block ledger of device %s transaction %s is pointing to transaction %s instead of transaction %s" % (
                            device_id, tx.id, tx.previous, previous_tx_id)
                        break
                    previous_tx_id = tx.id

                if not check_passed:
                    break
            if not check_passed:
                break

        check_result = ["Check Transaction Chaining",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that the average transaction latency is of the correct order
    def check_transaction_latency():
        check_passed = True
        check_info = []
        check_result = []
        TWO_HUNDRED_MS = 200.0

        average_latency = 0
        max_insertion_time = 0.0
        tx_info = []
        latencies = []
        tx_count = 0

        # Gather all the transaction from all the gateways
        for gateway_node in p.NODES[0:p.Gn]:
            for block in gateway_node.blockchain:
                for tx in block.transactions:
                    tx_info.append([tx.id, tx.timestamp[0], tx.timestamp[2]])

        # Order the transactions by creation time
        tx_info.sort(key=lambda tx: tx[1])

        # Calculate the average latency
        for tx in tx_info:
            tx_count += 1
            if tx[2] > max_insertion_time:
                max_insertion_time = tx[2]
            if tx_count % p.Gn == 0:
                latencies.append(max_insertion_time-tx[1])
                max_insertion_time = 0.0

        average_latency = round(np.mean(latencies)*1000, 1)

        check_info = "Average transaction latency of %s ms is of the correct order" % (
            average_latency)

        if average_latency > TWO_HUNDRED_MS:
            check_passed = False
            check_info = "Average transaction latency of %s ms is higher than expected" % (
                average_latency)

        check_result = ["Check Transcation Latency",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Checks that the transaction throughput is correct
    def check_transaction_throughput():
        check_passed = True
        check_info = []
        check_result = []
        earliest_tx_creation_time = 9999999999.0
        latest_tx_insertion_time = 0.0
        ONE_PERCENT = 1
        tx_submission_rate = p.Dn * p.Gn

        # Collect all the transaction from al the gateway chains
        for gateway_node in p.NODES[0:p.Gn]:
            for block in gateway_node.blockchain:
                for tx in block.transactions:
                    if tx.timestamp[0] < earliest_tx_creation_time:
                        earliest_tx_creation_time = tx.timestamp[0]
                    if tx.timestamp[2] > latest_tx_insertion_time:
                        latest_tx_insertion_time = tx.timestamp[2]
        transaction_throughput = round(float(
            p.Dn * p.Gn * p.Tn)/(latest_tx_insertion_time - earliest_tx_creation_time), 3)
        percentage_increase = (
            abs(transaction_throughput - tx_submission_rate)/tx_submission_rate)*100

        check_info = "Transaction throughput of %s per second is close enough to the submission rate of %s per second" % (
            transaction_throughput, tx_submission_rate)

        if percentage_increase > ONE_PERCENT:
            check_passed = False
            check_info = "Transaction throughput of %s per second is not close enough to the submission rate of %s per second" % (
                transaction_throughput, tx_submission_rate)

        check_result = ["Check Transcation Throughput",
                        Verification.display_status(check_passed), check_info]

        Verification.verification_results.append(check_result)

    # Produce verification report as an Excel worksheet
    def produce_verification_report():
        # Create the worksheets
        df1 = pd.DataFrame({'No. of Gateways': [p.Gn], 'No. of Devices per Gateway': [
            p.Dn], 'Total of No. of Nodes': [p.Nn], 'Transactions per Device': [p.Tn]})

        df2 = pd.DataFrame(Verification.verification_results)
        df2.columns = ['Verification Check', 'Status', 'Additional Info']

        # Setup the filename
        file_name = "VerificationResults-{0}.xlsx".format(
            datetime.now().strftime("%d.%m.%Y-%H.%M.%S"))

        # Save worksheets into the workbook
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        df1.to_excel(writer, sheet_name='InputConfig')
        df2.to_excel(writer, sheet_name='VerificationResults')
        writer.save()
