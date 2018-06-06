#!/bin/bash

import pdb
import matplotlib.pyplot as plt
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

inputFile = 'header_fields.csv'
configs = [(140, 3360), (210, 5040), (350, 6720), (420, 8400)]
dVals = range(2, 9)

trueCounter = FlowCounter(inputFile)
totalFlows = trueCounter.getNumFlows()

def simulateOneConfiguration(k, m):
  global trueCounter
  global totalFlows

  falseNegativeRates = []

  trueHeavyHitters = set(trueCounter.getHeavyHitters(k))

  for d in dVals:
    simulator = Simulator(inputFile, d, m)
    simulatedHeavyHitters = set(simulator.getHeavyHitters(k))

    truePositives = len(simulatedHeavyHitters & trueHeavyHitters)
    falsePositives = len(simulatedHeavyHitters) - truePositives
    falseNegatives = len(trueHeavyHitters) - truePositives
    trueNegatives = totalFlows - len(trueHeavyHitters) - falsePositives 

    falsePositiveRate = float(falsePositives) / float(falsePositives + trueNegatives)
    falseNegativeRate = float(falseNegatives) / float(falseNegatives + truePositives)

    falseNegativeRates.append(100 * falseNegativeRate)
  return falseNegativeRates

def main():
  for (k, m) in configs:
    plt.plot(dVals, simulateOneConfiguration(k, m))

  plt.ylabel('False Negative %')
  plt.xlabel('Number of table stages (d)')
  plt.legend(['k = %d, m = %d' % (k, m) for (k, m) in configs], loc='best')
  plt.show()

  plt.savefig('figure_2.png')

if __name__ == '__main__':
  main()