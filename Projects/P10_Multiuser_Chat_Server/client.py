import socket
import sys
import threading
import json
from chatui import init_windows, read_command, print_message, end_windows

def make_packet(json_str):
    payload_bytes = json_str.encode('utf-8')
    len_bytes = len(payload_bytes).to_bytes(2, 'big')
    complete_packet = len_bytes + payload_bytes
    return complete_packet

def check_packet_complete(buffer):
    if len(buffer) < 2:
        return False
    if len(buffer) >= 2:
        payload_len = int.from_bytes(buffer[:2], 'big')
        full_packet_len = len(buffer) + payload_len
        return full_packet_len
    
def get_next_packet(buffer):
    header_len = len(buffer[:2])
    payload_len = int.from_bytes(buffer[:2], 'big')
    total_len = header_len + payload_len

    payload_bytes = buffer[2:total_len]
    remaining_buffer = buffer[total_len:]
    payload_str = payload_bytes.decode('utf-8')

    return payload_str, remaining_buffer
    
#receiving thread 
def run_chat(name, client_socket):
    client_buffer = bytearray()
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        client_buffer += data

        while check_packet_complete(client_buffer):
            complete_packet, client_buffer = get_next_packet(client_buffer)
            print_message(complete_packet)
      
#main sending thread
def main(argv):
    init_windows()
    #initialize chat
    if argv: 
        name = argv[1]
        host = argv[2]
        port = int(argv[3])

        client_socket = socket.socket()
        server = (host, port)
        client_socket.connect(server)

        #begin chat with a hello and join packet
        data = {"type": "hello",
                        "nick": f"{name}"}
        json_hello = json.dumps(data)
        hello_packet = make_packet(json_hello)
        client_socket.sendall(hello_packet)

        data = {"type": "join",
                "nick": f"{name}"}
        json_join = json.dumps(data)
        join_packet = make_packet(json_join)
        client_socket.sendall(join_packet)

        t = threading.Thread(target=run_chat, args=(name, client_socket))
        t.start()

        #continue chat logic
        while True:
            chat = read_command(f"{name}> ")

            if chat == "/q":
                quit_data = {"type": "leave",
                             "nick": f"{name}"}
                json_quit = json.dumps(quit_data)
                quit_packet = make_packet(json_quit)

                client_socket.sendall(quit_packet)
                client_socket.close()
                end_windows()

            else: 
                chat_data = {"type": "chat",
                             "message": f"{chat}"}
                json_chat = json.dumps(chat_data)
                chat_packet = make_packet(json_chat)
                client_socket.sendall(chat_packet)

if __name__ == "__main__":
    sys.exit(main(sys.argv))