import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 1050
#MESSAGE = "URG,znomon;"
#MESSAGE = "QUO,znomon;"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

MESSAGE = raw_input("Please enter your packet: ")

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(512) # buffer size is 512 bytes

print data
