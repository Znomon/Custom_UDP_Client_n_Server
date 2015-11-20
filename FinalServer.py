import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 1050

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(512) # buffer size is 512 bytes
    frameArray = data.split(",")
    if frameArray[0] == "REG":
        #print "Register"
        username =  frameArray[1]
        #print "fA[1]: ", frameArray[1]
        username = username[:-1]
        #print "username: ", username
        with open('username.txt', 'a') as file:
            file.write(username,"\n")
    elif frameArray[0] == "URG":
        print "Unregister"
    elif frameArray[0] == "QUO":
        print "Quotes"
    
    print "received message:", data
