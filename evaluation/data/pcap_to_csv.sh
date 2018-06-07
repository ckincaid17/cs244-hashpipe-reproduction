tshark -r equinix-chicago.dirA.20160121-130400.UTC.anon.pcap.gz -Y "tcp" -T fields -E separator=, -e ip.src -e ip.dst -e ip.proto -e tcp.srcport -e tcp.dstport >> header_fields.csv
# TODO filter out non-TCP packets
# "-E" for header printing options
# "-G fields" format might be nice
# need to compile TShark with zlib
# zlib: install from zlib.net, cd into downloaded folder, run ./configure; make test and check that it is okay, run sudo make install
