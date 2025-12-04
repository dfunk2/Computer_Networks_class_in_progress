import socket 
import sys
import select


#accept multiple connections sent from multiple clients to a default port
#use select to be the accountent of whos in the chat
#need a buffer per connection to store chat data and be able to send out

def run_server(port):
    s_socket = socket.socket()
    s_socket.bind(('', port))

    chat_connections = set()
    wlist = set()
    xlist = set()
    s_socket.listen()
    chat_connections.add(s_socket)
    message_buffer = {}

    while True:
        ready_to_read, _, _ = select.select(chat_connections, wlist, xlist)
        for s in ready_to_read:
            if s == s_socket:
                new_socket, new_socket_info = s_socket.accept()
                chat_connections.add(new_socket)
                host, port = new_socket.getpeername()
                print(f"({host}, {port}): connected")
            else:
                data = s.recv(4096)
                client_message = data.decode('ISO-8859-1')
                message_buffer[host] = client_message.replace("\r\n", "")
                # print("key:", host, "message:", message_buffer[host])

                if client_message.endswith("\r\n"):
                    welcome_message = f"Welcome {client_message}"
                    new_socket.send(welcome_message.encode("ISO-8859-1"))
                    new_socket.close()
                    chat_connections.remove(s)
            print(f"({host}, {port}): disconnected")
            print(message_buffer)
                

def main(argv):
    port = int(argv[1])
    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))