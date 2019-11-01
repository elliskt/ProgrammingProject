##################################################### FIRST PAGE ##################################################
from Client import *
from tkinter import *
from tkinter.font import Font
from time import strftime
import math
import ast
client_connect_server()


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def show_back_button(previous_page, ):
    back_button = Button(text="<<", command=previous_page)
    back_button.place(x=10, y=10, width=50, height=25)
    back_button.configure(background="#66A1DC")


def locationsPage():
    clear_window()
    show_back_button(login_page)
    info_label = Label(text="Select your bike station: ")
    info_label.place(x=150, y=50)
    info_label.configure(font=14)
    marker = PhotoImage(file="./resources/location_icon.png")
    label_image = Label(image=marker)
    label_image.image = marker  # keep a reference
    label_image.place(x=180, y=90, width=128, height=128)
    start_y = 250
    width = 200
    height = 25
    x = 150

    # Asking server for location names in the "Locations" table
    clientSocket.send(bytes(('("GET_LOCATIONS", ("Locations", "name"))').encode('UTF-8')))
    locations = clientSocket.recv(BUFSIZE).decode('UTF-8')
    locations = ast.literal_eval(locations)
    location_buttons = []
    index = 0
    for location in locations:
        start_y += 50
        location_buttons.append(Button(text=location[0], command = lambda: bike_list_page(location[0]))) #location[0] = location name
        location_buttons[index].place(x=x, y=start_y, width=width, height=height)
        location_buttons[index].configure(font=14)
        location_buttons[index].configure(background="#98FB98")
        index += 1

def clientLogin(un, pw):
    # ============ GUI should not allow username or passwords to include spaces===========
    # login_package = '%s %s' % (un, pw)              # the user may sent space will hence error here
    # print(type(login_package))
    clientSocket.send(bytes(('("VERIFY_LOGIN", ("{}", "{}"))').format(un, pw).encode('UTF-8')))
    # clientSocket.recv(BUFSIZE)                      # receive the 'verify'
    # clientSocket.send(bytes(login_package.encode('UTF-8')))
    login_state = clientSocket.recv(BUFSIZE)
    login_state = login_state.decode('UTF-8')

    if login_state == "USER_NOT_EXIST":
        register_label = Label(text="The user does not exist!")
        register_label.place(x=150, y=220)
        register_label.configure(fg="red")
    elif login_state == "USER_NOT_VERIFIED":
        register_label = Label(text="The user and password don't match!")
        register_label.place(x=150, y=220)
        register_label.configure(fg="red")
    elif login_state == "USER_VERIFIED":
        locationsPage()


def registerClient(un, pw):
    # the user may sent space will hence error here
    # ============ GUI should not allow username or passwords to include spaces===========
    # regis_package = '%s %s' % (un, pw) 

    # ============ Bad design; serves no real purpose =============
    # clientSocket.send(b'REGISTER')
    # clientSocket.recv(BUFSIZE)  # receive the 'REGISTER' package

    # ---------- register to db ---------
    # clientSocket.send(bytes(regis_package.encode('UTF-8')))
    clientSocket.send(bytes(('("REGISTER", ("{}", "{}"))').format(un, pw).encode('UTF-8')))
    regis_state = clientSocket.recv(BUFSIZE)
    regis_state = regis_state.decode('UTF-8')
    # --------------------------------------
    if regis_state == "USER_EXISTS":
        register_label = Label(text="The user already exists!")
        register_label.place(x=150, y=220)
        register_label.configure(fg="red")
    elif regis_state == "USER_REGISTERD":
        locationsPage()


# def register(mobile, password):
#     if (check_register(mobile, password) == True):
#         register_label = Label(text="The user already exists!")
#         register_label.place(x=150, y=220)
#         register_label.configure(fg="red")
#     else:
#         # save to database
#         cursor.execute("""INSERT INTO user(mobile,password) VALUES(?,?)""", (mobile, password))
#         db.commit()
#         ## return to map
#         locationsPage()
#
#
def register_page():
    clear_window()
    show_back_button(login_page)

    logo = PhotoImage(file="./resources/bikeshare_icon2.png")
    label_image = Label(image=logo)
    label_image.image = logo
    label_image.place(x=150, y=40, width=200, height=140)

    mobile_label = Label(text="Enter your mobile:")
    mobile_label.place(x=150, y=250)
    mobile_label.configure(font=my_font)

    mobile_box = Entry(text="")
    mobile_box.place(x=150, y=280, width=200, height=25)
    mobile_box["justify"] = "center"
    mobile_box.focus()

    password_label = Label(text="Enter your password:")
    password_label.place(x=150, y=320)
    password_label.configure(font=my_font)

    password_box = Entry(text="", show="*")
    password_box.place(x=150, y=350, width=200, height=25)
    password_box["justify"] = "center"
    password_box.focus()

    register_button = Button(text="Sign Up", command=lambda: registerClient(mobile_box.get(), password_box.get()))
    register_button.place(x=150, y=400, width=200, height=25)
    register_button.configure(font=3)


