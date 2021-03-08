import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import messagebox
import PIL
from PIL import Image, ImageTk
from functools import partial
import datetime
import tkinter.font as font
import re


# sindesi sto database
db = mysql.connector.connect(host="  ###ip####    ",
                             user='   #####username####  ',
                             password=' #####password##### ',

                             db="   ###database_name#####   ")

# buttons back


def Back():
    root.destroy()
    welcomeWindow()


def Back2():
    root2.destroy()
    welcomeWindow()


def Back3():
    root1.destroy()
    mainWindow()
####

# ta inserts pou ginontai sto database otan o pelatis kanei mia paraggelia


def MakeOrder():
    root1.destroy()

    def logintodb_order(ordered, phone, pay, paymethod, orderBefore):

        cursor = db.cursor()
        print('db connected')

        if orderBefore == 0:

            if ordered and fn and ln and add and phone and pay and paymethod:
                try:

                    sql = "INSERT INTO Customer (last_name,first_name,address,phone) VALUES (%s,%s,%s,%s)"
                    recordTuple_customer = (ln, fn, add, phone)
                    cursor.execute(sql, recordTuple_customer)

                    sql = "INSERT INTO Restaurant_Customer_Association (idRestaurant,idCustomer) VALUES (%s,(SELECT idCustomer from Customer WHERE phone=%s))"
                    recordTuple_association = (restaurant_selected[0], phone)
                    cursor.execute(sql, recordTuple_association)
                    sql = "INSERT INTO Delivery (delivery_time,idCustomer) VALUES (%s,(SELECT idCustomer from Customer WHERE phone=%s))"
                    recordTuple_delivery = (datetime.datetime.now(), phone)
                    cursor.execute(sql, recordTuple_delivery)

                    sql = """INSERT INTO project_db20_up1046879.Order (order_type,order_date,idDelivery) VALUES 
                    (%s,%s,(SELECT idDelivery from Delivery where idCustomer in (SELECT idCustomer from Customer WHERE phone=%s)))"""

                    recordTuple_order_info = (
                        'delivery', datetime.datetime.now(), phone)
                    cursor.execute(sql, recordTuple_order_info)
                    i = 0
                    # emfwleymeni epanalipsi opou gia kathe proion vlepw poses fores uparxei
                    for i in range(len(ordered)):

                        x = re.findall(r"\d", str(ordered[i]))
                        s = ""
                        s = s.join(x[0])  # pairnw id

                        for j in range(len(ordered)):
                            # sygkrinw an to id yparxei sto leksiko mou kai pairnw tin epomeni poy deixnei to quantity
                            if list(my_dict.items())[j][0] == int(s):
                                q = list(my_dict.items())[
                                    j][1]  # pairnw to quantity

                        sql = """INSERT INTO Order_item (availability,item_quantity,idOrder,idMenu_item) VALUES 
                        (%s,%s,
                        (SELECT idOrder from project_db20_up1046879.Order  orderr inner join project_db20_up1046879.Delivery  
                        deliveryy on orderr.idDelivery=deliveryy.idDelivery inner join Customer on 
                        Customer.idCustomer=deliveryy.idCustomer where Customer.phone=%s ),%s);"""
                        recordTuple_order_item = ('yes', q, phone, s)
                        cursor.execute(sql, recordTuple_order_item)
                    sql = "INSERT INTO Payment (total_amount,date,pay_Method,idOrder) VALUES (%s,%s,%s,(SELECT idOrder from project_db20_up1046879.Order  orderr inner join project_db20_up1046879.Delivery  deliveryy on orderr.idDelivery=deliveryy.idDelivery inner join Customer on Customer.idCustomer=deliveryy.idCustomer where Customer.phone=%s ))"
                    recordTuple_pay = (
                        pay, datetime.datetime.now(), paymethod, phone)

                    cursor.execute(sql, recordTuple_pay)
                    db.commit()

                    print("Query Executed successfully")

                except:

                    db.rollback()
                    print("Error occured")

        else:
            try:
                try:
                    sql = """select count(idCustomer) from Delivery 
                    where Delivery.idCustomer in (SELECT idCustomer from Customer WHERE phone=%s) group by idCustomer ;"""
                    recordTuple_discount = (phone,)
                    cursor.execute(sql, recordTuple_discount)
                    payments = cursor.fetchall()
                    for dis in payments:
                        print(dis[0])
                    if int(dis[0]) % 6 == 0:
                        discount = 0.2  # the customer has a discount 20%
                    else:
                        discount = 0
                except:
                    discount=0

                sql = "INSERT INTO Delivery (delivery_time,idCustomer) VALUES (%s,(SELECT idCustomer from Customer WHERE phone=%s))"
                recordTuple_delivery = (datetime.datetime.now(), phone)
                cursor.execute(sql, recordTuple_delivery)

                sql = """INSERT INTO project_db20_up1046879.Order (order_type,order_date,idDelivery) VALUES 
                    (%s,%s,(SELECT idDelivery from Delivery where idCustomer in (SELECT idCustomer from Customer WHERE phone=%s) order by idDelivery desc limit 1))"""

                recordTuple_order_info = (
                    'delivery', datetime.datetime.now(), phone)
                cursor.execute(sql, recordTuple_order_info)
                i = 0

                for i in range(len(ordered)):

                    x = re.findall(r"\d", str(ordered[i]))
                    s = ""
                    s = s.join(x[0])

                    for j in range(len(ordered)):
                        if list(my_dict.items())[j][0] == int(s):
                            q = list(my_dict.items())[j][1]

                    sql = """INSERT INTO Order_item (availability,item_quantity,idOrder,idMenu_item) VALUES 
                        (%s,%s,
                        (SELECT idOrder from project_db20_up1046879.Order  orderr inner join project_db20_up1046879.Delivery  
                        deliveryy on orderr.idDelivery=deliveryy.idDelivery inner join Customer on 
                        Customer.idCustomer=deliveryy.idCustomer where Customer.phone=%s order by idOrder desc limit 1 ),%s);"""
                    recordTuple_order_item = ('yes', q, phone, s)
                    cursor.execute(sql, recordTuple_order_item)
                sql = "INSERT INTO Payment (total_amount,discount,date,pay_Method,idOrder) VALUES (%s,%s,%s,%s,(SELECT idOrder from project_db20_up1046879.Order  orderr inner join project_db20_up1046879.Delivery  deliveryy on orderr.idDelivery=deliveryy.idDelivery inner join Customer on Customer.idCustomer=deliveryy.idCustomer where Customer.phone=%s order by idOrder desc limit 1 ))"
                recordTuple_pay = (pay-pay*discount, discount,
                                   datetime.datetime.now(), paymethod, phone)

                cursor.execute(sql, recordTuple_pay)
                db.commit()

                print("Query Executed successfully")

            except:

                db.rollback()
                print("The user with that phone number does not exist")

    # energeies pou ginontai otan o pelatis pathsei to koumpi submit

    def submitact():
        results = order_items  # me duplicates
        ordered = list(set(order_items_id))  # xwris duplicates
        paymethod = payment_input.get()

        phone = phone_input.get()

        i = 0
        pay = 0
        for i in range(len(results)):

            x = re.findall(r"\d", str(results[i]))
            x.remove(x[0])

            s = ""
            s = s.join(x)
            # prosthetw oles tis times pou katagrafontai sti lista results
            pay = pay+int(s)
        if orderBefore == 0:

            global fn
            global ln
            global add

            fn = firstname_input.get()
            ln = lastname_input.get()
            add = address_input.get()

        logintodb_order(ordered, phone, pay, paymethod, orderBefore)
        lbl = Label()
        lbl.place(x=400, y=300)
        lbl.configure(text='Your order has been submitted')

    # sxediasmos parathyrou paraggelias
    global root
    root = tk.Tk()
    windowWidth = root.winfo_reqwidth()+400
    windowHeight = root.winfo_reqheight()+350

    # pairnw misa parathyrou kai othonis
    positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

    # kentrarw parathyro
    root.geometry("+{}+{}".format(positionRight, positionDown))
    root.geometry("700x500")
    root.title("Your Order")

    # inputs poy simplirwnei o pelatis
    if orderBefore == 0:
        phone = tk.Label(root,  font='Helvetica 10 bold', text="Phone -")
        phone.place(x=350, y=80)

        phone_input = tk.Entry(root, width=35)
        phone_input.place(x=440, y=80, width=100)

        firstname = tk.Label(root, font='Helvetica 10 bold', text="Firstame -")
        firstname.place(x=50, y=80)

        firstname_input = tk.Entry(root, width=35)
        firstname_input.place(x=140, y=80, width=100)

        lastname = tk.Label(root, font='Helvetica 10 bold', text="Lastname -")
        lastname.place(x=50, y=120)

        lastname_input = tk.Entry(root, width=35)
        lastname_input.place(x=140, y=120, width=100)

        payment = tk.Label(root, font='Helvetica 10 bold', text="Payment -")
        payment.place(x=350, y=120)

        payment_input = tk.Entry(root, width=35)
        payment_input.place(x=440, y=120, width=100)
        adress = tk.Label(root, font='Helvetica 10 bold', text="Address - ")
        adress.place(x=50, y=160)

        address_input = tk.Entry(root, width=35)
        address_input.place(x=140, y=160, width=100)

    else:
        phone = tk.Label(root, font='Helvetica 10 bold', text="Phone -")
        phone.place(x=50, y=80)

        phone_input = tk.Entry(root, width=35)
        phone_input.place(x=120, y=80, width=100)
        payment = tk.Label(root, font='Helvetica 10 bold', text="Payment -")
        payment.place(x=350, y=80)

        payment_input = tk.Entry(root, width=35)
        payment_input.place(x=440, y=80, width=100)

    submitbtn = tk.Button(root, text="Submit",
                          bg='coral', command=submitact)
    submitbtn.place(x=440, y=180, width=100)
    order_label = tk.Label(root, font=7, text='You have ordered nothing yet')
    order_label.place(x=320, y=265)

    goback = tk.Button(root, text="Back",
                       bg='sandy brown', command=Back)
    goback.place(x=600, y=455, width=80)

    # sindesi sto database
    cursor = db.cursor()
    cursor.execute('SELECT idMenu_item,item_name,item_price FROM Menu_item')
    menu_items = cursor.fetchall()

    k = 0
    order_items = []
    order_items_id = []

    def root_close():
        cursor.close()

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", root_close)

    # me to patima tou koumpiou (+) ginetai prosthiki selected proiontos se mia lista
    def addtomenu():
        try:
            for index in Lb1.curselection():  # pairnw to epilegmeno item
                item = [Lb1.get(index)]
                order_items.append(item)

            i = 0
            for i in range(len(order_items)):

                x = re.findall(r"\d", str(order_items[i]))
                s = ""
                s = s.join(x[0])  # eksagw to id tou

            order_items_id.append(int(s))  # vazw ola ta id se mia lista
            global my_dict
            # posotites proiontwn!!
            my_dict = {i: order_items_id.count(i) for i in order_items_id}

            order_label.config(text=my_dict)
            removeitem = tk.Button(root, text="-",
                                   bg='sandy brown', command=removefromMenu)
            removeitem.place(x=255, y=200, width=30)
        except UnboundLocalError:
            print("You haven't selected anything")

    # me to patima tou koumpiou (-) ginetai afairesi teleytaiou proiontos apo ti lista
    def removefromMenu():
        try:
            for index in Lb1.curselection():
                item = [Lb1.get(index)]
                order_items.append(item)

            order_items_id.remove(order_items_id[len(order_items_id)-1])
            global my_dict
            # posotites proiontwn!!
            my_dict = {i: order_items_id.count(i) for i in order_items_id}

            order_label.config(text=my_dict)

        except IndexError:
            print('the list is empty')
            order_label.config(text='The list is empty')

    # emfanizw ta menu items ston pelath mesa se listbox gia na epileksei
    myFont1 = font.Font(size=13)
    Lb1 = Listbox(root, width=14, font=myFont1)
    for item in menu_items:

        Lb1.insert(k, item)
        additem = tk.Button(root, text="+",
                            bg='navajo white', command=addtomenu)
        additem.place(x=220, y=200, width=30)
        Lb1.pack()
        Lb1.place(x=120, y=215)
        k = k+1

    root.mainloop()


