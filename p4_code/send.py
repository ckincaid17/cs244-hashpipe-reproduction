#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc. 
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from scapy.all import sniff, sendp
from scapy.all import Packet
from scapy.all import ShortField, IntField, LongField, BitField
from scapy.all import Ether, IP, TCP
import networkx as nx

import sys

def main():
  if len(sys.argv) != 1:
      print "Usage: send1.py"
      sys.exit(1)

  src, dst = 'h1', 'h2'
  srcmac = '00:aa:bb:00:00:00'
  dstmac = '00:aa:bb:00:00:01'
  port = 80
  msg = 'hi'

  # TODO: loop over csv 
  p = Ether(src=srcmac, dst=dstmac, type=0x0800) / IP(src = '197.89.8.178', dst = '1.146.110.6') / msg
  sendp(p, iface = "veth0", verbose = 0)


if __name__ == '__main__':
  main()