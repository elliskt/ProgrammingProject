from Client import *
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from tkinter.font import Font
from time import strftime
import datetime
import ast
from matplotlib.figure import Figure
from ClientConnection import ClientConnection
import threading


class ClientInterface(ClientConnection):
    def __init__(self):
        super().__init__()
        self.window = Tk()
        self.window.title("Bike Sharing System")
        self.username = None
        self.bike_id = None
        self.duration = None
        self.payment = None
        self.start_location_id = None
        self.return_location_id = None
        self.sec = 0
        self.minutes = 0
        self.hours = 0
        self.first_timer = True
        self.my_font = Font(size=12)
        self.title_font = ('Helvetica', 18)
        self.register_label = None
        self.sec_backup = None
        self.window.wm_iconbitmap('./resources/bicycle-rider.png')
        self.window.configure(bg = "white")

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()
            
    def color_widget_bg(self):
        for widget in self.window.winfo_children():
            if widget.winfo_class() == 'Label':
                widget.configure(bg = "white")

    def reset_timer(self):
        self.hours = 0
        self.minutes = 0
        self.sec = 0
        self.first_timer = True

    def show_back_button(self, previous_page):
        back_button = Button(text="<<", command=previous_page)
        back_button.place(x=10, y=10, width=50, height=25)
        back_button.configure(background="#66A1DC")

    def main_page(self):
        self.window.title("Bike Sharing System")
        w = 500  # width for the Tk root
        h = 530  # height for the Tk root
        # get screen width and height
        ws = self.window.winfo_screenwidth()  # width of the screen
        hs = self.window.winfo_screenheight()  # height of the screen
        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        # place the window in the middle of the screen
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # show the window with login page
        self.login_page()
        self.window.mainloop()

    def valid_number(self, phone_number):
        if len(phone_number) != 10:
            return False
        
        for i in range(10):
            if not phone_number[i].isalnum():
                return False
        return True
    
    def valid_password(self, psw):
        if len(psw) < 5:
            return False
        else:
            return True

    def register_page_connect(self, un, pw):
        if self.valid_number(un) == True:
            if self.valid_password(pw):
                regis_state = self.registerClient(un, pw)
                if regis_state == "USER_EXISTS":
                    self.register_label = Label(text="The user already exists!")
                    self.register_label.place(x=150, y=220)
                    self.register_label.configure(fg="red")
                elif regis_state == "USER_REGISTERD":
                    self.locationsPage()
            else:
                
                if self.register_label:
                    self.register_label.destroy()
                    
                self.register_label = Label(text="The password should be at least 5 charachters long!")
                self.register_label.place(x=120, y=220)
                self.register_label.configure(fg="red")
        else:
             
             if self.register_label:
                 self.register_label.destroy()
              
             self.register_label = Label(text="The phone number is not valid! It should have 10 digits!")
             self.register_label.place(x=110, y=220)
             self.register_label.configure(fg="red")
             
        self.color_widget_bg() # delete the gray bg of widgets

    def register_page(self):
        self.clear_window()
        self.show_back_button(self.login_page)
        # ----- place image -------------
        logo = PhotoImage(file="./resources/bikeshare_icon2.png")
        label_image = Label(image=logo)
        label_image.image = logo
        label_image.place(x=150, y=40, width=200, height=140)
        # ----- mobile textbox ----------
        mobile_label = Label(text="Enter your mobile:")
        mobile_label.place(x=150, y=250)
        mobile_label.configure(font=self.my_font)
        mobile_box = Entry(text="")
        mobile_box.place(x=150, y=280, width=200, height=25)
        mobile_box["justify"] = "center"
        mobile_box.focus()
        mobile_box.configure(bg="#F8F8F8")             
        # ----- password textbox ----------
        password_label = Label(text="Enter your password:")
        password_label.place(x=150, y=320)
        password_label.configure(font=self.my_font)
        password_box = Entry(text="", show="*")
        password_box.place(x=150, y=350, width=200, height=25)
        password_box["justify"] = "center"
        password_box.focus()
        password_box.configure(bg="#F8F8F8") 
        # -------- register button ---------
        register_button = Button(text="Sign Up", command=lambda: self.register_page_connect(mobile_box.get(), password_box.get()))
        register_button.place(x=150, y=400, width=200, height=25)
        register_button.configure(font=3)
        register_button.configure(background="#66A1DC")
                                  
        self.color_widget_bg() # delete the gray bg of widgets

    def login_page_connect(self, un, pw):
      
       
        if len(un) != 0:
            if len(pw) != 0:
                login_state = self.clientLogin(un, pw)
                if login_state[0] == "USER_NOT_EXIST":
                    register_label = Label(text="The user does not exist!")
                    register_label.place(x=150, y=220)
                    register_label.configure(fg="red")
                elif login_state[0] == "USER_NOT_VERIFIED":
                    register_label = Label(text="The user and password don't match!")
                    register_label.place(x=150, y=220)
                    register_label.configure(fg="red")
                elif login_state[0] == "USER_VERIFIED" and login_state[1] is None:
                    self.username = un
                    self.locationsPage()
                elif login_state[0] == "USER_VERIFIED":
                    self.username = un
                    self.bike_id = int(login_state[1])
                    self.cal_to_timer(self.bike_id)
            else:
                if self.register_label:
                    self.register_label.destroy()
              
                self.register_label = Label(text="You need to introduce a password!")
                self.register_label.place(x=160, y=220)
                self.register_label.configure(fg="red")
        else:
            if self.register_label:
                 self.register_label.destroy()
              
            self.register_label = Label(text="You need to introduce a mobile phone!")
            self.register_label.place(x=140, y=220)
            self.register_label.configure(fg="red")
            
        self.color_widget_bg() # delete the gray bg of widgets

    def cal_to_timer(self, bid):
        self.start_location_id = self.getBikeLocation(bid)
        self.bike_id = bid
        self.first_timer = True
        previous_time = self.calDuration(bid)
        pre = previous_time.split('-')[1]
        d = datetime.datetime.now().strftime("/%m/%d/%Y-%H:%M:%S")
        d = datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S")
        now = d.split('-')[1]
        self.hours=int(now[0]) - int(pre[0])
        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(now, FMT) - datetime.datetime.strptime(pre, FMT)
        print("[Client] continuous duration: ", tdelta)
        self.hours = int(str(tdelta).split(':')[0])
        self.minutes = int(str(tdelta).split(':')[1])
        self.sec = int(str(tdelta).split(':')[2])
        self.sec_backup = int(str(tdelta).split(':')[2])
        self.timer_page()

    def login_page(self):
        self.clear_window()
        # ----- place image -----
        logo = PhotoImage(file="./resources/bikeshare_icon2.png")
        label_image = Label(image=logo)
        label_image.image = logo
        label_image.place(x=150, y=40, width=200, height=140)
        # ------ mobile textbox -----
        mobile_label = Label(text="Enter your mobile:")
        mobile_label.place(x=150, y=250)
        mobile_label.configure(font=self.my_font)
        mobile_box = Entry(text="")
        mobile_box.place(x=150, y=280, width=200, height=25)
        mobile_box["justify"] = "center"
        mobile_box.focus()
        mobile_box.configure(bg="#F8F8F8") 
        # ------ password textbox -----
        password_label = Label(text="Enter your password:")
        password_label.place(x=150, y=320)
        password_label.configure(font=self.my_font)
        password_box = Entry(text="", show="*")
        password_box.place(x=150, y=350, width=200, height=25)
        password_box["justify"] = "center"
        password_box.focus()
        password_box.configure(bg="#F8F8F8") 
        # -------- login button ---------
        login_button = Button(text="Log In", command=lambda: self.login_page_connect(mobile_box.get(), password_box.get()))
        login_button.place(x=150, y=400, width=200, height=25)
        login_button.configure(font=6)
        login_button.configure(background="#66A1DC")
        # -------- register button ---------
        register_label = Label(text="You don't have an account?")
        register_label.place(x=150, y=450)
        register_label.configure(font=("Calibri", 8))
        register_button = Button(text="Register", command=self.register_page)
        register_button.place(x=300, y=450, width=50, height=20)
        self.color_widget_bg() # delete the gray bg of widgets

    def locationsPage(self):
        self.clear_window()
        self.show_back_button(self.login_page)
        info_label = Label(text="Select your bike station: ")
        info_label.place(x=150, y=50)
        info_label.configure(font=14)
        marker = PhotoImage(file="./resources/location_icon.png")
        label_image = Label(image=marker)
        label_image.image = marker  # keep a reference
        label_image.place(x=180, y=90, width=128, height=128)
        # Asking server for location names in the "Locations" table
        locations = self.getLocations()
        # ------- place the button -------------
        start_y = 250
        width = 200
        height = 25
        x = 150
        for i in range(len(locations)):
            start_y += 50
            button_tmp = Button(text=locations[i][0], command=lambda location_id=locations[i][1]: self.bike_list_page(location_id)) # bike_list_page(locations[i][1]) = Location id
            button_tmp.place(x=x, y=start_y, width=width, height=height)
            button_tmp.configure(font=14)
            button_tmp.configure(background="#98FB98")
        self.color_widget_bg() # delete the gray bg of widgets

    def bike_list_page(self, location_id):  # location indexed from 0..
        self.start_location_id = location_id
        # clientSocket.sendall(json.dumps('{"GET_COLUMNS_IN_TABLE", {"Bikes", "id, location_id"}}').encode('UTF-8'))
        # clear_window()
        # create a canvas object and a vertical scrollbar for scrolling it

        vscrollbar = Scrollbar(self.window, orient='vertical')
        vscrollbar.pack(side='right', fill='y', expand='False')
        canvas = Canvas(self.window, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill="both", expand="True")
        vscrollbar.config(command=canvas.yview)
        canvas.configure(bg = "white")
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        interior = Frame(canvas)
        interior.configure(bg = "white")
        self.window.interior = interior
        interior_id = canvas.create_window(0, 0, window=interior, anchor='nw')

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

        self.draw_bikes_button_page(location_id)  # if it's an operator should draw operator_buttons
        self.show_back_button(self.locationsPage)

    def timer(self, s_initial, time_label):
        if self.sec_backup is None:
            s = int(strftime("%S"))
        else:
            s = (int(strftime("%S")) + self.sec_backup) % 60
        if self.sec_backup is None:
            s = (int(strftime("%S")))
        else:
            s = (int(strftime("%S")) + self.sec_backup) % 60
        if s < s_initial:
            self.sec = s + 60 - s_initial
        else:
            self.sec = s - s_initial

        if self.sec == 0 and self.first_timer == False:
            self.minutes = (self.minutes + 1) % 60
            if self.minutes == 0:
                self.hours = (self.hours + 1) % 60
        else:
            self.first_timer = False

        time_label.configure(text=str(self.hours) + ":" + str(self.minutes) + ":" + str(self.sec))
        time_label.after(1000, lambda: self.timer(s_initial, time_label))

    def timer_page(self):
        self.clear_window()

        title = Label(text="Your trip has started", font=('Helvetica', 18))
        title.place(x=140, y=70)

        time_title = Label(text="H :   M:   S:", font=('Helvetica', 18))
        time_title.place(x=180, y=180)

        time_label = Label(text="", font=('Helvetica', 48), fg='red')
        time_label.place(x=170, y=210)

        return_button = Button(text="Return Bike", command=lambda: self.trip_summary_page(self.hours, self.minutes, self.sec),
                               font=('Helvetica', 12))
        return_button.place(x=150, y=400, width=200, height=25)
        return_button.configure(background="#66A1DC")

        self.timer(int(strftime("%S")), time_label)
        self.color_widget_bg() # delete the gray bg of widgets

    def draw_bikes_button_page(self, location_id):
        # This is the db code
        bikes = self.getBike(location_id)
        # ------- bikes button -------------------
        for i, bike in enumerate(bikes):
            current_bike_text = 'Bike-' + str(bike[0])
            reported_status = bike[6]
            btn = Button(self.window.interior, height=1, width=20, text=current_bike_text, bg='#61ED6C',
                         command=lambda b_id=bike[0]: self.openlink(b_id))
            if reported_status == 'True':
                btn.config(state='disabled', bg='#EA5C5C')
            btn.pack(padx=10, pady=5, side="top")
            
