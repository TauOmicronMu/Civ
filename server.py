import socket
import sys

global server_on
server_on = True

def main():
    global server_on
    host = '127.0.0.1'
    port = 7777

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print "Server Started"
    while server_on:
        print("While loop started")
        data, address = s.recvfrom(1024)
        print("Data received from : ") + str(address) + " :"
        print str(data)
        data_received_message = "Data received by server : " + str(data)
        s.sendto(data_received_message, address)
        if data == "endprocess":
            server_on = False #terminate the server
    s.close()

if __name__ == '__main__':
    main()
