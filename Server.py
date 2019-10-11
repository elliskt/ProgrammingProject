import socket
from threading import Thread
from ServerFunc import *


def deal_client(client_socket, client_addr):
    client = Server_Client(client_socket, client_addr)
    print("[Server] client accept")
    client.receiveCommand()


if __name__ == '__main__':
    # ----- server setup -----------
    serverAddr = ('127.0.0.1', 65501)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(serverAddr)  # bind for address
    serverSocket.listen(2)
    print("[Init] Server is listening......")
    # ------------------------------

    # ------- server listening --------------------
    try:
        while True:
            clientSocket, clientAddr = serverSocket.accept()
            client = Thread(target=deal_client, args=(clientSocket, clientAddr))
            client.start()
    finally:
        print("here is finally!")
        serverSocket.close()
    # -------------------------------------------
