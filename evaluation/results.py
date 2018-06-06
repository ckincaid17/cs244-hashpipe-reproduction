#!/bin/bash

import pdb
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

inputFile = 'data/header_fields.csv'
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

    falsePositives = len(simulatedHeavyHitters - trueHeavyHitters)
    falseNegatives = len(trueHeavyHitters - simulatedHeavyHitters)
    print ("False positives: %d" % falsePositives)
    print ("False negatives: %d" % falseNegatives)

    falsePositiveRate = float(falsePositives) / float(totalFlows - k)
    falseNegativeRate = float(falseNegatives) / float(k)

    print ("False positive rate: %f" % falsePositiveRate)
    print ("False negative rate: %f" % falseNegativeRate)

    falseNegativeRates.append(100 * falseNegativeRate)
  return falseNegativeRates

def main():
  print ("Total flows: %d" % totalFlows)

  for (k, m) in configs:
    print ("Heavy hitters: %d" % len(trueCounter.getHeavyHitters(k)))
    plt.plot(dVals, simulateOneConfiguration(k, m))

  plt.ylabel('False Negative %')
  plt.xlabel('Number of table stages (d)')
  plt.legend(['k = %d, m = %d' % (k, m) for (k, m) in configs], loc='best')
  # plt.show()

  plt.savefig('figure_2.png')

if __name__ == '__main__':
  main()