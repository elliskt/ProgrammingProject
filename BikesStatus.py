# -*- coding: utf-8 -*-
import ast
import tkinter as tk
import socket
import time
from threading import Thread

FIRST = True
LABELSLIST = []
BUFSIZE = 1024
serverAddr = ('127.0.0.1', 65501)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
locations = ["Partick", "Glasgow Uni", "Glasgow City Centre", "Buchana Bus station"]
TIMER = 10


def timer_update(lb):
    global TIMER
    while True:
        TIMER -= 1
        lb.config(text='Update in {}s'.format(TIMER))
        if TIMER == 0:
            TIMER = 10
            updateButton()
        time.sleep(1)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code"""
    return "#%02x%02x%02x" % rgb

def changed_color(label, str_1):
    for i in range(255,0,-1):
        label.config(text=str_1, fg=_from_rgb((i, 0, i//2)))
        time.sleep(0.01)

def client_connect_server():
    # ------ client connect --------
    print('Client is connecting to the server......')
    try:
        clientSocket.connect(serverAddr)  # try connect to server
        print("[Server] Connect successful.")

    except ConnectionRefusedError:
        print("Server error, please try again")
        exit(1)

def getBikes():
    command = ("GET_ALL_BIKES",)
    clientSocket.send(bytes(str(command).encode('UTF-8')))
    bikes = clientSocket.recv(BUFSIZE).decode('UTF-8')
    bikes = ast.literal_eval(bikes)
    return bikes

def updateButton():
    global TIMER
    global FIRST
    global LABELSLIST
    bikes = getBikes()
    for row in range(len(bikes)):
        rowlist = []
        for column in range(len(bikes[row])):
            cur_text = str(bikes[row][column]) if str(bikes[row][column]) != 'None' else '-'
            if FIRST:
                label = tk.Label(text=cur_text,
                        width=15, height=2, borderwidth=2, relief="sunken", )
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
    FIRST = False
    TIMER = 10


def show_status_page():
    bike_window = tk.Tk()
    bike_window.title('Operator-Bikes Staus')
    btn = tk.Button(bike_window, width=10, height=2, text='Update', command=lambda: updateButton())
    btn.grid(row=0, column=0)
    time_label = tk.Label(text='Update in {}s'.format(TIMER), width=15, height=2, borderwidth=2, relief="solid", )
    time_label.grid(row=0, column=1)
    tk.Label(text='BikeID', width=15, height=2, borderwidth=2, relief="sunken", ).grid(row=1, column=0)
    tk.Label(text='BikeStop', width=15, height=2, borderwidth=2, relief="sunken").grid(row=1, column=1)
    tk.Label(text='In use', width=15, height=2, borderwidth=2, relief="sunken").grid(row=1, column=2)
    tk.Label(text='Loc_latitute', width=15, height=2, borderwidth=2, relief="sunken").grid(row=1, column=3)
    tk.Label(text='Loc_longtitute', width=15, height=2, borderwidth=2, relief="sunken").grid(row=1, column=4)
    tk.Label(text='Rent time from', width=15, height=2, borderwidth=2, relief="sunken").grid(row=1, column=5)
    tk.Label(text='Reported', width=15, height=2, borderwidth=2, relief="sunken").grid(row=1, column=6)
    timer = Thread(target=timer_update, args=(time_label,))
    timer.start()
    bike_window.mainloop()




if __name__ == '__main__':
    client_connect_server()
    show_status_page()