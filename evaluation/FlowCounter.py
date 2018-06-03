#!/bin/bash

from collections import Counter
import sys
import pdb
import socket, struct

def ip2long(ip):
  """
  Convert an IP string to long
  """
  packedIP = socket.inet_aton(ip)
  return struct.unpack("!L", packedIP)[0]

class FlowCounter:

  def __init__(self, filename):
    # TODO add param for filename
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
    return [flow for (flow, count) in self.counts.most_common(k)]
