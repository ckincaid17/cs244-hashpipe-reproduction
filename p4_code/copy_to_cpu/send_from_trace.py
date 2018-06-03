from scapy.all import *

with open('header_fields.csv', 'r') as f:
  counter = 0
  for line in f:
    fields = line.split(',')
    if len(fields) != 5:
      continue
    p = Ether() / IP(src=fields[0], dst=fields[1]) / TCP(src=fields[3], dst=fields[4]) / "packet %d" % counter
    counter = counter + 1
    # p.show()
    hexdump(p)
    sendp(p, iface = "veth1")
