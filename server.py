import socket
import sys

global server_on
server_on = True

def main():
    global server_on
    host = "" # '127.0.0.1'
    port = 7777

    sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Prevent the socket from being stuck in the TIME_WAIT state.
    sockfd.bind((host, port))

    print "Server Started"
    while server_on:
        print("While loop started")
        data, address = sockfd.recvfrom(2048)
        print("Data received from : ") + str(address) + " :"
        print str(data)
        data_received_message = "Data received by server : " + str(data)
        sockfd.sendto(data_received_message, address)
        if data == "endprocess":
            server_on = False #terminate the server
    sockfd.close()

if __name__ == '__main__':
    main()
