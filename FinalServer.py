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
    commands = ["REG","UNR","QUO"]

    while True:
        data, addr = sock.recvfrom(512) 				# buffer size is 512 bytes
        frameArray = data.split(",")					#break up string on delimiter
        username =  frameArray[1]						#username is equal to the second delimited string
        username = username[:-1]						#username still includes a semicolon, strip that away

        if frameArray[0] not in commands:
        	sock.sendto("INC;", addr)

        if frameArray[0] == "REG":						#if first delimited string is REGister
            print "Register"
            print "fA[1]: ", frameArray[1]
            print "username: ", username
            if username in userList:					#if username already exists
                print "username exists"
                sock.sendto("UAE;", addr)				#send UserAlreadyExists UAE;
            else:
                userList.append(username)				#otherwise add username
                print "username added"
                sock.sendto("ROK;", addr)				#and then send Request OK
        elif frameArray[0] == "URG":
            print "Unregister"
            if username in userList:					#if user exists
                userList.remove(username)
                sock.sendto("ROK;", addr)
            else:
                userList.append(username)				#otherwise add username
                print "username added"
                sock.sendto("UNR;", addr)				#and then send Request OK
        elif frameArray[0] == "QUO":
            print "Quotes"


        #Send outBuffer using client code
            
        print "received message:", data

main()
