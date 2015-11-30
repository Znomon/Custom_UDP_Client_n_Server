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

        if frameArray[0] not in commands:                               #if command is not in the list of acceptable commands
        	sock.sendto("INC;", addr)                               #send INvalid Command
        	continue

        if frameArray[len(frameArray)-1].endswith(';'):                 #test to make sure request from client ends in a semicolon
            if len(frameArray) < 2:
                sock.sendto("INP;", addr)
                continue
            elif len(frameArray) == 2:
                if frameArray[0] == "REG" or frameArray[0] == "UNR":
                    username = frameArray[1]				#username is equal to the second delimited string
                    username = username[:-1]				#username still includes a semicolon, strip that away
                else:
                    sock.sendto("INP;", addr)
                    continue
                print "FrameArray == 2"
            elif len(frameArray) >= 3:
                if frameArray[0] == "REG" or frameArray[0] == "UNR":
                    sock.sendto("INP;",addr)
                    continue
                username = frameArray[1]                                #if this request contains stocks, set the second field to the username
                print "FrameArray == 3"
        else:
            print "Forgot semicolon"                
            sock.sendto("INP;", addr)                                   #if request from client doesn't end in a semicolon send INP
            continue

        username = username.upper()                                     #stores all usernames as uppercase because usernames are not case sensitive
        if not(username.isalnum()) or len(username) > 32:               #if username is alpha-numeric
            print "Invalid Username sent"
            print "username length:", len(username)
            sock.sendto("INU;", addr)                                   #else send INvalid Username
            continue
		
        if frameArray[0] == "REG":					#if first delimited string is REGister
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
        elif frameArray[0] == "UNR":
            print "Unregister"
            if username in userList:					#if user exists
                userList.remove(username)
                sock.sendto("ROK;", addr)
                continue
            else:
                print "username doesnt exist, can't remove"
                sock.sendto("UNR;", addr)				#and then send Request OK
                continue
        elif frameArray[0] == "QUO":
            if username not in userList:				#if username doesnt exist
                sock.sendto("UNR;", addr)
                continue
            quotes = list()
            stockFile  = list(list())
            output = "ROK"
            for i in frameArray[2:]:
                if i.endswith(';'):
                    i = i[:-1]
                quotes.append(i)
            with open('stockfile.txt') as file:
                for index, line in enumerate(file):
                    stockFile.append(line.split(" "))
            for i in quotes:
                push = ",-1"
                for j in stockFile:
                    print "are these the same? :",j[0],": --> :",i,":" #debug
                    
                    if j[0] == i:
                        push = "," + j[1]
                output += push
            output += ";"
            sock.sendto(output, addr)
            continue

        #Send outBuffer using client code
            
        print "received message:", data

main()
