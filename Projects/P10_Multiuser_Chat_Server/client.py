import socket
import sys

def run_chat(name, host, port):
    client_socket = socket.socket()

    server = (host, port)
    client_socket.connect(server)

    while True:
        hello_request = f"{name}\r\n"
        client_socket.send(hello_request.encode("ISO-8859-1"))

        data = client_socket.recv(4096)
        server_response = data.decode("ISO-8859-1")
        print(server_response)

        if not server_response:
            break
        client_socket.close()

#main sending thread
    #read keyboard input
    #send chat messages from user to the server

#receive thread 
    #receive packets from the server
    #display those results on-screen

def main(argv):
    name = argv[1]
    host = argv[2]
    port = int(argv[3])
    run_chat(name, host, port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))