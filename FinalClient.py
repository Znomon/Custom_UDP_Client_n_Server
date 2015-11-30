import socket
import time #Needed for sleep command

UDP_IP = "66.158.200.153"
UDP_PORT = 1050
#MESSAGE = "URG,znomon;"
#MESSAGE = "QUO,znomon;"

quoList = list() #List to remember stock values
quoBool = None #Boolean value testing if user sends QUO or not
servStock = list() #List to hold only the value of stocks

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

while 1:
    
    MESSAGE = raw_input("Please enter your packet: ")

    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

    while 1: #Try to resend packet every 5 seconds if it gets lost
        try: 
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            print "packet sent"
            data, addr = sock.recvfrom(512) # buffer size is 512 bytes
            if data: #If successfully sends break from loop
                break
            time.sleep(5) #Wait five seconds
        except ValueError:
            print "Resending Packet..."

    print data;
    
    if "QUO" in MESSAGE: #Store the stocks user asks for in a list
        MESSAGE = MESSAGE[:-1] #Remove ; at end of string
        quoList = MESSAGE.split(",")
        del quoList[0] #Delete QUO 
        del quoList[0] #Delete the username
        quoBool = True

    if quoBool: #Only do this when user sends QUO command
        data = data[:-1] #Remove ; at end of string
        servStock = data.split(",") #Break up string by delimeter
        if servStock[0] == "ROK":
            del servStock[0] #Remove the ROK to only get values
            for i in range(len(servStock)):
                 print quoList[i], servStock[i] #Prints prices for debugging
