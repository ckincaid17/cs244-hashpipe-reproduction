#!/bin/bash

from collections import Counter
from utils import ip2long

import pdb

class FlowCounter:

  def __init__(self, filename):
    self.counts = Counter()
    with open(filename, 'r') as f:
      for line in f:
        fields = line.split(',')
        ipSrc = fields[0]
        if len(fields) != 5 or not ipSrc:
          continue
        flowId = ip2long(ipSrc)
        self.counts[flowId] += 1

  def getNumFlows(self):
    return len(self.counts)   

  def getHeavyHitters(self, k):
    return set([flow for (flow, count) in self.counts.most_common(k)])
