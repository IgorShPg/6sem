import http.server
import socket
import sys


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sockfd:
    sockfd.connect(("8.8.8.8", 80))
    print(sockfd.getsockname()[0])
http.server.test(
    HandlerClass=http.server.SimpleHTTPRequestHandler,
    port=(int(sys.argv[1]) if len(sys.argv) > 1 else 8000)
)


