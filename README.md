# cs244-hashpipe-reproduction

## Description

Sierra Kaplan-Nelson and Colin Kincaid's (reproducible) reproduction of "Detecting Heavy-Hitters Entirely in the Data Plane" by Sivaraman et al. See our final report pdf as `final_paper.pdf` in this directory.

## Running our code

For instructions on setting up P4 and running our code, see the `README` file in the `p4_code` folder.

To reproduce our results from our Python HashPipe algorithm simulator, run `python results.py` in the evaluation folder of our project. It requires a csv file in the data folder containing header fields from TCP packet traces.

To produce a properly formatted csv file from a network traffic trace, first download the pcap file and then change the file name in `data/pcap_to_csv.sh` to the path of this pcap file. Then you can run `sh data/pcap_to_csv.sh`. This parsing script uses TShark compiled with zlib so that it can work on compressed pcap files if desired. You must have Wireshark downloaded in order to use TShark. In order to install zlib, download the file on zlib.net, cd into the folder where you downloaded it, run `./configure; make test` and check that it is okay, and finally run `sudo make install`.

`results.py` reproduces Figures 2, 3, and 6 from the original HashPipe paper by default, but the sections for each figure are clearly documented in the code and can be commented out if you desire a subset of the figures.

## Data

We ran our simulator of the HashPipe algorithm on data from "The CAIDA Anonymized Internet Traces 2016 Dataset", a trace from an ISP backbone link available at:
https://www.caida.org/data/passive/passive_2016_dataset.xml

The trace is unavailable to the public, but if you wish to reproduce our results, please request access from the CAIDA organization.

We also produced results on an anonymized trace from a datacenter available at:
http://pages.cs.wisc.edu/~tbenson/IMC10_Data.html

These traces are available to the public.

## Files

The evaluation folder contains all of the files needed to reproduce the HashPipe paper's Figures 2, 3, and 6 using our Python simulator. The `evaluation/data` folder includes the `pcap_to_csv.sh` script, which parses pcap files into a Python-friendly csv format and is where our code expects the parsed csv files to be. The evaluation folder also contains all of our reproduced figures. The Python classes included are:

`results.py` - This is the file that produces all of the referenced figures by creating the HashPipe simulator with the correct parameters and getting statistics on the resulting tables. 

`hashPipeSimulator.py` - This file implements the HashPipe algorithm in Python, producing the same hash tables that are produced by P4 on the switch.

`flowCounter.py` - This file contains utility functions that count the number of flows and get the true k heavy hitters when given csv file of packet headers.

`utils.py` - Contains utility functions

The `p4_code` folder contains all of the code relevant to our reproduction of the HashPipe algorithm in P4. See the README in that folder for more information.
