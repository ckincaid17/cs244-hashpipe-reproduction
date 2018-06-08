#!/bin/bash

import pdb
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

datacenter_file = 'data/header_fields_DC.csv'
ISP_file = 'data/header_fields_ISP_2016.csv'

# Values of (k, m) where k is number of heavy hitters and m is the total
# number of slots in the hashtable to test on each dataset
configs_ISP = [(140, 3360), (210, 5040), (350, 6720), (420, 8400)]
configs_DC = [(40, 840)]

# Number of stages in the hash table to test on
dVals = range(2, 9)

# Values of m where m is the total number of slots in the hashtable
# to test for % of duplicates on each dataset
mVals_ISP = [840 * i for i in range(1, 6)]
mVals_DC = [84 * i for i in range(1, 6)]

def simulateOneConfiguration(inputFile, k, m):
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

def findDupPercentage(inputFile, d, mVals):
  duplicatePercentages = []
  print ("d = %d" % d)
  for m in mVals:
    print ("m = %d" % m)
    simulator = Simulator(inputFile, d, m)
    duplicatePercentage = simulator.getDuplicatePercentage()
    duplicatePercentages.append(100 * duplicatePercentage)
    print ("Duplicate percentage for m=%d: %f" % (m, duplicatePercentage))
  return duplicatePercentages

def generateFigures(inputFile, dataName, configs, mVals):

  print ("Generating figures for %s data..." % dataName)

  trueCounter = FlowCounter(inputFile)
  totalFlows = trueCounter.getNumFlows()
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

  plt.savefig('figure_2_%s.png' % dataName)
  plt.close()

  # Figure 3, duplicates
  print ("Finding duplicates")
  colors = ['r', 'k', 'c']
  linestyles = ['--', '-.', ':']
  for i, d in enumerate([8, 4, 2]):
    plt.plot([(m / 840 * 15)/10.0 for m in mVals], findDupPercentage(d, mVals), color=colors[i], ls=linestyles[i])

  plt.ylabel('Duplicate Entries %')
  plt.xlabel('Memory (in KB)')
  plt.legend(['d = %d' % d for d in [8, 4, 2]], loc='best')

  plt.savefig('figure_3_%s.png' % dataName)

def main():
  generateFigures(ISP_file, "ISP_2016", configs_ISP, mVals_ISP)
  generateFigures(datacenter_file, "DC", configs_DC, mVals_DC)
  print ("All done!")
  
  
if __name__ == '__main__':
  main()