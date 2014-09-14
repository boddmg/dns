import socket
import random
import struct


def get_dns_packet(domain):
    transact_id = random.Random().randint(0,0xffff)

    #header
    transact_id = struct.pack("H",transact_id)
    flags = b"\x01\x00"
    question_count = b"\x00\x01"
    answer_count = b"\x00\x00"
    authority_count = b"\x00\x00"
    additional_count = b"\x00\x00"

    #queries
    domain_name = domain
    domain_name_parsed = b""
    for i in domain_name.split('.'):
        domain_name_parsed += struct.pack('b',len(i))
        domain_name_parsed += i
    domain_name_parsed += b'\x00'
    domain_type = b"\x00\x01"
    domain_class = b"\x00\x01"

    dns_packet = transact_id + flags + question_count + answer_count + \
                 authority_count + additional_count + domain_name_parsed + \
                 domain_type + domain_class
    return dns_packet

def hex_to_string(hex_data):
    hex_string = ""
    for i in hex_data:
        hex_string += '{:02x}'.format(struct.unpack('B',i)[0])
    return hex_string

def dns_response_parser(dns_response):
    pass

##udp_packet = b""
##sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
if __name__ == "__main__":
    mock_hex_string = "ae660100000100000000000005626169647503636f6d0000010001"
    mock_domain = "baidu.com"
    assert( hex_to_string(get_dns_packet(mock_domain))[4:] == mock_hex_string[4:] )
    UDP_IP = "114.114.114.114"
    UDP_PORT = 53
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(get_dns_packet(mock_domain),(UDP_IP, UDP_PORT))
    response = sock.recv(1024)
    print hex_to_string(response)