def login_page():
    clear_window()

    logo = PhotoImage(file="./resources/bikeshare_icon2.png")
    label_image = Label(image=logo)
    label_image.image = logo
    label_image.place(x=150, y=40, width=200, height=140)

    mobile_label = Label(text="Enter your mobile:")
    mobile_label.place(x=150, y=250)
    mobile_label.configure(font=my_font)

    mobile_box = Entry(text="")
    mobile_box.place(x=150, y=280, width=200, height=25)
    mobile_box["justify"] = "center"
    mobile_box.focus()

    password_label = Label(text="Enter your password:")
    password_label.place(x=150, y=320)
    password_label.configure(font=my_font)

    password_box = Entry(text="", show="*")
    password_box.place(x=150, y=350, width=200, height=25)
    password_box["justify"] = "center"
    password_box.focus()

    login_button = Button(text="Log In", command=lambda: clientLogin(mobile_box.get(), password_box.get()))
    login_button.place(x=150, y=400, width=200, height=25)
    login_button.configure(font=6)
    login_button.configure(background="#66A1DC")

    register_label = Label(text="You don't have an account?")
    register_label.place(x=150, y=450)
    register_label.configure(font=("Calibri", 8))

    register_button = Button(text="Register", command=register_page)
    register_button.place(x=300, y=450, width=50, height=20)



def timer(s_initial, time_label):
    global first_timer
    global minutes
    global hours
    
    s = int(strftime("%S"))
    
    if s < s_initial:
        sec = s + 60 - s_initial
    else:
        sec = s - s_initial

    if sec == 0 and first_timer == False:
        minutes = (minutes + 1) % 60
        if minutes == 0:
            hours = (hours + 1) % 60
    else:
        first_timer = False
        
    time_label.configure(text = str(hours) + ":" + str(minutes) + ":" + str(sec)  )
    time_label.after(1000, lambda: timer(s_initial, time_label) )

def timer_page():
    
    clear_window()
    
    title = Label(text = "Your trip has started", font = ('Helvetica', 18))
    title.place(x = 140, y = 70)

    time_title = Label(text="H :   M:   S:", font = ('Helvetica', 18) )
    time_title.place(x = 180, y = 180)

    time_label = Label(text="", font = ('Helvetica', 48), fg='red')
    time_label.place(x=170, y=210)

    return_button = Button(text = "Return Bike", command = lambda: trip_summary_page(hours, minutes), font = ('Helvetica', 12))
    return_button.place(x = 150, y = 400, width = 200, height = 25)

    timer( int(strftime("%S")), time_label )

def bike_list_page(stationId): # location indexed from 0..
    # clientSocket.sendall(json.dumps('{"GET_COLUMNS_IN_TABLE", {"Bikes", "id, location_id"}}').encode('UTF-8'))
     #clear_window()
     # create a canvas object and a vertical scrollbar for scrolling it
  
     
     vscrollbar = Scrollbar(window, orient='vertical')
     vscrollbar.pack(side='right', fill='y', expand='False')
     canvas = Canvas(window, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
     canvas.pack(side="left", fill="both", expand="True")
     vscrollbar.config(command=canvas.yview)
     
     # reset the view
     canvas.xview_moveto(0)
     canvas.yview_moveto(0)
 
     # create a frame inside the canvas which will be scrolled with it
     interior = Frame(canvas)
     window.interior = interior
     interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor='nw')
     
     # track changes to the canvas and frame width and sync them,
     # also updating the scrollbar
     def configure_interior(event):
        # update the scrollbars to match the size of the inner frame
        size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
        canvas.config(scrollregion="0 0 %s %s" % size)
        if interior.winfo_reqwidth() != canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            canvas.config(width=interior.winfo_reqwidth())
            
     interior.bind('<Configure>', configure_interior)
    
     def configure_canvas(event):
        if interior.winfo_reqwidth() != canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            canvas.itemconfigure(interior_id, width=canvas.winfo_width())
    
     canvas.bind('<Configure>', configure_canvas)
     
     draw_buttons(stationId) # if it's an operator should draw operator_buttons
     show_back_button(locationsPage)



     
