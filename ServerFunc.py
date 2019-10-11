from ServerDB import *


class Server_Client(DBFun):
    def __init__(self, client_socket, client_addr):
        super().__init__()
        self.BUFSIZE = 1024
        self.clientSocket = client_socket
        self.clientAddr = client_addr
        self.client_login = None

    def verify_command(self):
        self.clientSocket.sendall(b'verify')
        self.client_login = self.clientSocket.recv(self.BUFSIZE)
        self.client_login = self.client_login.decode('utf-8')
        client_username, client_pw = self.client_login.split(' ')
        print('[Client] username,', client_username)
        print('[Client] password,', client_pw)
        # ----- verify the username & password ---
        verify_status = self.verify_un_pw(un=client_username, pw=client_pw)
        # -----------------------------------------
        if verify_status == 'USER_VERIFIED':
            print("[Client] %s login successed." % client_username)
        else:
            print("[Client] %s error: %s" % (client_username, verify_status))
        # return the result of this login attempt ("USER_NOT_EXIST, ", "USER_UNVERIFIED", "USER_VERIFIED")
        self.clientSocket.sendall(bytes(verify_status.encode('utf-8')))
        # ------ go back to receiveCommand
        self.receiveCommand()

    def register_command(self):
        self.clientSocket.sendall(b'register')
        self.client_login = self.clientSocket.recv(self.BUFSIZE)
        self.client_login = self.client_login.decode('utf-8')
        client_username, client_pw = self.client_login.split(' ')
        print('[Client] username,', client_username)
        print('[Client] password,', client_pw)
        reg_status = self.client_register(un=client_username, pw=client_pw)
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
            self.register_command()

