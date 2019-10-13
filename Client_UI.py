##################################################### FIRST PAGE ##################################################
from Client import *
from tkinter import *
from tkinter.font import Font
from time import strftime
import math
client_connect_server()


def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def show_back_button(previous_page):
    back_button = Button(text="<<", command=previous_page)
    back_button.place(x=10, y=10, width=50, height=25)
    back_button.configure(background="#66A1DC")


def map_page():
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

    locationA_button = Button(text="Location A", command=clear_window)
    locationA_button.place(x=150, y=start_y + 50, width=200, height=25)
    locationA_button.configure(font=14)
    locationA_button.configure(background="#98FB98")

    locationB_button = Button(text="Location B", command=clear_window)
    locationB_button.place(x=150, y=start_y + 100, width=200, height=25)
    locationB_button.configure(font=14)
    locationB_button.configure(background="#98FB98")

    locationC_button = Button(text="Location C", command=clear_window)
    locationC_button.place(x=150, y=start_y + 150, width=200, height=25)
    locationC_button.configure(font=14)
    locationC_button.configure(background="#98FB98")

#
def clientLogin(un, pw):
    login_package = '%s %s' % (un, pw)               # the user may sent space will hence error here
    clientSocket.send(b'verify_login')
    clientSocket.recv(BUFSIZE)                      # receive the 'verify'
    clientSocket.send(bytes(login_package.encode('utf-8')))
    login_state = clientSocket.recv(BUFSIZE)
    login_state = login_state.decode('utf-8')

    if login_state == "USER_NOT_EXIST":
        register_label = Label(text="The user not exists!")
        register_label.place(x=150, y=220)
        register_label.configure(fg="red")
    elif login_state == "USER_NOT_VERIFIED":
        register_label = Label(text="The user and password don't match!")
        register_label.place(x=150, y=220)
        register_label.configure(fg="red")
    elif login_state == "USER_VERIFIED":
        map_page()


def registerClient(un, pw):
    # the user may sent space will hence error here
    regis_package = '%s %s' % (un, pw)
    clientSocket.send(b'register')
    clientSocket.recv(BUFSIZE)  # receive the 'register' package
    # ---------- register to db ---------
    clientSocket.send(bytes(regis_package.encode('utf-8')))
    regis_state = clientSocket.recv(BUFSIZE)
    regis_state = regis_state.decode('utf-8')
    # --------------------------------------
    if regis_state == "USER_REGISTERD":
        register_label = Label(text="The user already exists!")
        register_label.place(x=150, y=220)
        register_label.configure(fg="red")
    elif regis_state == "USER_REGISTERD":
        map_page()


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
#         map_page()
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


def return_bike_page(hours, minutes):
    print(hours, minutes)
    


def timmer(s_initial, time_label):
    global first_timmer
    global minutes
    global hours
    
    s = int(strftime("%S"))
    
    if s < s_initial:
        sec = s + 60 - s_initial
    else:
        sec = s - s_initial

    if sec == 0 and first_timmer == False:
        minutes = (minutes + 1) % 60
        if minutes == 0:
            hours = (hours + 1) % 60
    else:
        first_timmer = False
        
    time_label.configure(text = str(hours) + ":" + str(minutes) + ":" + str(sec)  )
    time_label.after(1000, lambda: timmer(s_initial, time_label) )

def timmer_page():
    
    title = Label(text = "Your trip has started", font = ('Helvetica', 18))
    title.place(x = 140, y = 70)

    time_title = Label(text="H :   M:   S:", font = ('Helvetica', 18) )
    time_title.place(x = 180, y = 180)

    time_label = Label(text="", font = ('Helvetica', 48), fg='red')
    time_label.place(x = 170, y = 210)

    return_button = Button(text = "Return Bike", command = lambda: return_bike_page(hours, minutes), font = ('Helvetica', 12))
    return_button.place(x = 150, y = 400, width = 200, height = 25)

    timmer( int(strftime("%S")), time_label )

######## main #########
    
def main_page():
    window.title("BikeSharing")
    window.geometry("500x530")
    global my_font
    my_font = Font(size=12)
    login_page()
    window.mainloop()

window = Tk()
minutes = 0
hours = 0
first_timmer = True
main_page()


