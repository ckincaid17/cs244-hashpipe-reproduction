#!/bin/bash

import pdb
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flowCounter import FlowCounter
from hashPipeSimulator import Simulator

datacenter_file = 'data/header_fields_DC.csv'
ISP_file = 'data/header_fields_ISP_16.csv'

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

# Values of k for figure 6
kVals = range(0, 160)

# Values for m in figure 6
mVal_fig6_ISP = [3000]
mVal_fig6_DC = [300]

def findFalseNegativePercent(simulator, trueHeavyHitters, totalFlows, k):
  
  simulatedHeavyHitters = simulator.getHeavyHitters(k)

  falsePositives = len(simulatedHeavyHitters - trueHeavyHitters)
  falseNegatives = len(trueHeavyHitters - simulatedHeavyHitters)
  print ("False positives: %d" % falsePositives)
  print ("False negatives: %d" % falseNegatives)

  falsePositiveRate = float(falsePositives) / float(totalFlows - k)
  falseNegativeRate = float(falseNegatives) / float(k)

  print ("False positive rate: %f" % falsePositiveRate)
  print ("False negative rate: %f" % falseNegativeRate)

  return falseNegativeRate

def findFalseNegativePercentByK(inputFile, trueCounter, d, m):
  falseNegativeRates = []

  trueHeavyHitters = trueCounter.getHeavyHitters(k)
  totalFlows = trueCounter.getNumFlows()
  simulator = Simulator(inputFile, d, m)

  for k in kVals:
    falseNegativeRates.append(100 * findFalseNegativePercent(simulator, trueHeavyHitters, totalFlows, k)

  return falseNegativeRates

def findFalseNegativePercentByD(inputFile, trueCounter, k, m):
  falseNegativeRates = []

  trueHeavyHitters = trueCounter.getHeavyHitters(k)
  totalFlows = trueCounter.getNumFlows()

  for d in dVals:
    simulator = Simulator(inputFile, d, m)
    falseNegativeRates.append(100 * findFalseNegativePercent(simulator, trueHeavyHitters, totalFlows, k)

  return falseNegativeRates

def findDupPercentage(inputFile, d, mVals):
  duplicatePercentages = []
  print ("d = %d" % d)
  for m in mVals:
    print ("m = %d" % m)
    simulator = Simulator(inputFile, d, m)
    duplicatePercentage = simulator.getDuplicatePercentage()
    
    print ("Duplicate percentage for m=%d: %f" % (m, duplicatePercentage))
    duplicatePercentages.append(100 * duplicatePercentage)

  return duplicatePercentages

def generateFigures(inputFile, dataName, configs, mVals, mVal_fig6):

  print ("Generating figures for %s data..." % dataName)

  trueCounter = FlowCounter(inputFile)
  totalFlows = trueCounter.getNumFlows()
  print ("Total flows: %d" % totalFlows)

  # Figure 2, false negatives
  print ("Finding false negatives")
  colors = ['r', 'b', 'k', 'm']
  shapes = ['s', 'o', 'D', '*']
  for i, (k, m) in enumerate(configs):
    plt.plot(dVals, findFalseNegativePercentByD(inputFile, trueCounter, k, m), color=colors[i], marker=shapes[i])

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
    plt.plot([(m / 840 * 15)/10.0 for m in mVals], findDupPercentage(inputFile, d, mVals), color=colors[i], ls=linestyles[i])

  plt.ylabel('Duplicate Entries %')
  plt.xlabel('Memory (in KB)')
  plt.legend(['d = %d' % d for d in [8, 4, 2]], loc='best')
  plt.savefig('figure_3_%s.png' % dataName)
  plt.close()

  # Figure 6, which heavy hitters are missed
  print ("Finding false negatives against varying k")
  colors = ['r', 'k', 'c']
  linestyles = ['--', '-.', ':']
  for i, m in enumerate(mVal_fig6):
    plt.plot(kVals, findFalseNegativePercentByK(inputFile, trueCounter, 4, m), color=colors[i], ls=linestyles[i])

  plt.ylabel('False negative %')
  plt.xlabel('Number of heavy hitters (k)')
  plt.legend(['m = %d' % m for m in mVal_fig6], loc='best')
  plt.savefig('figure_6_%s.png' % dataName)
  plt.close()


def main():
  generateFigures(ISP_file, "ISP_2016", configs_ISP, mVals_ISP)
  generateFigures(datacenter_file, "DC", configs_DC, mVals_DC)
  print ("All done!")
  
  
if __name__ == '__main__':
  main()