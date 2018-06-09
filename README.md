# cs244-hashpipe-reproduction

## Description



## Running the demo

To reproduce our P4 results . For more instructions on setting up P4 and running a simulation see the README file in the p4_code folder.

To reproduce our results from our Python HashPipe algorithm simulator, run `python results.py` in the evaluation folder of our project. It requires a csv file in the data folder containing TCP packet traces. To produce this file from a compressed or decompressed pcap file, first download the pcap file and then change the file name in `data/pcap_to_csv.sh` to the path of this pcap file. Then you can run `sh data/pcap_to_csv.sh`. 

`results.py` reproduces figures 2, 3, and 6 from the original HashPipe paper by default, but these figures are clearly commented in the code and can be commented out if you desire a subset of the figures.

## Data

We ran our simulator of the HashPipe algorithm on data from "The CAIDA Anonymized Internet Traces 2016 Dataset", a trace from an ISP backbone link available at:
https://www.caida.org/data/passive/passive_2016_dataset.xml

It is unavailable to the public but if you wish to reproduce our results please request access from the CAIDA organization.

We also produced results on an anonymized trace from a datacenter available at:
http://pages.cs.wisc.edu/~tbenson/IMC10_Data.html

These traces are available to the public.

## Files

The evaluation folder contains all of the files needed to reproduce the HashPipe paper's figures 2, 3, and 6 using our Python simulator. The evaluation/data folder includes the pcap_to_csv.sh files which parses pcap files into a Python friendly csv file and is where our code expects the parsed csv files to be. The evaluation folder also contains all of our reproduced figures. The Python classes included are:

results.py - This is the file that produces all of the referenced figures by creating the HashPipe simulator with the correct parameters and getting statistics on the resulting tables. 

hashPipeSimulator.py - This file contains the HashPipe algorithm and simulates it in Python, producing the final hash tables that are produced by P4 on the switch.

flowCounter.py - This file contains some utility functions that do processing on a csv file of packets, counting the number of flows and getting the true k heavy hitters.

utils.py - Contains utility functions

The p4_code folder contains all of the code relevant to our reproduction of the HashPipe algorithm in P4. 
