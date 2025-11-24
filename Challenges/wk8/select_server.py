# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select
#select() purpose is it looks at a whole set of sockets and tells you which ones have data to be recv

def run_server(port):
    # create socket
    s_socket = socket.socket()
    s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind to port
    s_socket.bind(('', port))

    #connected and listening socket set
    read_set = set()
    wlist = set()
    elist = set()

    s_socket.listen()
    read_set.add(s_socket)
    print('waiting for connections')

    while True:
        # test if ready to receive data
        ready_to_read, _, _ = select.select(read_set, wlist, elist)

        for s in ready_to_read:
            if s == s_socket:
                # accept new connections
                new_socket, new_socket_addr_info = s_socket.accept()
                read_set.add(new_socket)

                #print message stating connection
                host, port = new_socket.getpeername()
                print(f'({host}, {port}): connected')
            else:
                data = s.recv(4096)
                clientRequest = data.decode("ISO-8859-1")
                print(f'({host}, {port}) {len(data)} bytes: {data}: {clientRequest}')

                if not data:
                    new_socket.close()
                    read_set.remove(s)
        print(f'({host}, {port}): disconnected')



#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
