Instructions on how to run P4 Code:

The following instructions are modified from https://github.com/p4lang/tutorials/tree/master/examples:

## Obtaining required software

You will need to clone 2 p4lang Github repositories and install their dependencies. To clone the repositories:

`git clone https://github.com/p4lang/behavioral-model.git bmv2`
`git clone https://github.com/p4lang/p4c-bm.git p4c-bmv2`

The first repository (bmv2) is the second version of the behavioral model. It is a C++ software switch that will behave according to your P4 program. The second repository (p4c-bmv2) is the compiler for the behavioral model: it takes P4 program and output a JSON file which can be loaded by the behavioral model.

Each of these repositories come with dependencies. `p4c-bmv2` is a Python repository and installing the required Python dependencies is very easy to do using `pip`: `sudo pip install -r requirements.txt`.

bmv2 is a C++ repository and has more external dependencies. They are listed in the README. If you are running Ubuntu 14.04+, the dependencies should be easy to install (you can use the `install_deps.sh` script that comes with `bmv2`). Do not forget to build the code once all the dependencies have been installed:

`./autogen.sh`
`./configure`
`make`

## Before starting the exercises

You need to tell us where you cloned the `bmv2` and `p4c-bm` repositories :). Please update the values of the shell variables `BMV2_PATH` and `P4C_BM_PATH` in the `env.sh` file - located in the directory `p4_code` (this directory). Note that if you cloned both repositories in the same directory as this one (cs244-hashpipe-reproduction), you will not need to change the value of the variables.

You will also need to run the veth_setup.sh script included in this directory as sudo to setup the veth interfaces needed by the switch.

That's all :)