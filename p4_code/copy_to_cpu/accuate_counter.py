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

def main():
  flowCounts = Counter()

  with open('header_fields.csv', 'r') as f:
    for line in f:
      fields = line.split(',')
      ipSrc = fields[0]
      if len(fields) != 5 or not ipSrc:
        continue
      flowId = ip2long(ipSrc)
      flowCounts[flowId] += 1

  print len(flowCounts)

  k = 8
  heavyHitters = [flow for (flow, count) in flowCounts.most_common(k)]
  print(heavyHitters)

  # Change to append mode when dealing with multiple files
  with open('heavy_hitters_true.csv', 'w') as f:
    f.write(','.join([str(flow) for flow in heavyHitters]))

if __name__ == '__main__':
  main()