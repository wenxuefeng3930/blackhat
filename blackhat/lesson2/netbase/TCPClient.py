import socket

target_host = "127.0.0.1"
target_port = 80
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
client.connect((target_host, target_port))
# send some data
client.send(bytes("GET / HTTP/1.1\r\nHost: cn.bing.com\r\n\r\n", "utf-8"))
# receive some data
response = client.recv(4096)
print(response)
