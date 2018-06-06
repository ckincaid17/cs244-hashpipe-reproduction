#!/bin/bash

import pdb
import matplotlib.pyplot as plt
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

inputFile = 'data/header_fields.csv'
configs = [(140, 3360), (210, 5040), (350, 6720), (420, 8400)]
dVals = range(2, 9)
mVals = [840 * i for i in range(1, 6)]

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

def findDupPercentage(d):
  duplicatePercentages = []
  for m in mVals:
    simulator = Simulator(inputFile, d, m)
    duplicatePercentages.append(simulator.getDuplicatePercentage())
  return duplicatePercentages

def main():
  colors = ['r', 'b', 'k', 'm']
  shapes = ['s', 'o', 'D', '*']
  for i, (k, m) in enumerate(configs):
    plt.plot(dVals, simulateOneConfiguration(k, m), color=colors[i], marker=shapes[i])

  plt.ylabel('False Negative %')
  plt.xlabel('Number of table stages (d)')
  plt.legend(['k = %d, m = %d' % (k, m) for (k, m) in configs], loc='best')

  plt.savefig('figure_2.png')
  plt.close()

  colors = ['r', 'k', 'c']
  linestyles = ['--', '-.', ':']
  for i, d in enumerate([2, 4, 8]):
    plt.plot([m / 840 * 15000 for m in mVals], findDupPercentage(d), color=colors[i], ls=linestyles[i])

  plt.ylabel('Duplicate Entries %')
  plt.xlabel('Memory (in KB)')
  plt.legend(['d = %d' % d for d in [2, 4, 8]], loc='best')

  plt.savefig('figure_3.png')

if __name__ == '__main__':
  main()