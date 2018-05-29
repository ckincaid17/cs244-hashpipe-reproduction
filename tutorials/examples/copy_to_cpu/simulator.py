#!/bin/bash
import numpy as np

def initTables(d):


main():
  d = 4
  numSlots = 6

  flowTables = np.zeros((d, numSlots), dtype=int)

  with open('header_fields.csv', 'r') as f:
  counter = 0
  for line in f:
    fields = line.split(',')
    if len(fields) != 5:
      continue
    flowId = hash(tuple(fields))
    counter = counter + 1
    # p.show()
    hexdump(p)
    sendp(p, iface = "veth1")

if __name__ == '__main__':
  main()