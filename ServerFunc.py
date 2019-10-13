from db import *


class bikeSharingServer(database):
    def __init__(self, client_socket, client_addr):
        super().__init__()
        self.BUFSIZE = 1024
        self.clientSocket = client_socket
        self.clientAddr = client_addr
        self.client_login = None
        self.client_mobile = None

    def authenticateUser(self):
        self.clientSocket.sendall(b'verify')
        self.client_login = self.clientSocket.recv(self.BUFSIZE)
        self.client_login = self.client_login.decode('utf-8')
        self.client_mobile, pswd = self.client_login.split(' ')
        print('[Client] username,', self.client_mobile)
        print('[Client] password,', pswd)
        # ----- verify the username & password ---
        verify_status = self.verifyUser(self.client_mobile, pswd)
        # -----------------------------------------
        if verify_status == 'USER_VERIFIED':
            print("[Client] %s login successed." % self.client_mobile)
        else:
            print("[Client] %s error: %s" % (self.client_mobile, verify_status))
        # return the result of this login attempt ("USER_NOT_EXIST, ", "USER_UNVERIFIED", "USER_VERIFIED")
        self.clientSocket.sendall(bytes(verify_status.encode('utf-8')))
        # ------ go back to receiveCommand
        self.receiveCommand()

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

    def closeUser(self):
        print('[Client] %s left.' % self.client_mobile)
        self.clientSocket.close()

    def receiveCommand(self):
        client_command = self.clientSocket.recv(self.BUFSIZE)
        client_command = client_command.decode('utf-8')
        print("[Server] received command: ", client_command)
        if client_command == '':
            self.closeUser()
        elif client_command == 'verify_login':
            self.authenticateUser()
        elif client_command == 'register':
            self.registerUser()
        elif client_command == "GET_LOCATIONS":
            locations = self.getDB("Locations")
            self.clientSocket.sendall(bytes(str(locations).encode('utf-8')))