def draw_buttons(stationId):
    # This is the db code
    
    #conn = sql.connect("bikesharing.db")
    #c = conn.cursor()
    #c.execute("""SELECT id 
    #          FROM Bikes 
    #         WHERE condition=? AND location_id = ?;
    #          """,(1,stationId))
    #conn.commit()
    #bikelist = c.fetchall()
    
    # This is the test code
    # show_back_button(locationsPage)
    
    bikelist = ["Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike"]
    for i,x in enumerate(bikelist):
        btn = Button(window.interior, height=1, width=20, relief="flat", 
                        bg="gray99", fg="black",
                        font="Dosis", text = bikelist[i],
                        command=lambda i=i: openlink(bikelist[i]))
        btn.pack(padx=10, pady=5, side="top") 
        
def draw_operator_buttons(stationId):
    # This is the db code
    
    #conn = sql.connect("bikesharing.db")
    #c = conn.cursor()
    #c.execute("""SELECT id 
    #          FROM Bikes 
    #         WHERE condition=? AND location_id = ?;
    #          """,(1,stationId))
    #conn.commit()
    #bikelist = c.fetchall()
    
    # This is the test code
#    show_back_button(map_page)

    
    bikelist = ["Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike","Bike"]
    for i,x in enumerate(bikelist):
         
        btnwrapper = Frame(window.interior)
       
        bike_label = Label(btnwrapper, height=1, width=10, relief= RIDGE,
                        bg="gray99", fg="black",
                        font="Dosis", text = bikelist[i])
       
        repair = Button(btnwrapper, height=1, width=10, relief = RIDGE,	
                        bg="gray99", fg="black",
                        font="Dosis", text = "Repair",
                        command=lambda i=i: repair_bike_popup(bikelist[i]))
       
        move = Button(btnwrapper, height=1, width=10, relief = RIDGE,
                        bg="gray99", fg="black",
                        font="Dosis", text = "Move",
                        command=lambda i=i: move_bike_popup(bikelist[i]))
       
       
        bike_label.pack(padx=0, pady=10, side="left")
        repair.pack(padx=0, pady=5, side="left")
        move.pack(padx=0, pady=5, side="left")
        btnwrapper.pack(side="top")
   
        
def openlink(i):
    popup = Toplevel(window)
    w = 250 # width for the Tk root
    h = 100 # height for the Tk root
    ws = window.winfo_vrootwidth() # width of root window
    hs = window.winfo_vrootheight() # height of the root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window
    popup.grab_set()
    l1 = Label(popup,text = "Confirm Selection?")
    l1.pack(fill = "y")
    l2 = Label(popup,text=i)
    l2.pack(fill = "y")
    
    go_to = "open_reporter"
    
    go_to2 = "timer_page"
    
    r = Button(popup, height = 1, width = 10 , text = "Report Bike", command = lambda p=popup: popup_release(popup, go_to))
    r.pack(side="left",padx = 30)
    n = Button(popup, height = 1, width = 10 , text = "Confirm",command = lambda p=popup: popup_release(popup, go_to2))
    n.pack(side="right",padx = 15)
    popup.mainloop()
    
def repair_bike_popup(i):
    popup = Toplevel(window)
    w = 250 # width for the Tk root
    h = 100 # height for the Tk root
    ws = window.winfo_vrootwidth() # width of root window
    hs = window.winfo_vrootheight() # height of the root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window
    popup.grab_set()
    l1 = Label(popup,text = "Confirm sending bike to service?")
    l1.pack(fill = "y")
    l2 = Label(popup,text=i)
    l2.pack(fill = "y")
    go_to = ""
    
    n = Button(popup, height = 1, width = 10 , text = "Confirm",command = lambda p=popup: popup_release(popup, go_to))
    n.pack(side="top",padx = 15, pady = 15)
    popup.mainloop()
    
