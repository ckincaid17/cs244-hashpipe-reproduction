Instructions on how to run P4 Code:

## Obtaining required software

The following instructions are modified from https://github.com/p4lang/tutorials/tree/master/examples:

You will need to clone 2 p4lang Github repositories and install their dependencies. To clone the repositories:

`git clone https://github.com/p4lang/behavioral-model.git bmv2`
`git clone https://github.com/p4lang/p4c-bm.git p4c-bmv2`

The first repository (bmv2) is the second version of the behavioral model. It is a C++ software switch that will behave according to your P4 program. The second repository (p4c-bmv2) is the compiler for the behavioral model: it takes P4 program and output a JSON file which can be loaded by the behavioral model.

Each of these repositories come with dependencies. `p4c-bmv2` is a Python repository and installing the required Python dependencies is very easy to do using `pip`: `sudo pip install -r requirements.txt`.

bmv2 is a C++ repository and has more external dependencies. They are listed in the README. If you are running Ubuntu 14.04+, the dependencies should be easy to install (you can use the `install_deps.sh` script that comes with `bmv2`). Do not forget to build the code once all the dependencies have been installed:

`./autogen.sh`
`./configure`
`make`

## Before running our code

You need to tell P4 where you cloned the `bmv2` and `p4c-bm` repositories :). Please update the values of the shell variables `BMV2_PATH` and `P4C_BM_PATH` in the `env.sh` file - located in the directory `p4_code` (this directory). Note that if you cloned both repositories in the same directory as this outer one (cs244-hashpipe-reproduction), you will not need to change the value of the variables.

You will also need to run the veth_setup.sh script included in this directory as sudo to setup the veth interfaces needed by the switch.

## Custom hash functions

The HashPipe algorithm requires custom hash functions that use different unique primes for each stage, so that the same flow can be hashed to multiple slots in the hash table in multiple stages. Adding these hash functions to the behavioral model is simple but is necessary before running our code. Copy the hash functions we provide in the hash_functions.cpp file to this file in the bmv2 repository: https://github.com/p4lang/behavioral-model/blob/master/targets/simple_switch/simple_switch.cpp. They go on line 34 above other example custom hash functions. Once doing this remake `bmv2`.

That's all for setup :)

## Description of files

Much of this code was based on or directly taken from Vibhaalakshmi Sivaraman's original implementation of this algorithm. Her P4 code can be found here: https://github.com/vibhaa/iw15-heavyhitters/tree/master/p4v1_1/. We tried to rewrite the algorithm in P4 with her code as a reference.

`p4src` contains the actual p4 code. `simple_router.p4` is taken from the P4 language's example code with 
`apply(track_stage1);`
`apply(track_stage2);`
added to the ingress control. These actions are described in `hashpipe.p4` where the actual algorithm to update the flow trackers and packet counters is written.

The other files in this folder help perform a demo on the P4 behavioral model. `send.py` sends packets from a csv trace through the switch. `receive.py` handles receiving the packets. `run_demo.sh` compiles our P4 code for the behavioral model and runs it, so that when it's ready we can send and receive packets. `read_registers.sh` prints out the values in the flow tracker and packet counter registers for each stage so that they can be compared against the simulator.

## Running our code