def orderAgain():
    result = tk.messagebox.askquestion(
        "Check", "Are you already a customer?", icon='question')
    global orderBefore
    if result == 'yes':

        orderBefore = TRUE
        root3.destroy()
        welcomeWindow()
    else:
        orderBefore = FALSE
        root3.destroy()
        welcomeWindow()


# parathyro kleisimatos trapeziou
def MakeReservation():

    root1.destroy()
    global root2
    root2 = tk.Tk()

    # ta inserts poy ginontai sti vasi
    def logintodb_table(phone, people, table):

        if orderBefore == 0:
            if fn and ln and phone and people and table:
                try:

                    sql = "INSERT INTO Customer (last_name,first_name,phone) VALUES (%s,%s,%s)"
                    recordTuple_customer = (ln, fn, phone)
                    cursor.execute(sql, recordTuple_customer)
                    sql = "INSERT INTO Reservation (people_amount,reserve_datetime,idTable,idCustomer) VALUES (%s,%s,%s,(SELECT idCustomer from Customer WHERE phone=%s))"
                    recordTuple_reservation = (
                        people, datetime.datetime.now(), table, phone)
                    cursor.execute(sql, recordTuple_reservation)

                    sql = "INSERT INTO Restaurant_Customer_Association (idRestaurant,idCustomer) VALUES (%s,(SELECT idCustomer from Customer WHERE phone=%s))"
                    recordTuple_association = (restaurant_selected[0], phone)
                    cursor.execute(sql, recordTuple_association)
                    db.commit()

                    print("Query Executed successfully")

                except:
                    db.rollback()
                    print("Error occured")
        else:
            try:

                sql = "INSERT INTO Reservation (people_amount,reserve_datetime,idTable,idCustomer) VALUES (%s,%s,%s,(SELECT idCustomer from Customer WHERE phone=%s))"
                recordTuple_reservation = (
                    people, datetime.datetime.now(), table, phone)
                cursor.execute(sql, recordTuple_reservation)

               

                print("Query Executed successfully")

            except:

                db.rollback()
                print("Error occured")

    # energeies me to patima tou koumpiou 'Submit'

    def submitact():

        people = people_amount_input.get()
        phone = phone_input.get()
        table = Lb.get(Lb.curselection())[0]
        if orderBefore == 0:
            global fn, ln
            fn = firstname_input.get()
            ln = lastname_input.get()

        logintodb_table(phone, people, table)
        lbl = Label()
        lbl.place(x=400, y=300)
        lbl.configure(text='Your order has been submitted')

    # sxediasmos parathyrou kratisis

    windowWidth = root2.winfo_reqwidth()+400
    windowHeight = root2.winfo_reqheight()+350

    # pairnw misa othonis kai parathyrou
    positionRight = int(root2.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root2.winfo_screenheight()/2 - windowHeight/2)

    # kentrarw othoni
    root2.geometry("+{}+{}".format(positionRight, positionDown))
    root2.geometry("700x500")
    root2.title("Your Reservation")

    # ta inputs poy symplirwnei o pelatis
    if orderBefore == 0:
        firstname = tk.Label(
            root2, font='Helvetica 10 bold', text="Firstame -")
        firstname.place(x=50, y=80)

        firstname_input = tk.Entry(root2, width=35)
        firstname_input.place(x=140, y=80, width=100)

        phone = tk.Label(root2,  font='Helvetica 10 bold', text="Phone -")
        phone.place(x=350, y=80)

        phone_input = tk.Entry(root2, width=35)
        phone_input.place(x=420, y=80, width=100)

        lastname = tk.Label(
            root2,  font='Helvetica 10 bold', text="Lastname -")
        lastname.place(x=50, y=120)

        lastname_input = tk.Entry(root2, width=35)
        lastname_input.place(x=140, y=120, width=100)
        people_amount = tk.Label(
            root2, font='Helvetica 10 bold', text="People -")
        people_amount.place(x=350, y=120)

        people_amount_input = tk.Entry(root2, width=35)
        people_amount_input.place(x=420, y=120, width=100)
    else:
        phone = tk.Label(root2, font='Helvetica 10 bold', text="Phone -")
        phone.place(x=50, y=80)

        phone_input = tk.Entry(root2, width=35)
        phone_input.place(x=120, y=80, width=100)
        people_amount = tk.Label(
            root2, font='Helvetica 10 bold', text="People -")
        people_amount.place(x=350, y=80)

        people_amount_input = tk.Entry(root2, width=35)
        people_amount_input.place(x=420, y=80, width=100)
    submitbtn = tk.Button(root2, text="Submit",
                          bg='coral', command=submitact)
    submitbtn.place(x=250, y=170, width=100)
    selected = tk.Label(root2, font='8', text='No table is selected')
    selected.place(x=300, y=250)

    goback = tk.Button(root2, text="Back",
                       bg='sandy brown', command=Back2)
    goback.place(x=600, y=455, width=80)

    # syndeomai sti vasi kai emfanizw ta trapezia ston pelati
    cursor = db.cursor()
    print('db connected')
    sql = 'SELECT idTable,chairs_number,Description FROM project_db20_up1046879.Table where status=0 and idRestaurant=%s'
    idRes = (restaurant_selected[0],)
    cursor.execute(sql, idRes)
    tables = cursor.fetchall()

    myFont1 = font.Font(size=13)
    Lb = Listbox(root2, width=16, height=10, font=myFont1)
    k = 0
    for item in tables:

        Lb.insert(k, item)

        # Lb.pack()
        Lb.place(x=120, y=215)
        k = k+1
    # me thn callback otan o pelatis kanei select vlepei dipla se label ti exei epileksei

    def callback(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            selected.configure(
                text='A ' + data[2] + ' table for ' + str(data[1]) + ' people')

    Lb.bind("<<ListboxSelect>>", callback)

    def root2_close():
        cursor.close()

        root2.destroy()

    root2.protocol("WM_DELETE_WINDOW", root2_close)

# parathyro kalwsorismatos


def welcomeWindow():
    global root1
    root1 = tk.Tk()
    image = Image.open(r'resizewelcome.jpg')
    photo_image = ImageTk.PhotoImage(image)
    label = tk.Label(root1, image=photo_image)
    label.pack()
    # vazw to parathyro sto kentro tis othonis mou
    windowWidth = root1.winfo_reqwidth()+400
    windowHeight = root1.winfo_reqheight()+350

    positionRight = int(root1.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root1.winfo_screenheight()/2 - windowHeight/2)

    root1.geometry("+{}+{}".format(positionRight, positionDown))
    ##################

    root1.geometry("700x500")
    root1.title("Welcome" + '(' + restaurant_selected[2] + ')')

    lbl = Label(font='Helvetica 20 bold', bg='red3',
                relief=GROOVE, text="Welcome to our restaurant")
    lbl.place(x=160, y=40, width=400)

    contact = Label(font='Helvetica 10 italic bold', bg='sandy brown',
                    text='Contact us:' + ' ' + restaurant_selected[3])
    contact.place(x=2, y=477)
    makeorder = tk.Button(root1,  text="Μake your order", font=5,
                          bg='sandy brown', command=MakeOrder)
    makeorder.place(x=230, y=135, width=200)

    makeReservation = tk.Button(root1, text="Μake a reservation", font=5,
                                bg='navajo white', command=MakeReservation)
    makeReservation.place(x=230, y=195, width=200)
    mostPopular = Label(font='Helvetica 14 italic underline bold',
                        bg='firebrick1', relief=GROOVE, text='Top Choices')
    mostPopular.place(x=90, y=270, width=200)
    offer = Label(font='Helvetica 14 italic underline bold',
                  bg='firebrick1', relief=GROOVE, text='Special Offer')
    offer.place(x=360, y=270, width=200)
    offertext = Label(font='Helvetica 14 italic  ', relief='ridge', bg='navajo white', wraplength=200,
                      justify='left', text='If you make more than 6 orders, you get a 20' + '% ' + 'discount!')
    offertext.place(x=360, y=310, width=200)
    goback = tk.Button(root1, text="Back",
                       bg='sandy brown', command=Back3)
    goback.place(x=600, y=455, width=80)
    food = db.cursor()
    mysql = """SELECT count(Menu_item.idMenu_item),item_name FROM project_db20_up1046879.Order_item
      inner join Menu_item on Menu_item.idMenu_item=Order_item.idMenu_item group by item_name limit 3;"""

    food.execute(mysql)
    foods = food.fetchall()
    k = 310
    for f in foods:

        p = Label(font='Helvetica 14 italic ',
                  bg='navajo white', relief='ridge', text=f[1])
        p.place(x=120, y=k, width=130)
        k = k+30

    def root1_close():
        food.close()

        root1.destroy()

    root1.protocol("WM_DELETE_WINDOW", root1_close)

    root1.mainloop()


# edw o pelatis dialegei apo poio estiatorio tha paraggeilei h tha kleisei trapezi
def mainWindow():
    global root3
    root3 = tk.Tk()

    image = Image.open(r'rsz_1pexels-life-of-pix-67468dd.jpg')
    photo_image = ImageTk.PhotoImage(image)
    label = tk.Label(root3, image=photo_image)
    label.pack()
    # vazw to parathyro sto kentro tis othonis mou
    windowWidth = root3.winfo_reqwidth()+400
    windowHeight = root3.winfo_reqheight()+350

    positionRight = int(root3.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(root3.winfo_screenheight()/2 - windowHeight/2)

    root3.geometry("+{}+{}".format(positionRight, positionDown))
    ##################

    root3.geometry("700x500")
    root3.title("Restaurant Selection")

    lbl = Label(font='Helvetica 20 bold ', bg='brown3',
                relief=GROOVE, text="Select Restaurant")
    lbl.place(x=170, y=40, width=350)

    restaurant = db.cursor()
    mysql = """SELECT idRestaurant,address,name,phone from Restaurant"""

    restaurant.execute(mysql)
    restaurants = restaurant.fetchall()
    myFont1 = font.Font(size=12)
    Lb = Listbox(root3, width=43, height=5, font=myFont1)
    k = 0

    for r in restaurants:

        Lb.insert(k, r)

        Lb.pack()
        Lb.place(x=150, y=135)
        k = k+1

    # me thn callback otan o pelatis kanei select vlepei dipla se label ti exei epileksei

    def selected(event):

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            global restaurant_selected
            restaurant_selected = event.widget.get(index)

            proceed = tk.Button(root3, text="Proceed", font=5,
                                bg='brown2', command=orderAgain)
            proceed.place(x=270, y=250, width=140)

    Lb.bind("<<ListboxSelect>>", selected)

    def on_closing():
        restaurant.close()

        root3.destroy()

    root3.protocol("WM_DELETE_WINDOW", on_closing)

    root3.mainloop()


mainWindow()