def move_bike_popup(i):
    popup = Toplevel(window)
    w = 250 # width for the Tk root
    h = 150 # height for the Tk root
    ws = window.winfo_vrootwidth() # width of root window
    hs = window.winfo_vrootheight() # height of the root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window
    popup.grab_set()
    l1 = Label(popup,text = "Confirm moving bike to another location?")
    l1.pack(fill = "y")
    
    l2 = Label(popup,text=i)
    l2.pack(fill = "y")
    
    go_to = ""
    
    opt = StringVar(popup)
    selection_info = "Select next location "
    opt.set(selection_info)
    next_location_menu = OptionMenu(popup, opt, "Location A", "Location B", "Location C")
    next_location_menu.pack(side = "left", padx = 10)
 
    n = Button(popup, height = 1, width = 10 , text = "Confirm",command = lambda p=popup: popup_release(popup, go_to))
    n.pack(side = "right", padx = 10)
    popup.mainloop()

def popup_release(master, go_to):
    master.grab_release()
    master.destroy()
    
    if go_to == "locationsPage":
        locationsPage()
    elif go_to == "open_reporter":
        open_reporter()
    elif go_to == "timer_page":
        timer_page()
  

def open_reporter():
    popup = Toplevel(window)
    
    w = 250 # width for the Tk root
    h = 100 # height for the Tk root
    ws = window.winfo_vrootwidth() # width of root window
    hs = window.winfo_vrootheight() # height of the root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    popup.geometry('%dx%d+%d+%d' % (w, h, x, y)) # place the popup in the middle of the window
    
    popup.grab_set()
    
    go_to = "locationsPage"
    
    message_label = Label(popup,text = "You're report has be noticed.")
    message_label.pack(fill = "y")
    
    confirm_btn = Button(popup, height = 1, width = 10 , text = "Confirm",command = lambda p=popup: popup_release(popup,go_to))
    confirm_btn.place(x=80, y= 60)
    popup.mainloop()
    
# billing screen
def trip_summary_page(hours, minutes):
    clear_window()

    tripend_label = Label(text="Trip Summary")
    tripend_label.place(x=180, y=30)
    tripend_label.configure(font=title_font)

    # for displaying end time / trip duration

    endtime_label = Label(text="Duration: " + str(hours) + " hours and " + str(minutes) + " minutes")  # (textvariable=end_loc)
    endtime_label.place(x=150, y=100, width=230, height=50)
    endtime_label.configure(font=my_font)
    

    # payment
    # setting payment to label, 0.2 pounds each minute
    p =  str(minutes * 0.2 + hours * 60 * 0.2)
    pay_label = Label(text= "Money: " +  p + " pounds ")
    pay_label.place(x=150, y=200, width=200, height=25)
    pay_label.configure(font=my_font)
    
    # dropdown for endloc
    global hint
    hint = StringVar()
    selection_info = "Select ending location "
    hint.set(selection_info)
    endlocation_menu = OptionMenu(window, hint, "Location A", "Location B", "Location C")
    endlocation_menu.place(x=160, y=300, width = 200)
    endlocation_menu.configure(font=my_font)
    
    
    pay_button = Button(text="Pay", command = lambda: verify_location(hours,minutes,hint.get(), selection_info))
    pay_button.place(x=200, y=420, width=120, height=30)
    pay_button.configure(font=my_font)
    
def verify_location(h, m , sel, sel_info):
    
    if sel == sel_info:
        trip_summary_page(h, m)
        register_label = Label(text="Please select the ending location!")
        register_label.place(x=170, y=370)
        register_label.configure(fg="red")
        
    else:
        open_pay()
        
def open_pay():
    clear_window()
    statment_label1 = Label(text="Payment Successfull.")
    statment_label1.place(x=180, y=150)
    statment_label1.configure(font=my_font)

    back_button = Button(text="Complete Trip", command=locationsPage)
    back_button.place(x=300, y=350, width=120, height=30)
    back_button.configure(font=my_font)

    report_button = Button(text="Report Bike", command=open_reporter)
    report_button.place(x=100, y=350, width=120, height=30)
    report_button.configure(font=my_font)
    
    
    
######## main #########
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
    login_page()
    window.mainloop()

window = Tk()
minutes = 0
hours = 0
first_timer = True
main_page()


