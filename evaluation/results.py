#!/bin/bash

import pdb
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

inputFile = 'data/header_fields_DC.csv'
# configs = [(140, 3360), (210, 5040), (350, 6720), (420, 8400)]
configs = [(40, 840)]

dVals = range(2, 9)
mVals = [840 * i for i in range(1, 6)]

trueCounter = FlowCounter(inputFile)
totalFlows = trueCounter.getNumFlows()

def simulateOneConfiguration(k, m):
  global trueCounter
  global totalFlows

  falseNegativeRates = []

  trueHeavyHitters = trueCounter.getHeavyHitters(k)

  for d in dVals:
    simulator = Simulator(inputFile, d, m)
    simulatedHeavyHitters = simulator.getHeavyHitters(k)

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

def findDupPercentage(d):
  duplicatePercentages = []
  print ("d = %d" % d)
  for m in mVals:
    print ("m axis = %d" % ((m / 840 * 15)/10.0))
    m = m/10
    print ("m = %d" % m)
    simulator = Simulator(inputFile, d, m)
    duplicatePercentage = simulator.getDuplicatePercentage()
    duplicatePercentages.append(100 * duplicatePercentage)
    print ("Duplicate percentage for m=%d: %f" % (m, duplicatePercentage))
  return duplicatePercentages

def main():
  print ("Total flows: %d" % totalFlows)

  # Figure 2, false negatives
  print ("Finding false negatives")
  colors = ['r', 'b', 'k', 'm']
  shapes = ['s', 'o', 'D', '*']
  for i, (k, m) in enumerate(configs):
    plt.plot(dVals, simulateOneConfiguration(k, m), color=colors[i], marker=shapes[i])

  plt.ylabel('False Negative %')
  plt.xlabel('Number of table stages (d)')
  plt.legend(['k = %d, m = %d' % (k, m) for (k, m) in configs], loc='best')

  plt.savefig('figure_2_DC.png')
  plt.close()

  # Figure 3, duplicates
  # print ("Finding duplicates")
  # colors = ['r', 'k', 'c']
  # linestyles = ['--', '-.', ':']
  # for i, d in enumerate([8, 4, 2]):
  #   plt.plot([(m / 840 * 15)/10.0 for m in mVals], findDupPercentage(d), color=colors[i], ls=linestyles[i])

  # plt.ylabel('Duplicate Entries %')
  # plt.xlabel('Memory (in KB)')
  # plt.legend(['d = %d' % d for d in [8, 4, 2]], loc='best')

  # plt.savefig('figure_3_DC.png')

if __name__ == '__main__':
  main()