import socket
import time
# ----- client setup -----------
BUFSIZE = 1024
serverAddr = ('127.0.0.1', 65501)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ------------------------------


def client_connect_server():
    # ------ client connect --------
    print('Client is connecting to the server......')
    try:
        clientSocket.connect(serverAddr)                        # try connect to server
        print("[Server] Connect successful.")

    except ConnectionRefusedError:
        print("Server error, please try again")
        exit(1)


