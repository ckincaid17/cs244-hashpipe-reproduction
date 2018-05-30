#!/bin/bash

import pdb

totalFlows = 32122

trueFlows = set()
with open('heavy_hitters_true.csv', 'r') as f:
    for line in f:
        for flow in line.split(','):
            trueFlows.add(flow )

simulatedFlows = set()
with open('heavy_hitters_simulated.csv', 'r') as f:
    for line in f:
        for flow in line.split(','):
            simulatedFlows.add(flow)

# pdb.set_trace()

truePositives = len(simulatedFlows & trueFlows)
falsePositives = len(simulatedFlows) - truePositives
falseNegatives = len(trueFlows) - truePositives
trueNegatives = totalFlows - (8 - falseNegatives) 

falsePositiveRate = float(falsePositives) / float(falsePositives + trueNegatives)
falseNegativeRate = float(falseNegatives) / float(falseNegatives + truePositives)
print falsePositiveRate
print falseNegativeRate