import socket, struct

def ip2long(ip):
  """
  Convert an IP string to long
  """
  packedIP = socket.inet_aton(ip)
  return struct.unpack("!L", packedIP)[0]