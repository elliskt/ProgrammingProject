import socket
from ClientInterface import *
import geocoder
import threading

class ClientConnection(object):
    def __init__(self): # initialize the connection attributes
        self.BUFSIZE = 1024
        self.serverAddr = ('127.0.0.1', 65501)
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connect_server()

    def client_connect_server(self): # make the connection with the server
        # ------ client connect --------
        print('Client is connecting to the server......')
        try:
            self.clientSocket.connect(serverAddr)  # try connect to server
            print("[Server] Connect successful.")

        except ConnectionRefusedError:
            print("Server error, please try again")
            exit(1)

    def getLocations(self): # send request to server for getting information from LOCATIONS TABLE
        self.clientSocket.send(bytes(('("GET_LOCATIONS", ("Locations", "name"))').encode('UTF-8')))
        locations = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        locations = ast.literal_eval(locations) # safely evaluate the expression
        return locations

    def clientLogin(self, un, pw): # send request to server for verifying login state
        self.clientSocket.send(bytes(('("VERIFY_LOGIN", ("{}", "{}"))').format(un, pw).encode('UTF-8')))
        login_state1 = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        login_state = ast.literal_eval(login_state1) # safely evaluate the expression
        return login_state

    def registerClient(self, un, pw): # send request to server for verifying register state
        # ---------- register to db ---------
        self.clientSocket.send(bytes(('("REGISTER", ("{}", "{}"))').format(un, pw).encode('UTF-8')))
        regis_state = self.clientSocket.recv(BUFSIZE)
        regis_state = regis_state.decode('UTF-8')
        return regis_state
        # --------------------------------------

    def getBike(self, location_id): # send request to server for getting all bikes from a location, where location_id is known
        command = ("GET_BIKES", location_id)
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))
        bikes = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        bikes = ast.literal_eval(bikes)
        return bikes
    
    def getBikeLocation(self, bid): # send request to server for getting the location of a bike, where bike_id is known 
        command = ("GET_BIKE_LOCATION", bid)
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))
        bikes = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        bikes = ast.literal_eval(bikes)
        return bikes

    def payBill(self, mobile, bike_id, duration, bill, start_location_id, return_location_id, date): # inform server the information of the bike used and user who rent it 
        command = ("PAY_BILL", (mobile,bike_id,duration,bill, start_location_id, return_location_id, date))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))
        payment_state = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        return payment_state

    def sendReport(self, bike_id, user_id, location_id, error_type, date): # send command to server for informing the report of a bike and the problem of it
        command = ("SEND_REPORT", (bike_id, user_id, location_id, error_type, date))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))

    def rentBike(self, bike, date, mobile): # send command to server for informing that a bike is rent and not available
        command = ("RENT_BIKE", (bike, date, mobile))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))

    def sendLocation(self, bid): # send command to server for saving bike location
        current_loc = geocoder.ip('me')
        lat = current_loc.latlng[0]
        lng = current_loc.latlng[1]
        command = ("SEND_LOCATION", (bid, lat, lng))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))

    def returnBike(self, bid, return_loc_id, mobile): # send command to server for reseting the clock after a bike was returned
        command = ("RETURN_BIKE_RESET", (bid, return_loc_id, mobile))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))

    def calDuration(self, bid):  # send request to server for getting duration
        command = ("CAL_DURATION", (bid, ))
        self.clientSocket.send(bytes(str(command).encode('UTF-8')))
        time = self.clientSocket.recv(BUFSIZE).decode('UTF-8')
        return time