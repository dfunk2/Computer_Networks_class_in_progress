import socket 
import sys
import select
import json 

def make_packet(json_str):
    payload_bytes = json_str.encode('utf-8')
    len_bytes = len(payload_bytes).to_bytes(2, 'big')
    complete_packet = len_bytes + payload_bytes
    return complete_packet

def check_packet_complete(buffer):
    if len(buffer) < 2:
        return False
    payload_len = int.from_bytes(buffer[:2], 'big')
    return len(buffer) >= 2 + payload_len
    
    
def get_next_packet(buffer):
    header_len = len(buffer[:2])
    payload_len = int.from_bytes(buffer[:2], 'big')
    total_len = header_len + payload_len

    payload_bytes = buffer[2:total_len]
    remaining_buffer = buffer[total_len:]
    payload_str = payload_bytes.decode('utf-8')

    return payload_str, remaining_buffer

def broadcast(s_socket, chat_connections, message):
    for client in chat_connections:
        if client != s_socket:
            try:
                client.sendall(message)
            except BrokenPipeError:
                client.close()
                chat_connections.remove(client)

def chat_server(port):
    s_socket = socket.socket()
    s_socket.bind(('', port))

    chat_connections = set()
    wlist = set()
    xlist = set()
    s_socket.listen()
    chat_connections.add(s_socket)
    nick_dict = {}
    client_buffers = {}

    while True:
        ready_to_read, _, _ = select.select(chat_connections, wlist, xlist)
        for s in ready_to_read:
            if s == s_socket:
                new_socket, new_socket_addr = s_socket.accept()
                chat_connections.add(new_socket)
                client_buffers[new_socket] = bytearray()
            else:
                data = s.recv(4096)
                if not data:
                    continue
                client_buffers[s] += data

                while check_packet_complete(client_buffers[s]):
                    packet, client_buffers[s] = get_next_packet(client_buffers[s])
                    packet_dict = json.loads(packet)
                
                    if packet_dict['type'] == 'hello':
                        nick_dict[s] = packet_dict['nick']

                    if packet_dict['type'] == 'join':
                        hello_str = (f"*** {nick_dict[s]} has joined the chat")
                        hello_response = make_packet(json.dumps(hello_str))
                        broadcast(s_socket, chat_connections, hello_response)

                    if packet_dict['type'] == 'chat':
                        chat_str = f"{nick_dict[s]}: {packet_dict['message']}"
                        chat_response = make_packet(json.dumps(chat_str))
                        broadcast(s_socket, chat_connections, chat_response)
                        
                    if packet_dict['type'] == 'leave':
                        quit_str = f"*** {nick_dict[s]} has left the chat"
                        quit_response = make_packet(json.dumps(quit_str))
                        chat_connections.remove(s)
                        s.close()
                        broadcast(s_socket, chat_connections, quit_response)
                        
                        
def main(argv):
    port = int(argv[1])
    chat_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))