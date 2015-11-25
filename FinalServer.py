import socket
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 1050

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))           

def main():
    userList = list()

    while True:
        data, addr = sock.recvfrom(512) # buffer size is 512 bytes
        frameArray = data.split(",")
        if frameArray[0] == "REG":
            print "Register"
            username =  frameArray[1]
            print "fA[1]: ", frameArray[1]
            username = username[:-1]
            print "username: ", username
            if username in userList:
                print "username exists"
                sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            else:
                userList.append(username)
                print "username added"
        elif frameArray[0] == "URG":
            print "Unregister"
        elif frameArray[0] == "QUO":
            print "Quotes"


        #Send outBuffer using client code
            
        print "received message:", data

main()
