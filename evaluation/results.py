#!/bin/bash

import pdb
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

k = 8
d = 6
memorySize = 600
inputFile = 'header_fields.csv'

trueCounter = FlowCounter(inputFile)
totalFlows = trueCounter.getNumFlows()
trueHeavyHitters = set(trueCounter.getHeavyHitters(k))

simulator = Simulator(inputFile, d, memorySize)
simulatedHeavyHitters = set(simulator.getHeavyHitters(k))

# pdb.set_trace()

truePositives = len(simulatedHeavyHitters & trueHeavyHitters)
falsePositives = len(simulatedHeavyHitters) - truePositives
falseNegatives = len(trueHeavyHitters) - truePositives
trueNegatives = totalFlows - len(trueHeavyHitters) - falsePositives 

falsePositiveRate = float(falsePositives) / float(falsePositives + trueNegatives)
falseNegativeRate = float(falseNegatives) / float(falseNegatives + truePositives)

print falsePositiveRate
print falseNegativeRate