# BlockSim Simultor

## What is BlockSim Simulator?
**BlockSim** is an open source blockchain simulator, capturing network, consensus and incentives layers of blockchain systems. BlockSim aims to provide simulation constructs that are intuitive, hide unnecessary detail and can be easily manipulated to be applied to a large set of blockchains design and deployment questions (related to performance, reliability, security or other properties of interest). At the core of BlockSim is a Base Model, which contains a number of functional blocks (e.g., blocks, transactions and nodes) common across blockchains, that can be extended and configured as suited for the system and study of interest. BlockSim is implemented in **Python**.

For more details about BlockSim, we refer to our journal paper that can be freely accessed online https://www.frontiersin.org/articles/10.3389/fbloc.2020.00028/full

## Installation and Requirements

Before you can use BlockSim  simulator, you need to have **Python version 3 or above** installed in your machine as well as have the following packages installed:

- pandas 
>pip install pandas
- numpy 
>pip install numpy
- sklearn 
>pip install sklearn
- xlsxwriter
>pip install xlsxwriter

## Running the simulator

Before you run the simulator, you can access the configuration file *InputsConfig.py* to choose the model of interest (Base Model 0, Bitcoin Model 1 and Ethereum Model 2) and to set up the related parameters.
The parameters include the number of nodes (and their fraction of hash power), the block interval time, the block propagation delays, the block and transaction sizes, the block rewards, the tranaction fees etc.
Each model has a slightly different (or additional) parameters to capture it.

To run the simulator, one needs to trigger the main class *Main.py* either from the command line
> python Main.py

or using any Python editor such as Spyder.

## Statistics and Results

The results of the simulator is printed in an excel file at the end of the simulation. The results include the blockchain ledger, number of blocks mined, number of stale (uncles) blocks and the rewards gained by each miner etc. 

## Contact

For any query about how to use or even extend the simulator, feel free to contact me **alharbi.maher@gmail.com**
