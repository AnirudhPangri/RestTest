import socket
import ssl
from urllib import parse
import sys
import logging


def execute_API_Call(self, request_method, port, request_path, hostname, query_params_dict, headers, request_body):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = ssl.wrap_socket(s)
        logging.info("Socket successfully created")
    except socket.error as err:
        logging.error("socket creation failed with error: " + str(err))

    try:
        host_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        print("Error while resolving the host.")
        sys.exit()

    # todo: manage headers and request body.
    # todo: encrypt socket.

    s.connect((host_ip, port))
    logging.info("The socket has successfully connected to macaddress.io on port 443")
    query_params = parse.urlencode(query_params_dict)
    if query_params:
        request_path = request_path + '?' + query_params

    logging.info("request path: " + request_path)
    request = "{} {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(request_method, request_path, hostname)
    s.sendall(bytes(request, encoding='utf-8'))
    response_string = str(s.recv(4096), 'utf-8')
    s.close()

    return response_string

