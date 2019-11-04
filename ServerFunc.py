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

    # ------------- close user --------------
    def closeUser(self):
        print('[Server] %s left.' % self.client_mobile)
        self.clientSocket.close()
    # -------------------------------------------

    # -------------- authenticate user ----------------
    def authenticateUserCommand(self, data): # Command structure: ("mobile_number", "password")
        mobile, pswd = data[0], data[1]
        # self.clientSocket.sendall(b'verify')
        # self.client_login = self.clientSocket.recv(self.BUFSIZE)
        # self.client_login = self.client_login.decode('utf-8')
        # self.mobile, pswd = self.client_login.split(' ')
        print('[Server] Mobile number:', mobile)
        print('[Server] Password:', pswd)
        # ----- verify the username & password ---
        verificationStatus = self.verifyUser(mobile, pswd)
        # -----------------------------------------
        if verificationStatus == 'USER_VERIFIED':
            print("[Server] %s login succeeded." % mobile)
        else:
            print("[Server] %s error: %s" % (mobile, verificationStatus))
        # return the result of this login attempt ("USER_NOT_EXIST, ", "USER_UNVERIFIED", "USER_VERIFIED")
        self.clientSocket.sendall(bytes(verificationStatus.encode('utf-8')))
        # ------ go back to receiveCommand
        self.receiveCommand()

    # -------------- register user -------------------------------------------------------
    def registerUserCommand(self, data): # Command structure: ("mobile_number", "password")
        mobile, pswd = data[0], data[1]
        # print('[Server] Username: ', mobile)
        # print('[Server] Password: ', pswd)
        reg_status = self.addUser(str(mobile), pswd, "Mohammad Alharbi", 1)
        self.clientSocket.sendall(bytes(reg_status.encode('utf-8')))        # result of register attempt
        # ------ go back to receiveCommand
        self.receiveCommand()

    # --------------get the locations  -------------------
    def getLocationsCommand(self, tupleRcvd):
        records = self.getColumnsInDB(tupleRcvd)
        self.clientSocket.sendall(bytes(str(records).encode('utf-8')))
        self.receiveCommand()

    # ------------- get the bikes from Location ----------
    def getBikesCommand(self, location_id):
        bikes = self.getBikesInLocation(location_id)
        self.clientSocket.sendall(bytes(str(bikes).encode('utf-8')))
        self.receiveCommand()

    # ------------ pay bill and record -----------------
    def payBillCommand(self, tupleRcvd):
        # (mobile, bike_id, duration, bill, start_location_id, return_location_id)
        pay_state = self.payBill(tupleRcvd[0], tupleRcvd[3])
        self.clientSocket.sendall(bytes(str(pay_state).encode('utf-8')))
        self.receiveCommand()

    # ------------ pay bill and record -----------------
    def sendReportCommand(self, tupleRcvd):
        # (bike_id, user_id, location_id, error_type, date)
        self.writeReport(tupleRcvd)
        self.receiveCommand()

    # ------------- get all bikes ----------------------
    def getAllBikesCommand(self):
        records = self.getAllBikes()
        self.clientSocket.sendall(bytes(str(records).encode('utf-8')))
        self.receiveCommand()

    # ------------- Packet Structure: ("COMMAND_NAME", (command specific fields)) ------------
    def receiveCommand(self):
        client_command = self.clientSocket.recv(self.BUFSIZE).decode('utf-8')
        print("[Server] Package received:", client_command)
        tupleRcvd = ast.literal_eval(client_command)
        command = tupleRcvd[0]
        # command = command.decode('utf-8')
        if command == '':
            self.closeUser()
        elif command == 'VERIFY_LOGIN':     # Command structure: ("mobile_number", "password")
            self.authenticateUserCommand(tupleRcvd[1])
        elif command == 'REGISTER':         # Command structure: ("mobile_number", "password")
            self.registerUserCommand(tupleRcvd[1])
        elif command == "GET_LOCATIONS":    # Command structure: ("Table_name", "column1, column2, column3, etc"))
            self.getLocationsCommand(tupleRcvd[1])
        elif command == "GET_BIKES":
            self.getBikesCommand(tupleRcvd[1])
        elif command == "PAY_BILL":
            self.payBillCommand(tupleRcvd[1])
        elif command == "SEND_REPORT":
            self.sendReportCommand(tupleRcvd[1])
        elif command == "GET_ALL_BIKES":
            self.getAllBikesCommand()
