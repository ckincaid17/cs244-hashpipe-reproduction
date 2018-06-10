tshark -r pcap_file -Y "tcp" -T fields -E separator=, -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport >> header_fields_DC.csv
