#!/bin/bash
import numpy as np
import sys
import pdb

import socket, struct

def ip2long(ip):
    """
    Convert an IP string to long
    """
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

def main():
  flowCounts = {}

  with open('header_fields.csv', 'r') as f:
    for line in f:
      fields = line.split(',')
      if len(fields) != 5:
        continue
      # # Don't let multiplying by a prime cause overflow
      # numPreservedHashBits = sys.getsizeof(int()) - 12
      # hashMask = (1 << numPreservedHashBits) - 1
      # flowId = hash(tuple(fields)) & hashMask
      # flowId = hash(tuple(fields))
      flowId = ip2long(fields[0])
      if flowId in flowCounts:
        flowCounts[flowId] += 1
      else:
        flowCounts[flowId] = 1
  
  heavyHitters = {key: value for (key, value) in flowCounts.items() if value > 1000}
  print(heavyHitters)
  pdb.set_trace() 

if __name__ == '__main__':
  main()