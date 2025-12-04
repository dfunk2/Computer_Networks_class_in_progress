import socket
import sys
from chatui import init_windows, read_command, print_message, end_windows

#receive thread 
    #receive packets from the server
    #display those results on-screen
def run_chat(name, client_socket):
    #while True:
    data = client_socket.recv(4096)
    server_response = data.decode("ISO-8859-1")
    print("server response:", server_response)

    if not server_response:
        client_socket.close()
        end_windows

#main sending thread
    #read keyboard input
    #send chat messages from user to the server
def main(argv):
    name = argv[1]
    host = argv[2]
    port = int(argv[3])

    client_socket = socket.socket()
    server = (host, port)
    client_socket.connect(server)
    hello_request = f"{name}\r\n"
    client_socket.send(hello_request.encode("ISO-8859-1"))

    #get user input and send to server
    s = read_command(f"{name}>\r\n")
    client_socket.send(s.encode("ISO-8859-1"))

    init_windows()
    run_chat(name, client_socket)

if __name__ == "__main__":
    sys.exit(main(sys.argv))