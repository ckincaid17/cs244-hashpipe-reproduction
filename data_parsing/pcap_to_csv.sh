tshark -r equinix-chicago.dirA.20160121-125911.UTC.anon.pcap.gz -T fields -E separator=, -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport > header_fields.csv
# "-E" for header printing options
# "-G fields" format might be nice
# need to compile TShark with zlib
# zlib: install from zlib.net, cd into downloaded folder, run ./configure; make test and check that it is okay, run sudo make install
