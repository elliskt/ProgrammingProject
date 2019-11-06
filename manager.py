from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter.font import Font
import socket
from threading import Thread
import ast
import datetime

bike_window = None
LABELSLIST = []
BUFSIZE = 1024
serverAddr = ('127.0.0.1', 65501)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
locations_id = [1, 2, 3, 4]
locations_id_abb = ["1-Pt", "2-UoG", "3-GCC", "4-BBS"]


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
            "Rental activities in last 7 days",
            "Rents per station",
            "Broken Bike per station"
            ]
    
    #values for dropdown menu
    varx = StringVar(window)
    varx.set(datatype[0])

    #The drop down menu
    xaxis = OptionMenu(window,varx,*datatype)
    x = Label(text="Data")
    x.configure(bg = "white", font=('Helvetica',16))
    x.grid(row=0,column=1,padx = 260)
    xaxis.grid(row=4,column=1)
    
    #The draw button
    plot = Button(window, height = 1, width = 5,text = "Draw", bg = "#66A1DC", font = ('Roboto',10), command=lambda: draw(varx.get()))
    plot.grid(row=5,column=1,pady = 40)
    
        
    label  = Label(text = "The graph will be displayed here ...", ) 
    label.place(x = 200, y = 300) 
    
#----This function is used to get data and call the appropriate chart fucntion
def draw(datatype):
        if datatype =="Rental activities in last 7 days":
            i=0
            xaxis = []
            #get the date of last 7 days
            while i<7:
                xaxis.append(datetime.date.today()-datetime.timedelta(days = i))
                i+=1
            rentals_per_station = []
            #get the rental activities count for each station at each day
            for i in locations_id :
                temp = []
                #looping through each days for station i
                for d in xaxis:
                    
                    #getLog returns the total rental activities for date d and station i
                    #and append the data to temp
                    #So basically at the end of the inner loop the temp will have 7 days activities count with station 
                    
                    temp.append(getLog(d,i))
                    
                #append the activities spanning 7 days for each station to rentals_per_station
                rentals_per_station.append(temp)
                
            #call the line chart function
            LineChart(xaxis,rentals_per_station,locations_id_abb)
            
        elif datatype =="Rents per station":
            #get the appropriate data
            income_per_station = getIncome()
             #call the bar chart function   
            BarChart(locations_id_abb,income_per_station,False)
            
        elif datatype =="Broken Bike per station":
            #get the appropriate data
            brokenBikes = getBrokenBike()
            #call the pie chart function   
            PieChart(locations_id_abb,brokenBikes)

def LineChart(datasetx,datasety,legend_name):
    #define size of the chart
    fig = Figure(figsize=(7,5))
    #define the position 
    a = fig.add_subplot(111)
    #dataset y contains a list of rental activities from each station
    #it will loop through dataset y and draw a line for each station
    #x axis is last 7 days
    for r in datasety:
        a.plot(datasetx,r)
    #adding a legend
    a.legend([legend_name[0], legend_name[1], legend_name[2], legend_name[3]], loc='upper left')
    #draw the figure
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=5)

    #----Bar Chart function----
def BarChart(datasetx,datasety,stacked):
    #draw the figure with given data
    fig = Figure(figsize=(7,5))
    a = fig.add_subplot(111)
    a.bar(datasetx,datasety)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)

    #----Pie Chart function----
def PieChart(datasetx,datasety):
    
    fig = Figure(figsize=(7,5))
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

def getLog(today,id):
    command = ("GET_LOG_COUNT",(str(today) , id))
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

def color_widget_bg():
    for widget in window.winfo_children():
        if widget.winfo_class() == 'Label':
            widget.configure(bg = "white")
            
def main_page():
    window.title("BikeSharing")
    window.configure(bg = "white")
    w = 550 # width for the Tk root
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
    color_widget_bg()
    window.mainloop()



if __name__ == '__main__':
    
    client_connect_server()
    window = Tk()
    main_page()