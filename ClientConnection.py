import socket
from ClientInterface import *


class ClientConnection(object):
    def __init__(self):
        self.BUFSIZE = 1024
        self.serverAddr = ('127.0.0.1', 65501)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connect_server()

    def client_connect_server(self):
        # ------ client connect --------
        print('Client is connecting to the server......')
        try:
            self.clientSocket.connect(serverAddr)  # try connect to server
            print("[Server] Connect successful.")

        except ConnectionRefusedError:
            print("Server error, please try again")
            exit(1)

    def getLocations(self):
        self.clientSocket.send(bytes(('("GET_LOCATIONS", ("Locations", "name"))').encode('UTF-8')))
        locations = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        locations = ast.literal_eval(locations)
        return locations

    def clientLogin(self, un, pw):
        self.clientSocket.send(bytes(('("VERIFY_LOGIN", ("{}", "{}"))').format(un, pw).encode('UTF-8')))
        login_state = self.clientSocket.recv(BUFSIZE)
        login_state = login_state.decode('UTF-8')
        return login_state

    def registerClient(self, un, pw):
        # the user may sent space will hence error here
        # ============ GUI should not allow username or passwords to include spaces===========
        # regis_package = '%s %s' % (un, pw)

        # ---------- register to db ---------
        self.clientSocket.send(bytes(('("REGISTER", ("{}", "{}"))').format(un, pw).encode('UTF-8')))
        regis_state = self.clientSocket.recv(BUFSIZE)
        regis_state = regis_state.decode('UTF-8')
        return regis_state
        # --------------------------------------

    def getBike(self, location_id):
        command = ("GET_BIKES", location_id)
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))
        bikes = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        bikes = ast.literal_eval(bikes)
        return bikes

    def payBill(self, mobile, bike_id, duration, bill, start_location_id, return_location_id):
        command = ("PAY_BILL", (mobile,bike_id,duration,bill, start_location_id, return_location_id))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))
        payment_state = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        return payment_state