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


    # -------------------------------


# def client_login(un, pw):
#     clientSocket.sendall(bytes(''.encode('utf-8')))
#     clientSocket.sendall(bytes(un.encode('utf-8')))
#     clientSocket.sendall(bytes(pw.encode('utf-8')))
#     login_state = clientSocket.recv(BUFSIZE)
#
#     if login_state == "USER_NOT_EXIST":
#         register_label = Label(text="The user not exists!")
#         register_label.place(x=150, y=220)
#         register_label.configure(fg="red")
#     elif login_state == 'USER_UNVERIFIED':
#         register_label = Label(text="The user and password don't match!")
#         register_label.place(x=150, y=220)
#         register_label.configure(fg="red")
#     elif login_state == 'USER_VERIFIED':
#         map_window()


# ------ client communicate with server -------
# while True:
#     try:
#         state = clientSocket.recv(BUFSIZE)
#         state_content = state.decode('utf-8')
#         if state_content == 'verify':
#             username = input("Username: ")
#             clientSocket.sendall(bytes(username.encode('utf-8')))
#             password = input("Password: ")
#             clientSocket.sendall(bytes(password.encode('utf-8')))
#         else:
#             print(state_content)
#             command = input("something need to do: ")
#             clientSocket.sendall(bytes(command.encode('utf-8')))
#     # ---------deal with the server error --------
#     except ConnectionError:
#         clientSocket.close()
#         print("[Server] Server error, please try again.")
#     except OSError:
#         clientSocket.close()
#         print("[Server] OS error.")
#     # -----------------------------------------------
