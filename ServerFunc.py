from db import *


class bikeSharingServer(database):
    def __init__(self, client_socket, client_addr):
        super().__init__()
        self.BUFSIZE = 1024
        self.clientSocket = client_socket
        self.clientAddr = client_addr
        # self.client_login = None

    # Deprecated
    # def verify_command(self):
    #     self.clientSocket.sendall(b'verify')
    #     self.client_login = self.clientSocket.recv(self.BUFSIZE)
    #     self.client_login = self.client_login.decode('utf-8')
    #     mobile, pswd = self.client_login.split(' ')
    #     print('[Client] username,', mobile)
    #     print('[Client] password,', pswd)
    #     # ----- verify the username & password ---
    #     verify_status = self.verify_un_pw(un=mobile, pw=pswd)
    #     # -----------------------------------------
    #     if verify_status == 'USER_VERIFIED':
    #         print("[Client] %s login successed." % mobile)
    #     else:
    #         print("[Client] %s error: %s" % (mobile, verify_status))
    #     # return the result of this login attempt ("USER_NOT_EXIST, ", "USER_UNVERIFIED", "USER_VERIFIED")
    #     self.clientSocket.sendall(bytes(verify_status.encode('utf-8')))
    #     # ------ go back to receiveCommand
    #     self.receiveCommand()

    def registerUser(self):
        self.clientSocket.sendall(b'register')
        self.client_login = self.clientSocket.recv(self.BUFSIZE)
        self.client_login = self.client_login.decode('utf-8')
        mobile, pswd = self.client_login.split(' ')
        print('[Client] Username: ', mobile)
        print('[Client] Password: ', pswd)
        reg_status = self.addUser(str(mobile), pswd, "Mohammad Alharbi", 1)
        self.clientSocket.sendall(bytes(reg_status.encode('utf-8')))        # result of register attempt
        # ------ go back to receiveCommand
        self.receiveCommand()

    def receiveCommand(self):
        client_command = self.clientSocket.recv(self.BUFSIZE)
        client_command = client_command.decode('utf-8')
        print("[Server] received command: ", client_command)
        if client_command == 'verify_login':
            self.verify_command()
        elif client_command == 'register':
            self.registerUser()

