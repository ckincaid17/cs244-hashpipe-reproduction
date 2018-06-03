#!/bin/bash

import pdb
from FlowCounter import FlowCounter

k = 8

trueCounter = FlowCounter('header_fields.csv')
totalFlows = trueCounter.getNumFlows()
trueHeavyHitters = set(trueCounter.getHeavyHitters(k))

simulatedHeavyHitters = set()
with open('heavy_hitters_simulated.csv', 'r') as f:
  for line in f:
    for flow in line.split(','):
      simulatedHeavyHitters.add(int(flow))

# pdb.set_trace()

truePositives = len(simulatedHeavyHitters & trueHeavyHitters)
falsePositives = len(simulatedHeavyHitters) - truePositives
falseNegatives = len(trueHeavyHitters) - truePositives
trueNegatives = totalFlows - len(trueHeavyHitters) - falsePositives 

falsePositiveRate = float(falsePositives) / float(falsePositives + trueNegatives)
falseNegativeRate = float(falseNegatives) / float(falseNegatives + truePositives)

print falsePositiveRate
print falseNegativeRate