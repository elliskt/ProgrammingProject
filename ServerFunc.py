from db import *
import json
import ast


class bikeSharingServer(database):
    def __init__(self, client_socket, client_addr):
        super().__init__()
        self.BUFSIZE = 1024
        self.clientSocket = client_socket
        self.clientAddr = client_addr
        self.client_login = None
        self.client_mobile = None

    def authenticateUser(self, data): # Command structure: ("mobile_number", "password")
        mobile, pswd = data[0], data[1]
        # self.clientSocket.sendall(b'verify')
        # self.client_login = self.clientSocket.recv(self.BUFSIZE)
        # self.client_login = self.client_login.decode('utf-8')
        # self.mobile, pswd = self.client_login.split(' ')
        # print('[Server] Mobile number:', mobile)
        # print('[Server] Password:', pswd)
        # ----- verify the username & password ---
        verificationStatus = self.verifyUser(mobile, pswd)
        # -----------------------------------------
        if verificationStatus == 'USER_VERIFIED':
            print("[Server] %s login succeeded" % mobile)
        else:
            print("[Server] %s error: %s" % (mobile, verificationStatus))
        # return the result of this login attempt ("USER_NOT_EXIST, ", "USER_UNVERIFIED", "USER_VERIFIED")
        self.clientSocket.sendall(bytes(verificationStatus.encode('utf-8')))
        # ------ go back to receiveCommand
        self.receiveCommand()

    def registerUser(self, data): # Command structure: ("mobile_number", "password")
        mobile, pswd = data[0], data[1]
        # self.clientSocket.sendall(b'REGISTER')
        # self.client_login = self.clientSocket.recv(self.BUFSIZE)
        # self.client_login = self.client_login.decode('utf-8')
        # mobile, pswd = self.client_login.split(' ')
        print('[Server] Username: ', mobile)
        print('[Server] Password: ', pswd)
        reg_status = self.addUser(str(mobile), pswd, "Mohammad Alharbi", 1)
        self.clientSocket.sendall(bytes(reg_status.encode('utf-8')))        # result of register attempt
        # ------ go back to receiveCommand
        self.receiveCommand()

    def closeUser(self):
        print('[Server] %s left.' % self.client_mobile)
        self.clientSocket.close()

    # Packet Structure: ("COMMAND_NAME", (command specific fields))
    def receiveCommand(self):
        client_command = self.clientSocket.recv(self.BUFSIZE).decode('utf-8')
        print("[Server] Packet received:", client_command)
        tupleRcvd = ast.literal_eval(client_command)
        command = tupleRcvd[0]
        # command = command.decode('utf-8')
        print("[Server] Received command:", command)
        if command == '':
            self.closeUser()
        elif command == 'VERIFY_LOGIN': # Command structure: ("mobile_number", "password")
            self.authenticateUser(tupleRcvd[1]) 
        elif command == 'REGISTER':# Command structure: ("mobile_number", "password")
            self.registerUser(tupleRcvd[1])
        elif command == "GET_COLUMNS_IN_TABLE": # Command structure: ("Table_name", "column1, column2, column3, etc", "conditions")
            # print(tupleRcvd[1])
            records = self.getColumnsInDB(tupleRcvd[1])
            # print(records)
            self.clientSocket.sendall(bytes(str(records).encode('utf-8')))
        # Deprecated
        # elif command == "GET_LOCATIONS":
        #     locations = self.getDB("Locations")
        #     self.clientSocket.sendall(bytes(str(locations).encode('utf-8')))

