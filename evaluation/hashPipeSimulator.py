#!/bin/bash

from utils import ip2long

import numpy as np
import pdb

hashA =        [421,  199,  83, 89, 97, 101,  103,  107,  109,  113,
                127,  131,  137,  139,  149,  151,  157,  163,  167,  173,
                179,  181,  191,  193,  197,  199,  211,  223,  227,  229,
                233,  239,  241,  251,  257,  263,  269,  271,  277,  281,
                283,  293,  307,  311,  313,  317,  331,  337,  347,  349,
                353,  359,  367,  373,  379,  383,  389,  397,  401,  409,
                419,  421,  431,  433,  439,  443,  449,  457,  461,  463,
                467,  479,  487,  491,  499,  503,  509,  521,  523,  541,
                547,  557,  563,  569,  571,  577,  587,  593,  599,  601,
                1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223,
                1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291,
                1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373,
                1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451]

hashB =        [73,   3079, 617,  619,  631,  641,  643,  647,  653,  659,
                661,  673,  677,  683,  691,  701,  709,  719,  727,  733,
                739,  743,  751,  757,  761,  769,  773,  787,  797,  809,
                811,  821,  823,  827,  829,  839,  853,  857,  859,  863,
                877,  881,  883,  887,  907,  911,  919,  929,  937,  941,
                947,  953,  967,  971,  977,  983,  991,  997,  1009, 1013,
                1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
                1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151,
                1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223,
                1453, 1459, 1471, 1481, 1483, 1487, 1489, 1493, 1499, 1511,
                1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583,
                1597, 1601, 1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657]

class Simulator:

  def __init__(self, filename, d, m):
    self.d = d 
    self.slotsPerTable = m / self.d
    self.flowTables = np.zeros((self.d, self.slotsPerTable), dtype=(int,2))

    with open(filename, 'r') as f:
      for line in f:
        fields = line.split(',')
        ipSrc = fields[0]
        if len(fields) != 5 or not ipSrc:
          continue
        flowId = ip2long(ipSrc)
        carriedPacket = self.insertInFirstStage(flowId)
        # Assume stage 0 was first stage
        stage = 1
        while carriedPacket and stage < d:
          carriedPacket = self.updateRollingMinimum(carriedPacket, stage)
          stage += 1
    
    self.flowIds, self.flowCounts = np.split(self.flowTables, 2, axis=2)
    self.flowIds = self.flowIds.flatten()
    self.flowCounts = self.flowCounts.flatten()

  def flowIdHash(self, flowId, stage):
    return (hashA[stage] * flowId + hashB[stage]) % self.slotsPerTable

  def insertInFirstStage(self, flowId):
    stage = 0
    tableSlot = self.flowIdHash(flowId, stage)
    tableFlowId, tableFlowCounter = self.flowTables[stage][tableSlot]
    if tableFlowId == flowId:
      # Increment existing flow's count
      self.flowTables[stage][tableSlot][1] += 1
      return None
    # Insert the flow regardless of whether slot is occupied
    self.flowTables[stage][tableSlot] = (flowId, 1)
    # Carry the old flow if the slot was occupied
    return None if tableFlowId == 0 else (tableFlowId, tableFlowCounter)

  def updateRollingMinimum(self, carriedPacket, stage):
    flowId, flowCounter = carriedPacket
    tableSlot = self.flowIdHash(flowId, stage)
    tableFlowId, tableFlowCounter = self.flowTables[stage][tableSlot]
    if tableFlowId == flowId:
      # Increment existing flow's count
      self.flowTables[stage][tableSlot][1] += flowCounter
      return None
    elif tableFlowId == 0:
      self.flowTables[stage][tableSlot] = (flowId, flowCounter)
      return None
    if tableFlowCounter < flowCounter:
      self.flowTables[stage][tableSlot] = (flowId, flowCounter)
      return (tableFlowId, tableFlowCounter)
    else:
      return (flowId, flowCounter)

  def getHeavyHitters(self, k):
    return self.flowIds[np.argpartition(self.flowCounts, -k)[-k:]]

  def getDuplicatePercentage(self):
    uniqueFlows = set()
    for row in range(self.d):
      for col in range(self.slotsPerTable):
         flowId = self.flowTables[row][col][0]
         uniqueFlows.add(flowId)
    return 1 - (len(uniqueFlows) / float(self.d * self.slotsPerTable))
