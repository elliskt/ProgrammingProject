# -*- coding: utf-8 -*-
import ast
import tkinter as tk
from tkinter.font import Font
import socket
import time
from threading import Thread

FIRST = True
bike_window = None
LABELSLIST = []
BUFSIZE = 1024
serverAddr = ('127.0.0.1', 65501)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
locations_id = ["1-Partick", "2-Glasgow Uni", "3-Glasgow City Centre", "4-Buchanan Bus Station"]
locations_id_abb = ["1-Pt", "2-UoG", "3-GCC", "4-BBS"]
TIMER = 10
ddlist = []
fixbuttonlist = []
confirmbuttonlist = []

# ------------- set a timer that is updated in every 10s
def timer_update(lb):
    global TIMER
    while True:
        TIMER -= 1
        lb.config(text='Update in {}s'.format(TIMER))
        if TIMER == 0:
            TIMER = 10
            updateButton(bike_window)
        time.sleep(1)

# ------------ color code to rgb function ----------
def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb

# ------------- the changed data will show in red color for a sec --------
def changed_color(label, str_1):
    for i in range(255,0,-1):
        label.config(text=str_1, fg=_from_rgb((i, 0, i//2)))
        time.sleep(0.01)

# --------------- connect the page to server  ----------
def client_connect_server():
    # ------ client connect --------
    print('Client is connecting to the server......')
    try:
        clientSocket.connect(serverAddr)  # try connect to server
        print("[Server] Connect successful.")

    except ConnectionRefusedError:
        print("Server error, please try again")
        exit(1)

# ------------ send the get bike command to server -----
def getBikes():
    command = ("GET_ALL_BIKES",)
    clientSocket.send(bytes(str(command).encode('UTF-8')))
    bikes = clientSocket.recv(BUFSIZE).decode('UTF-8')
    bikes = ast.literal_eval(bikes)
    return bikes

# ------------ send the move bike command to server -----
def moveBike(bike_id, location_id, num):
    command = ("MOVE_BIKE",(bike_id, location_id))
    clientSocket.send(bytes(str(command).encode('UTF-8')))

# ------------ send the fix bike command to server -----
def fixBike(bike_id):
    command = ("FIX_BIKE", (bike_id,))
    clientSocket.send(bytes(str(command).encode('UTF-8')))

# ------------ update button that can update the table -----
def updateButton(window):
    global TIMER
    global FIRST
    global LABELSLIST
    bikes = getBikes()
    global ddlist
    global fixbuttonlist
    global confirmbuttonlist
    for row in range(len(bikes)):
        # -----------
        if FIRST:
            ddlist.append(tk.StringVar())
            selection_info = "Move to..."
            ddlist[row].set(selection_info)
            endlocation_menu = tk.OptionMenu(window, ddlist[row], *locations_id)
            endlocation_menu.grid(row=row+2, column=7)
            # -------------
            b = tk.Button(text='Confirm', width=18, height=1, borderwidth=2, relief="raised",
                          command=lambda id=bikes[row][0], dd= ddlist[row], rownum=row:moveBike(id, dd.get().split('-')[0],rownum))
            b.grid(row=row+2, column = 8)
            confirmbuttonlist.append(b)
            # ---------
            f = tk.Button(text='Fix Bike', width=18, height=1, borderwidth=2, relief="raised",
                          command=lambda id=bikes[row][0]: fixBike(id))
            f.grid(row=row + 2, column=9)
            fixbuttonlist.append(f)
        # ------------
        rowlist = []
        for column in range(len(bikes[row])):
            cur_text = str(bikes[row][column]) if str(bikes[row][column]) != 'None' else '-'
            if column == 1:
                cur_text ='-' if str(bikes[row][column]) == 'None' else locations_id_abb[int(bikes[row][column])-1]
            if FIRST:
                label = tk.Label(text=cur_text,
                        width=18, height=2, borderwidth=2, relief="sunken", )
                label.grid(row=row + 2, column=column)
                rowlist.append(label)
            else:
                if LABELSLIST[row][column].cget("text") == cur_text:
                    continue
                else:
                    changing_color = Thread(target=changed_color, args=(LABELSLIST[row][column], cur_text))
                    changing_color.start()
        if FIRST:
            LABELSLIST.append(rowlist)
        if str(bikes[row][6]) == 'False':
            fixbuttonlist[row].config(state='disabled')
        elif str(bikes[row][6]) == 'True':
            fixbuttonlist[row].config(state='normal')
        if str(bikes[row][2]) == 'True':
            confirmbuttonlist[row].config(state='disabled')
        elif str(bikes[row][2]) == 'False':
            confirmbuttonlist[row].config(state='normal')
    FIRST = False
    TIMER = 10

# ----------- init the table format -----------------
def show_status_page():
    global bike_window
    bike_window = tk.Tk()
    bike_window.title('Operator-Bikes Staus')
    btn = tk.Button(bike_window, width=10, height=2, text='Update', command=lambda: updateButton(bike_window))
    btn.grid(row=0, column=0)
    time_label = tk.Label(text='Update in {}s'.format(TIMER), width=18, height=2, borderwidth=2, relief="solid", )
    time_label.grid(row=0, column=1)
    tk.Label(text='BikeID', width=18, height=2, borderwidth=2, relief="sunken", ).grid(row=1, column=0)
    tk.Label(text='BikeStop', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=1)
    tk.Label(text='In use', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=2)
    tk.Label(text='Loc_latitute', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=3)
    tk.Label(text='Loc_longtitute', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=4)
    tk.Label(text='Rent time from', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=5)
    tk.Label(text='Reported', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=6)
    tk.Label(text='Move to', width=18, height=2, borderwidth=2, relief="sunken").grid(row=1, column=7)
    timer = Thread(target=timer_update, args=(time_label, ))
    timer.start()
    bike_window.mainloop()


if __name__ == '__main__':
    client_connect_server()
    show_status_page()