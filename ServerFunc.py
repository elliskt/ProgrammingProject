from db import *
from db import *
from threading import Thread
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
        print('[Server] %s left.' % (self.client_mobile ))
        self.clientSocket.close()
        exit(1)
    # -------------------------------------------

    # -------------- authenticate user ----------------
    def authenticateUserCommand(self, data): # Command structure: ("mobile_number", "password")
        mobile, pswd = data[0], data[1]
        # self.clientSocket.sendall(b'verify')
        # self.client_login = self.clientSocket.recv(self.BUFSIZE)
        # self.client_login = self.client_login.decode('utf-8')
        # self.mobile, pswd = self.client_login.split(' ')
        # print('[Server] Mobile number:', mobile)
        # print('[Server] Password:', pswd)
        # ----- verify the username & password ---
        verificationStatus = self.verifyUser(mobile, pswd)
        print("verificationStatus", verificationStatus)
        # -----------------------------------------
        if verificationStatus[0] == 'USER_VERIFIED' or verificationStatus[0] =="USER_VERIFIED_USING":
            print("[Server] %s login succeeded." % mobile)
        else:
            print("[Server] %s error: %s" % (mobile, verificationStatus))
        # return the result of this login attempt ("USER_NOT_EXIST, ", "USER_UNVERIFIED", "USER_VERIFIED")
        self.clientSocket.sendall(bytes(str(verificationStatus).encode('utf-8')))
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
        pay_state = self.payBill(tupleRcvd[0], tupleRcvd[1], tupleRcvd[2], tupleRcvd[3], tupleRcvd[4], tupleRcvd[5], tupleRcvd[6])
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
        
    def getBikeLocationCommand(self,tupleRcvd):
        records = self.getBikeLocation(tupleRcvd)
        self.clientSocket.sendall(bytes(str(records).encode('utf-8')))
        self.receiveCommand()

    # ----- move bike ----
    def moveBikeCommand(self, tupleRcvd):
        self.moveBike(tupleRcvd)
        self.receiveCommand()

    # ------ fix bike -----
    def fixBikeCommand(self, tupleRcvd):
        self.fixBike(tupleRcvd)
        self.receiveCommand()

    def rentBikeCommand(self, tupleRcvd):
        self.rentBike(tupleRcvd)
        self.receiveCommand()

    def sendLocationCommand(self, tupleRcvd):
        self.sendLocation(tupleRcvd)
        self.receiveCommand()

    def returnBikeResetCommand(self, tupleRcvd):
        self.returnBikeReset(tupleRcvd)
        self.receiveCommand()
        
    def getIncomeCommand(self):
        income = self.getIncomeperStation()
        self.clientSocket.sendall(bytes(str(income).encode('utf-8')))
        self.receiveCommand()
        
    def getBrokenBikeCommand(self):
        badBikes = self.getBrokenbikesperStation()
        self.clientSocket.sendall(bytes(str(badBikes).encode('utf-8')))
        self.receiveCommand()

    def calDurationCommand(self, tupleRcvd):
        time = self.calDuration(tupleRcvd)
        self.clientSocket.sendall(bytes(str(time).encode('utf-8')))
        self.receiveCommand()
    
    def getLogCommand(self, tupleRcvd):
        counts = self.countLogperStation(tupleRcvd)
        self.clientSocket.sendall(bytes(str(counts).encode('utf-8')))
        self.receiveCommand()

    # ------------- Packet Structure: ("COMMAND_NAME", (command specific fields)) ------------
    def receiveCommand(self):
        client_command = self.clientSocket.recv(self.BUFSIZE).decode('utf-8')
        if client_command == '':
            self.closeUser()
        else:
            print("[Server] Package received:", client_command)
            tupleRcvd = ast.literal_eval(client_command)
            command = tupleRcvd[0]
        if command == 'VERIFY_LOGIN':     # Command structure: ("mobile_number", "password")
            self.authenticateUserCommand(tupleRcvd[1])
        elif command == 'REGISTER':         # Command structure: ("mobile_number", "password")
            self.registerUserCommand(tupleRcvd[1])
        elif command == "GET_LOCATIONS":    # Command structure: ("Table_name", "column1, column2, column3, etc"))
            self.getLocationsCommand(tupleRcvd[1])
        elif command == "GET_BIKES":
            self.getBikesCommand(tupleRcvd[1])
        elif command == "GET_BIKE_LOCATION":
            self.getBikeLocationCommand(tupleRcvd[1])
        elif command == "PAY_BILL":
            self.payBillCommand(tupleRcvd[1])
        elif command == "SEND_REPORT":
            self.sendReportCommand(tupleRcvd[1])
        elif command == "GET_ALL_BIKES":
            self.getAllBikesCommand()
        elif command == "MOVE_BIKE":
            self.moveBikeCommand(tupleRcvd[1])
        elif command == "FIX_BIKE":
            self.fixBikeCommand(tupleRcvd[1])
        elif command == "RENT_BIKE":
            self.rentBikeCommand(tupleRcvd[1])
        elif command =="SEND_LOCATION":
            self.sendLocationCommand(tupleRcvd[1])
        elif command =="RETURN_BIKE_RESET":
            self.returnBikeResetCommand(tupleRcvd[1])
        elif command == "GET_LOG_COUNT":
            self.getLogCommand(tupleRcvd[1])    # Command structure: ("today", "Id"))
        elif command == "GET_INCOME":
            self.getIncomeCommand()
        elif command == "GET_BROKEN_BIKE":
            self.getBrokenBikeCommand()
        elif command == "CAL_DURATION":
            self.calDurationCommand(tupleRcvd[1])