#Deprecated
    def draw_operator_buttons(self, stationId):
        # ....... connect to db here
        bikelist = ["Bike", "Bike", "Bike", "Bike", "Bike", "Bike", "Bike", "Bike", "Bike", "Bike", "Bike", "Bike",
                    "Bike", "Bike", "Bike"]
        for i, x in enumerate(bikelist):
            btnwrapper = Frame(self.window.interior)

            bike_label = Label(btnwrapper, height=1, width=10, relief=RIDGE,
                               bg="gray99", fg="black",
                               font="Dosis", text=bikelist[i])

            repair = Button(btnwrapper, height=1, width=10, relief=RIDGE,
                            bg="gray99", fg="black",
                            font="Dosis", text="Repair",
                            command=lambda i=i: self.repair_bike_popup(bikelist[i]))

            move = Button(btnwrapper, height=1, width=10, relief=RIDGE,
                          bg="gray99", fg="black",
                          font="Dosis", text="Move",
                          command=lambda i=i: self.move_bike_popup(bikelist[i]))

            bike_label.pack(padx=0, pady=10, side="left")
            repair.pack(padx=0, pady=5, side="left")
            move.pack(padx=0, pady=5, side="left")
            btnwrapper.pack(side="top")

    def openlink(self, bike_id):
        self.bike_id = bike_id
        popup = Toplevel(self.window)
        popup.configure(bg='white') 
        w = 250  # width for the Tk root
        h = 100  # height for the Tk root
        ws = self.window.winfo_vrootwidth()  # width of root window
        hs = self.window.winfo_vrootheight()  # height of the root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window
        popup.grab_set()
        l1 = Label(popup, text="Confirm Selection?")
        l1.pack(fill="y")
        l1.configure(bg = "white")
        l2 = Label(popup, text='Bike-' + str(bike_id))
        l2.pack(fill="y")
        l2.configure(bg="white")
        go_to = "open_reporter"
        go_to2 = "timer_page"

        r = Button(popup, height=1, width=10, text="Report Bike", command=lambda p=popup: self.popup_release(popup, go_to))
        r.pack(side="left", padx=30)
        r.configure(background="#F8F8F8")
        n = Button(popup, height=1, width=10, text="Confirm", command=lambda bid=bike_id: self.confirmBike(popup, go_to2, bid))
        n.pack(side="right", padx=15)
        n.configure(background="#F8F8F8")
        
        popup.mainloop()

    def confirmBike(self, popup, go_to2, bike_id):
        self.bike_id = bike_id
        self.rentBike(bike_id, datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"), self.username)
        thread_sendloc = threading.Thread(target=self.sendLocation, args=(bike_id, ))
        thread_sendloc.start()
        self.popup_release(popup, go_to2)

    def repair_bike_popup(self, i):
        popup = Toplevel(self.window)
        w = 250  # width for the Tk root
        h = 100  # height for the Tk root
        ws = self.window.winfo_vrootwidth()  # width of root window
        hs = self.window.winfo_vrootheight()  # height of the root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window
        popup.grab_set()
        l1 = Label(popup, text="Confirm sending bike to service?")
        l1.pack(fill="y")
        l2 = Label(popup, text=i)
        l2.pack(fill="y")
        go_to = ""

        n = Button(popup, height=1, width=10, text="Confirm", command=lambda p=popup: self.popup_release(popup, go_to))
        n.pack(side="top", padx=15, pady=15)
        popup.mainloop()

    def move_bike_popup(self, i):
        popup = Toplevel(self.window)
        w = 250  # width for the Tk root
        h = 150  # height for the Tk root
        ws = self.window.winfo_vrootwidth()  # width of root window
        hs = self.window.winfo_vrootheight()  # height of the root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window
        popup.grab_set()
        l1 = Label(popup, text="Confirm moving bike to another location?")
        l1.pack(fill="y")

        l2 = Label(popup, text=i)
        l2.pack(fill="y")

        go_to = ""

        opt = StringVar(popup)
        selection_info = "Select next location "
        opt.set(selection_info)
        next_location_menu = OptionMenu(popup, opt, "Location A", "Location B", "Location C")
        next_location_menu.pack(side="left", padx=10)

        n = Button(popup, height=1, width=10, text="Confirm", command=lambda p=popup: self.popup_release(popup, go_to))
        n.pack(side="right", padx=10)
        popup.mainloop()

    def popup_release(self, master, go_to):
        master.grab_release()
        master.destroy()

        if go_to == "locationsPage":
            self.locationsPage()
        elif go_to == "open_reporter":
            self.open_reporter()
        elif go_to == "timer_page":
            self.timer_page()

    def open_reporter_sendError(self, popup, go_to,bike_id, user_id, location_id, error_type, date):
        self.sendReport(bike_id, user_id, location_id, error_type, date)
        # ---- go back to locations page --------
        self.popup_release(popup, go_to)

    def open_reporter(self):
        popup = Toplevel(self.window)
        popup.configure(bg='white') 
        w = 300  # width for the Tk root
        h = 100  # height for the Tk root
        ws = self.window.winfo_vrootwidth()  # width of root window
        hs = self.window.winfo_vrootheight()  # height of the root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        popup.geometry('%dx%d+%d+%d' % (w, h, x, y))  # place the popup in the middle of the window

        popup.grab_set()

        go_to = "locationsPage"
        # ----------------------------
        hint_reporter = StringVar(popup)
        report_type = ["Tire pressure leaked", "Tire damaged", "Bike not working",
                                      "Bike dirty", "Component missed", "Other"]
        selection_info = "Select an issue"
        hint_reporter.set(selection_info)
        endlocation_menu = OptionMenu(popup, hint_reporter, *report_type)
        endlocation_menu.pack()
        endlocation_menu.configure(font=self.my_font, bg = "#F8F8F8" )
        # ---------------------------

        message_label = Label(popup, text="Your report will be submitted to our system.")
        message_label.pack(fill="y")
        message_label.configure(bg="white")

        confirm_btn = Button(popup, height=1, width=10, text="Confirm",
                             command=lambda b_id=self.bike_id, u_id=self.username, l_id=self.start_location_id,
                             d=datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S"):
                             self.open_reporter_sendError(popup, go_to, b_id, u_id, l_id, hint_reporter.get(), d))
        confirm_btn.pack()
        popup.mainloop()


    # billing screen
    def trip_summary_page(self, hours, minutes, sec):
        self.sec_backup = None
        self.clear_window()
        tripend_label = Label(text="Trip Summary")
        tripend_label.place(x=180, y=30)
        tripend_label.configure(font=self.title_font)
        # for displaying end time / trip duration
        time_label = Label(text="", font=('Helvetica', 48), fg='red')
        endtime_label = Label(
            text="Duration: " + str(hours) + " : " + str(minutes) + " : " + str(sec) + "",
            font=('Helvetica', 48), fg='red')  # (textvariable=end_loc)
        endtime_label.place(x=150, y=100, width=230, height=50)
        endtime_label.configure(font=self.my_font)
        # payment
        # setting payment to label, 0.2 pounds each second
        self.payment = round(sec*0.2 + minutes*60*0.2 + hours*3600*0.2, 2)
        pay_label = Label(text="Bill: £ {} ".format(self.payment))
        pay_label.place(x=150, y=200, width=200, height=25)
        pay_label.configure(font=self.my_font)
        # dropdown for endloc
        hint = StringVar()
        selection_info = "Select ending location "
        hint.set(selection_info)
        endlocation_menu = OptionMenu(self.window, hint, "1-Partick", "2-Glasgow Uni", "3-Glasgow City Centre", "4-Buchanan Bus Station")
        endlocation_menu.place(x=140, y=300, width=250)
        endlocation_menu.configure(font=self.my_font)

        pay_button = Button(text="Pay", command=lambda: self.verify_location(hours, minutes, sec, hint.get(), selection_info))
        pay_button.place(x=200, y=420, width=120, height=30)
        pay_button.configure(font=self.my_font)
        pay_button.configure(background="#66A1DC")
        
        self.color_widget_bg()

    def verify_location(self, h, m, s, sel, sel_info):
        self.duration = "{}:{}:{}".format(h, m, s)
        
        if sel == sel_info:
            self.trip_summary_page(h, m, s)
            register_label = Label(text="Please select the ending location!")
            register_label.place(x=170, y=370)
            register_label.configure(fg="red")
        else:
            self.return_location_id = int(sel.split('-')[0])
            self.open_pay()
        
        self.color_widget_bg()

    def open_pay(self, ):
        self.clear_window()
        # (mobile,bike_id,duration,bill, start_location_id, return_location_id,date)
        payment_state = self.payBill(self.username, self.bike_id, self.duration, self.payment, self.start_location_id, self.return_location_id, datetime.datetime.now().strftime("%Y/%m/%d"))
        self.returnBike(self.bike_id, self.return_location_id, self.username, )
        payment_state = round(float(payment_state), 2)
        if payment_state > 0:
            statment_label1 = Label(text="Payment Successfull.",  font=('Helvetica', 14))
        else:
            statment_label1 = Label(text="Payment Successful. Please top-up.",  font=('Helvetica', 14))
        self.reset_timer()
        statment_label1.place(x=150, y=150)
        statment_label1.configure(font=self.my_font)
        statment_label2 = Label(text="Balance: " + str(payment_state))
        statment_label2.place(x=180, y=180)
        statment_label2.configure(font=self.my_font)
        # ----- complete trip button ----
        back_button = Button(text="Complete Trip", command=self.locationsPage)
        back_button.place(x=300, y=350, width=120, height=30)
        back_button.configure(font=self.my_font)
        # ----- report bike button ----
        report_button = Button(text="Report Bike", command=self.open_reporter)
        report_button.place(x=100, y=350, width=120, height=30)
        report_button.configure(font=self.my_font)
        report_button.configure(font=self.my_font)
