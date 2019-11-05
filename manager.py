from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.font import Font
import socket
from threading import Thread
import ast

#FIRST = True
bike_window = None
LABELSLIST = []
BUFSIZE = 1024
serverAddr = ('127.0.0.1', 65501)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
locations_id = [1, 2, 3, 4]
locations_id_abb = ["1-Pt", "2-UoG", "3-GCC", "4-BBS"]
#TIMER = 10
#ddlist = []
#fixbuttonlist = []
#confirmbuttonlist = []


def client_connect_server():
    # ------ client connect --------
    print('Client is connecting to the server......')
    try:
        clientSocket.connect(serverAddr)  # try connect to server
        print("[Server] Connect successful.")

    except ConnectionRefusedError:
        print("Server error, please try again")
        exit(1)

def manager_page():
    
    datatype = [
            "Rental activities",
            "Rents per station",
            "Broken Bike per station"
            ]
      

    Chart_Type = [
            "Bar Chart",
            "Pie Chart"
            ]

    varx = StringVar(window)
    varx.set(datatype[0])
  
    varchart = StringVar(window)
    varchart.set(Chart_Type[0])

    xaxis = OptionMenu(window,varx,*datatype)
    x = Label(text="Data")
    x.grid(row=0,column=0,padx = 90)
    xaxis.grid(row=1,column=0)
    
    chartType = OptionMenu(window,varchart,*Chart_Type)
    chart = Label(text="Chart Types")
    chart.grid(row=0,column=2,padx = 90)
    chartType.grid(row=1,column=2)
    
    plot = Button(window, height = 1, width = 5,text = "Draw",command=lambda: draw(varchart.get(),varx.get()))
    plot.grid(row=2,column=1,pady = 40)

def draw(chartType,datatype):
    if chartType == "Bar Chart":
        if datatype =="Rental activities":
            
            rentals_per_station = getLog()
            print(rentals_per_station)
            BarChart(locations_id_abb,rentals_per_station,False)
        elif datatype =="Rents per station":
            
            income_per_station = getIncome()
                
            BarChart(locations_id_abb,income_per_station,False)
        elif datatype =="Broken Bike per station":
            
            brokenBikes = getBrokenBike()
            
            BarChart(locations_id_abb,brokenBikes,False)
        
    elif chartType  == "Pie Chart":
        if datatype =="Rental activities":
            
            rentals_per_station = getLog()
                
            PieChart(locations_id_abb,rentals_per_station)
        elif datatype =="Rents per station":
            
            income_per_station = getIncome()
            
            PieChart(locations_id_abb,income_per_station)
        elif datatype =="Broken Bike per station":
            
            brokenBikes = getBrokenBike()
            
            PieChart(locations_id_abb,brokenBikes)
    else:
        print("you picked the wrong chart fool!")

def LineChart(datasetx,datasety):
    
    fig = Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.plot(datasetx,datasety)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)

def BarChart(datasetx,datasety,stacked):
    
    fig = Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.bar(datasetx,datasety)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)

def PieChart(datasetx,datasety):
    
    fig = Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.pie(datasety,labels=datasetx)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)
    
def getLocations():
    clientSocket.send(bytes(('("GET_LOCATIONS", ("Locations", "name"))').encode('UTF-8')))
    locations = clientSocket.recv(BUFSIZE).decode('UTF-8')
    locations = ast.literal_eval(locations)
    return locations

def getLog():
    command = ("GET_LOG_COUNT",)
    clientSocket.send(bytes(str(command).encode('UTF-8'))) 
    log_count = clientSocket.recv(BUFSIZE).decode('UTF-8')
    log_count = ast.literal_eval(log_count)
    return log_count

def getIncome():
    command = ("GET_INCOME",)
    clientSocket.send(bytes(str(command).encode('UTF-8'))) 
    log_count = clientSocket.recv(BUFSIZE).decode('UTF-8')
    log_count = ast.literal_eval(log_count)
    return log_count

def getBrokenBike():
    command = ("GET_BROKEN_BIKE",)
    clientSocket.send(bytes(str(command).encode('UTF-8'))) 
    log_count = clientSocket.recv(BUFSIZE).decode('UTF-8')
    log_count = ast.literal_eval(log_count)
    return log_count


def main_page():
    window.title("BikeSharing")
    w = 500 # width for the Tk root
    h = 530 # height for the Tk root
    
    # get screen width and height
    ws = window.winfo_screenwidth() # width of the screen
    hs = window.winfo_screenheight() # height of the screen
    
    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y)) # place the window in the middle of the screen

    global my_font
    my_font = Font(size=12)
    global title_font
    title_font = ('Helvetica', 18)
    manager_page()
    window.mainloop()



if __name__ == '__main__':
    
    client_connect_server()
    window = Tk()
    main_page()