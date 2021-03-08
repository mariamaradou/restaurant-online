import mysql.connector
from mysql.connector import errorcode
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
from functools import partial



# connect to database
try:
  mydb = mysql.connector.connect(
    host="150.140.186.221",
    user='db20_up1046879',
    password='up1046879',
    database="project_db20_up1046879"
  );
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)


admin_dicitonary={'admin1':'admin'}
mycursor = mydb.cursor(buffered = True,dictionary=True)
mycursor2 = mydb.cursor(buffered = True,dictionary=True)
mycursor3 = mydb.cursor(buffered = True)

#fetch restaurant details (username +password)
mycursor.execute("SELECT * FROM Restaurant")
try:
  for x in mycursor:
        #print(x)
        admin_dicitonary[x['username']] = x['password']
        
except :
  print ("Bug2")
print(admin_dicitonary)

##########################################################################################################

############# statistics functions: ###############
def statisticsfunc(id,window):
    for widget in window.winfo_children():
        widget.destroy()
    myFont0 = font.Font(family='Helvetica',size = 11,weight = 'bold')
    myFont = font.Font(family='Helvetica',size = 11)

  # customers rank of restaurants and total customers in current restaurant:

    Label(window, text ='Customer Statistics',font = myFont0, relief = RAISED).grid(row=1, column= 0, sticky=W)
    mycursor2.execute("SELECT count(idCustomer),idRestaurant from Restaurant_Customer_Association where \
idRestaurant=%s group by idRestaurant",(id,))
    total = mycursor2.fetchone()
    try:
      Label(window,text = 'Total customers in this restaurant: '+str(total['count(idCustomer)']),font = myFont ).grid(row=2,column=0)
    except TypeError : 
      Label(window,text = 'Total customers in this restaurant: 0',font = myFont ).grid(row=2,column=0)

    Label(window,text = 'Restaurants rank (by total customers): ',font = myFont ).grid(row=3,column=0)
    mycursor2.execute("SELECT Restaurant_Customer_Association.idRestaurant, Restaurant.name,count(idCustomer)\
      from Restaurant_Customer_Association inner join Restaurant \
      on Restaurant.idRestaurant = Restaurant_Customer_Association.idRestaurant\
      group by idRestaurant order by count(idCustomer) desc")
    msg = Text(window,font = myFont,height = 5, width = 100 )
    msg.grid(row= 4,column = 0)
    for x in mycursor2:
          stg = 'Restaurant : ' + str(x['idRestaurant'])+ '   '+x['name']+'      Total customers : ' + str(x['count(idCustomer)'])+ '\n' 
          msg.insert(END,stg)

  # traffic fro delivery orders and reservations 
    Label(window, text ='High Traffic Statistics',font = myFont0, relief = RAISED).grid(row=5, column= 0, sticky=W)
    mycursor2.execute ("SELECT count(idDelivery), hour(delivery_time) from Delivery group by hour(delivery_time)\
       order by count(idDelivery) limit 1;")
    deliverytime =  mycursor2.fetchone()
    try:
      Label(window,text = 'High traffic hour - Delivery : '+str(deliverytime['hour(delivery_time)']),font = myFont ).grid(row=6,column=0)
    except TypeError:
      Label(window,text = 'High traffic hour - Delivery : 0',font = myFont ).grid(row=6,column=0)
    
    mycursor2.execute("SELECT count(idReservation), hour(reserve_datetime) from Reservation \
      group by hour(reserve_datetime) order by count(idReservation) limit 1;")
    reservetime = mycursor2.fetchone()
    try:
      Label(window,text = 'High traffic hour - Reservations : '+str(reservetime['hour(reserve_datetime)']),font = myFont ).grid(row=7,column=0)
    except TypeError:
      Label(window,text = 'High traffic hour - Reservations : 0',font = myFont ).grid(row=7,column=0)
  # rank of menu items by how many times they are ordered 
    Label(window, text ='Menu Statistics',font = myFont0, relief = RAISED).grid(row=8, column= 0, sticky=W)
    Label(window,text = 'Menu items rank :',font = myFont ).grid(row=9,column=0)
    mycursor2.execute("SELECT  Menu_item.item_name as name, count(Order_item.idMenu_item) as total \
from Menu_item inner join Order_item on Menu_item.idMenu_item = Order_item.idMenu_item \
group by Menu_item.idMenu_item \
order by total desc")
    msg1 = Text(window,font = myFont,height = 5, width = 20  )
    msg1.grid(row= 10,column = 0)
    for x in mycursor2:
          stg1 = x['name'] + '\n'
          msg1.insert(END,stg1)

  # income by this month and total 
    Label(window, text ='Income Statistics',font = myFont0, relief = RAISED).grid(row=11, column= 0, sticky=W)
    
    mycursor2.execute("SELECT sum(total_amount) as total from Payment where month(date)=month(now())")
    monthlyincome = mycursor2.fetchone()
    Label(window,text = 'Total income (this month) : '+ str(monthlyincome['total']) ,font = myFont ).grid(row=12,column=0)
    mycursor2.execute("SELECT sum(total_amount) as total from Payment where month(date)<=month(now())")
    totalincome = mycursor2.fetchone()
    Label(window,text = 'Total income : '+ str(totalincome['total']) ,font = myFont ).grid(row=13,column=0)



############# orders functions: ###################
######## show orders:
def delivery_orders(id,window):
      for widget in window.winfo_children():
            widget.destroy()
      idorder = []
      ordertype=[]
      orderdate = []
      mycursor2.execute("SELECT * from ((project_db20_up1046879.Order inner join project_db20_up1046879.Order_item\
     on Order.idOrder = Order_item.idOrder) inner join project_db20_up1046879.Delivery on Order.idDelivery = Delivery.idDelivery)\
     inner join Restaurant_Customer_Association on Restaurant_Customer_Association.idCustomer = Delivery.idCustomer \
     where idRestaurant = %s order by order_date desc",(id,))
      i=0
      for x in mycursor2:
        if x['idOrder'] in idorder:
              continue
        idorder.append(x['idOrder'])
        ordertype.append(x['order_type'])
        orderdate.append(x['order_date'])
        stg1 = "Id Order:       Order Type:            Order Date:     \
         \n"+str(x['idOrder'])+'                 '+ x['order_type'] +'                '+ str(x['order_date']) +'\n'
        scroll = Scrollbar(window)
        scroll.grid(column=2, row =2+i, sticky=N+S+W)
        msg = Text(window,relief = RAISED,height = 5, width = 100)
        msg.grid(row = 2+i,column=1)
        scroll.config(command=msg.yview)
        msg.config(yscrollcommand=scroll.set)
        msg.insert(END,stg1)
        i+=1
        # show all order items in current order
        mycursor.execute("SELECT * from ((project_db20_up1046879.Order inner join project_db20_up1046879.Order_item\
     on Order.idOrder = Order_item.idOrder) inner join project_db20_up1046879.Delivery on Order.idDelivery = Delivery.idDelivery)\
     inner join Restaurant_Customer_Association on Restaurant_Customer_Association.idCustomer = Delivery.idCustomer \
     where (idRestaurant = %s and Order.idOrder = %s)",(id,x['idOrder']))
        for y in mycursor:
                stg2 = '\nMenu_item: '+ str(y['idMenu_item'])+'  Quantity: '+str(y['item_quantity']) +\
                    '  Availability: '+ y['availability'] +'\n'
                msg.insert(END,stg2)

def table_orders(id,window):
      for widget in window.winfo_children():
            widget.destroy()
      idorder = []
      ordertype=[]
      orderdate = []
      mycursor2.execute("SELECT * from ((project_db20_up1046879.Order inner join project_db20_up1046879.Order_item\
     on Order.idOrder = Order_item.idOrder) inner join project_db20_up1046879.Table on Order.idTable = Table.idTable)\
     where idRestaurant = %s order by order_date desc",(id,))
      i=0
      for x in mycursor2:
        if x['idOrder'] in idorder:
              continue
        idorder.append(x['idOrder'])
        ordertype.append(x['order_type'])
        orderdate.append(x['order_date'])
        stg1 = "Id Order:       Order Type:            Order Date:     \
         \n"+str(x['idOrder'])+'                 '+ x['order_type'] +'                '+ str(x['order_date']) +'\n'
        scroll = Scrollbar(window)
        scroll.grid(column=2, row =2+i, sticky=N+S+W)
        msg = Text(window,relief = RAISED,height = 5, width = 100)
        msg.grid(row = 2+i,column=1)
        scroll.config(command=msg.yview)
        msg.config(yscrollcommand=scroll.set)
        msg.insert(END,stg1)
        i+=1
        # show all order items in current order
        mycursor.execute("SELECT * from ((project_db20_up1046879.Order inner join project_db20_up1046879.Order_item\
     on Order.idOrder = Order_item.idOrder) inner join project_db20_up1046879.Table on Order.idTable = Table.idTable)\
     where idRestaurant = %s and Order.idOrder = %s",(id,x['idOrder']))
        for x in mycursor:
                stg2 = '\nMenu_item: '+ str(x['idMenu_item'])+'  Quantity: '+str(x['item_quantity']) +\
                    '  Availability: '+ x['availability'] +'\n'
                msg.insert(END,stg2)
        

########### add order:

def add_order2(id,id_entry):
    idtable = id_entry.get()
    mycursor2.execute("INSERT INTO project_db20_up1046879.Order (idTable,order_date,order_type) \
          VALUES(%s,now(),'Sitting' )",(str(idtable),))
    mydb.commit()

# function to return key for any value
def get_key(val,my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key
 
    return "key doesn't exist"
##

def add_to_order(id,value,menu_list,menu_items):
    amount = value.get()
    item = menu_list.get(menu_list.curselection())
    menu_items
    mycursor2.execute("SELECT idOrder from project_db20_up1046879.Order where idDelivery is null order by idOrder desc limit 1 ")
    for x in mycursor2:
          idOrder= x['idOrder']
          break;
          
    idMenu_item = get_key(item,menu_items)
    mycursor2.execute("INSERT INTO Order_item (availability,item_quantity, idOrder,idMenu_item)\
      VALUES ('yes', %s,%s,%s)",(amount,idOrder,idMenu_item))
    mydb.commit()

def add_order(id,window):
    for widget in window.winfo_children():
        widget.destroy()
    
    Table=Label(window, text="Table-id:", font="none 11 bold").grid(row=1, column= 0, sticky=W)
    id_entry = Entry(window,width=15,bg = 'white')
    id_entry.grid(row=1,column=2)
    # print the menu items on the app
    menu_items = {}
    menu_label =  Label(window, text = 'Menu List:')  
    menu_list = Listbox(window)
    menu_label.grid(row= 3, column = 0)
    menu_list.grid(row = 4, column = 0)
    i=1
    mycursor2.execute("SELECT * from Menu_item")
    for item in mycursor2:
        menu_items[item['idMenu_item']]=item['item_name']
        menu_list.insert(item['idMenu_item'],item['item_name'])
        i+=1
      
    # combobox to choose amount of item
    value = tk.StringVar()
    amountchoosen = ttk.Combobox(window,width = 3, textvariable = value)
    amountchoosen['values'] = ('1','2','3','4','5','6','7','8','9','10')
    amountchoosen.grid(row = 4, column =1)
    # function to insert in the existing order
    add_to_order_arg =partial(add_to_order,id,value, menu_list,menu_items) 
    Done_btn=Button(window,text = 'Add',width = 0,command=add_to_order_arg)
    Done_btn.grid(row=4,column = 3,sticky =W)
    # function to insert new order element and begin the process
    add_order2_arg = partial(add_order2,id,id_entry)
    Done_btn=Button(window,text = 'Start Order',width = 0,command=add_order2_arg)
    Done_btn.grid(row=2,column = 3,sticky =W)


def ordersfunc(id,window):
    for widget in window.winfo_children():
        widget.destroy()
    delivery_orders_arg=partial(delivery_orders,id,window)
    table_orders_arg=partial(table_orders,id,window)
    add_order_arg  = partial(add_order,id,window)
    btn1 = Button(window, text="Table Orders", width=0, command=table_orders_arg, bg = 'cyan')
    btn1.grid(row=1,column=1)
    btn2 = Button(window, text="Delivery Orders", width=0, command=delivery_orders_arg, bg = 'cyan')
    btn2.grid(row=1,column=3)
    btn2 = Button(window, text="Add Order", width=0, command=add_order_arg,bg = 'green')
    btn2.grid(row=1,column=4)
    
############# reservation functions: #################
def reservationsfunc(id,window):
    for widget in window.winfo_children():
        widget.destroy()
    mycursor2.execute("SELECT * FROM (Reservation INNER JOIN Restaurant_Customer_Association \
      on Reservation.idCustomer = Restaurant_Customer_Association.idCustomer) INNER JOIN Customer on \
        Customer.idCustomer=Reservation.idCustomer where (idRestaurant = %s) ORDER by Reservation.reserve_datetime",(id,))


    stg1 = "Reservation time:           People:      Table:      Last Name:              First Name:             Phone:\n"
    msg = Message(window,text = stg1,width = 1000).grid(row = 1,column=1)
    for x in mycursor2:
          reserve_time = x['reserve_datetime']
          people=x['people_amount']
          table = x['idTable']
          last_name = x['last_name']
          first_name = x['first_name']
          phone = x['phone']
          stg2 = str(reserve_time) +'               '+ str(people)+'                '+ str(table)+'          '+last_name+'                       '+first_name+'        '+str(phone)
          msg2=Message(window,text=stg2,width=1000).grid(column=1,sticky = W)

############### delivery functions: ####################
def update_time2(id,id_entry,time_entry):
      idDelivery0 = id_entry.get()
      time0=time_entry.get()
      mycursor2.execute("UPDATE Delivery INNER JOIN\
        Restaurant_Customer_Association \
      on Delivery.idCustomer = Restaurant_Customer_Association.idCustomer\
         SET Delivery.delivery_approximate_time =%s\
          where (idRestaurant = %s) and (idDelivery = %s)",(time0,id,idDelivery0))
      mydb.commit()
      

def update_time(window,id):
    id_label=Label(window, text="Delivery-id:", font="none 11 bold").grid(row=0, column= 10, sticky=W)
    Status_label=Label(window, text="Estimated time:", font="none 11 bold").grid(row=1, column= 10, sticky=W)
    id_entry = Entry(window,width=15,bg = 'white')
    time_entry = Entry(window,width=15,bg='white')
    id_entry.grid(row=0,column=11)
    time_entry.grid(row=1,column=11)

    update_arg = partial(update_time2,id,id_entry,time_entry)
    Done_btn=Button(window,text = 'Done',width = 0,command=update_arg)
    Done_btn.grid(row=3,column = 12,sticky =W)
      

def deliveryfunc(id,window):
    for widget in window.winfo_children():
        widget.destroy()
    mycursor2.execute("SELECT * FROM (Delivery INNER JOIN Restaurant_Customer_Association \
      on Delivery.idCustomer = Restaurant_Customer_Association.idCustomer) INNER JOIN Customer on \
        Customer.idCustomer=Delivery.idCustomer where (idRestaurant = %s) ORDER by Delivery.delivery_time",(id,))

    update_arg=partial(update_time,window,id)
    update_btn=Button(window,text = 'Update Time',width = 0,bg = 'green',command=update_arg)
    update_btn.grid(row=0,column = 7,sticky =W)


    stg1 = "Id Delivery:    Last Name:        First Name:             Address:      Phone:      Delivery Time:      \
      Estimated Time:       Delivery Status:\n" 
    msg = Message(window,text = stg1,width = 1000).grid(row = 1,column=5,sticky=W)
    for x in mycursor2:
          iddelivery = x['idDelivery']
          last_name = x['last_name']
          first_name = x['first_name']
          address = x['address']
          phone = x['phone']
          delivery_time = x['delivery_time']
          estimated_time =  x['delivery_approximate_time']
          status = x['delivery_status']
          stg2 = str(iddelivery) +'               '+ last_name+'     '+ first_name+ '     '+address+'   '+str(phone)+'     '+str(delivery_time)+'      '+str(estimated_time)+'    '+status
          msg2=Message(window,text=stg2,width=1000).grid(column=5,sticky=W)

####################### menu functions #####################
def insert_menu2(id,id_entry,item_price,name):
      idMenu_item0 = id_entry.get()
      item_price0 = item_price.get()
      name0=name.get()
      mycursor2.execute("INSERT INTO project_db20_up1046879.Menu_item (idMenu_item, item_name ,item_price) \
          VALUES(%s,%s,%s)",(idMenu_item0,name0,item_price0))
      mydb.commit()


def insert_menu(window,id):
    for widget in window.winfo_children():
            widget.destroy()
    
    id_label=Label(window, text="Menu-item-id(*):", font="none 11 bold").grid(row=1, column= 0, sticky=W)
    item_price_label=Label(window, text="Price(*):", font="none 11 bold").grid(row=2, column= 0, sticky=W)
    name_label=Label(window, text="Name:", font="none 11 bold").grid(row=3, column= 0, sticky=W)
    id_entry = Entry(window,width=15,bg = 'white')
    item_price_entry=Entry(window,width=15,bg='white')
    name_entry = Entry(window,width=15,bg='white')
    id_entry.grid(row=1,column=2)
    item_price_entry.grid(row=2,column=2)
    name_entry.grid(row=3,column=2)


    insert_arg = partial(insert_menu2,id,id_entry,item_price_entry,name_entry)
    Done_btn=Button(window,text = 'Done',width = 0,command=insert_arg)
    Done_btn.grid(row=6,column = 3,sticky =W)

def delete_menu(delete_text):
    id = delete_text.get()
    mycursor2.execute('DELETE FROM project_db20_up1046879.Menu_item WHERE (idMenu_item = %s)',(id,))
    mydb.commit()

def menufunc(window):
    for widget in window.winfo_children():
        widget.destroy()
    mycursor2.execute("SELECT * FROM menu_item ")


    ####### add food
    insert_arg=partial(insert_menu,window,id)
    insert_btn=Button(window,text = 'Add Menu Item',width = 0,bg = 'cyan',command=insert_arg)
    insert_btn.grid(row=0,column = 10,sticky =W)
    ####### delete fodd
    delete_text = Entry(window,width=5,bg = 'white')
    delete_text.grid(row=0,column=5)
    delete_arg=partial(delete_menu,delete_text)
    delete_btn=Button(window,text='Delete Menu Item',width = 0, bg = 'red',command=delete_arg)
    delete_btn.grid(row=0,column=6,sticky=W)


    stg1 = "Id item:    Price:       Name:"
    msg = Message(window,text = stg1,width = 400).grid(row = 1,column=6,sticky=W)
    for x in mycursor2:
          idMenu_item = x['idMenu_item']
          item_name = x['item_name']
          item_price = x['item_price']
          stg2 = str(idMenu_item) +'               '+ str(item_price)+'                '+ item_name
          msg2=Message(window,text=stg2,width=400).grid(column=6,sticky=W)


############################# customer functions: #########################
def search_customer(textentry,window): 
    id = textentry.get()
    mycursor2.execute('SELECT * FROM project_db20_up1046879.Customer where (idCustomer = %s) ',(id,))
    x=mycursor2.fetchone()
    print(x)
     # for loop to destroy everything that's already in the frame we want to use
    for widget in window.winfo_children():
        widget.destroy()
    stg1 = "Customer ID:    Last Name:     First Name:        Address:         Phone:\n"
    msg = Message(window,text = stg1,width = 400).grid(row = 8,column=4,sticky=W)
    idcustomer=x['idCustomer']
    last_name = x['last_name']
    first_name = x['first_name']
    address = x['address']
    phone = x['phone']
    stg2 = str(idcustomer)+'                 '+last_name +'    '+ first_name +'     '+ address +'     '+ str(phone)
    msg2=Message(window,text=stg2,width=400).grid(column=4,sticky=W)

def customersfunc(id,window):
    for widget in window.winfo_children():
        widget.destroy()
    mycursor2.execute("SELECT * FROM Customer INNER JOIN Restaurant_Customer_Association \
      on Customer.idCustomer = Restaurant_Customer_Association.idCustomer where (idRestaurant = %s) order by last_name,first_name",(id,))

     ################ search button 
    textentry = Entry(window,width = 5, bg= "white")
    textentry.grid(row=0, column = 0, sticky = W)
    # pass arguements to search function
    search_arg=partial(search_customer,textentry,window)
    search_btn=Button(window,text = 'Search',width=0,command=search_arg)
    search_btn.grid(row=0,column = 1,sticky=W)
    ###################


    stg1 = "Customer ID:    Last Name:     First Name:        Address:         Phone:\n"
    msg = Message(window,text = stg1,width = 400).grid(row = 8,column=4,sticky=W)
    for x in mycursor2:
          idcustomer=x['idCustomer']
          last_name = x['last_name']
          first_name = x['first_name']
          address = x['address']
          phone = x['phone']
          stg2 = str(idcustomer)+'                 '+last_name +'    '+ first_name +'     '+ address +'     '+ str(phone)
          msg2=Message(window,text=stg2,width=400).grid(column=4,sticky=W)

#######################  tables functions: ######################## 

def search_tables(textentry,window):
    id = textentry.get()
    mycursor2.execute('SELECT * FROM project_db20_up1046879.Table where (idTable = %s)',(id,))
    x=mycursor2.fetchone()
    # for loop to destroy everything that's already in the frame we want to use
    for widget in window.winfo_children():
        widget.destroy()
    stg1 = "idTable    Chairs    Status    Description\n"
    msg=Message(window,text = stg1,width=400).grid(row=2,column=2,sticky=W)
    idTable= x['idTable'] 
    chairs = x['chairs_number']
    status = x['status']
    description = x['Description']
    stg2 = str(idTable)+'               ' +str(chairs)+ '              '+str(status)+ '              '+ description +'\n'
    msg2=Message(window,text=stg2,width=400).grid(column=2,sticky=W)

def delete_tables(delete_text):
    id = delete_text.get()
    print(id)
    mycursor2.execute('DELETE FROM project_db20_up1046879.Table WHERE (idTable = %s)',(id,))
    mydb.commit()

def insert_tables2(id,chairs_number,Status,Description):
      chairs_number0 = chairs_number.get()
      Status0=Status.get()
      Description0= Description.get()
      mycursor2.execute("INSERT INTO project_db20_up1046879.Table (Table.chairs_number, Table.status,Table.Description,\
          Table.idRestaurant) \
          VALUES(%s,%s,%s,%s)",(chairs_number0,Status0,Description0,id))
      mydb.commit()

def insert_tables(window,id):
    for widget in window.winfo_children():
        widget.destroy()
    
    #id_label=Label(window, text="Table-id(*):", font="none 11 bold").grid(row=1, column= 0, sticky=W)
    chairs_number_label=Label(window, text="Number of Chairs(*):", font="none 11 bold").grid(row=2, column= 0, sticky=W)
    Status_label=Label(window, text="Status:", font="none 11 bold").grid(row=3, column= 0, sticky=W)
    Description=Label(window, text="Description:", font="none 11 bold").grid(row=4, column= 0, sticky=W)
    chairs_entry=Entry(window,width=15,bg='white')
    Status_entry = Entry(window,width=15,bg='white')
    Description_entry = Entry(window,width=15,bg='white')
    chairs_entry.grid(row=2,column=2)
    Status_entry.grid(row=3,column=2)
    Description_entry.grid(row=4,column=2)


    insert_arg = partial(insert_tables2,id,chairs_entry,Status_entry,Description_entry)
    Done_btn=Button(window,text = 'Done',width = 0,command=insert_arg)
    Done_btn.grid(row=6,column = 3,sticky =W)

def update_tables2(id,id_entry,chairs_number,Status,Description):
      idTable0 = id_entry.get()
      chairs_number0 = chairs_number.get()
      Status0=Status.get()
      Description0= Description.get()
      mycursor2.execute("UPDATE project_db20_up1046879.Table SET Table.chairs_number =%s, Table.status =%s,Table.Description =%s\
          where (idRestaurant = %s) and (idTable = %s)",(chairs_number0,Status0,Description0,id,idTable0))
      mydb.commit()

def update_table(window,id):
    for widget in window.winfo_children():
        widget.destroy()
    
    id_label=Label(window, text="Table-id(*):", font="none 11 bold").grid(row=1, column= 0, sticky=W)
    chairs_number_label=Label(window, text="Number of Chairs(*):", font="none 11 bold").grid(row=2, column= 0, sticky=W)
    Status_label=Label(window, text="Status:", font="none 11 bold").grid(row=3, column= 0, sticky=W)
    Description=Label(window, text="Description:", font="none 11 bold").grid(row=4, column= 0, sticky=W)
    id_entry = Entry(window,width=15,bg = 'white')
    chairs_entry=Entry(window,width=15,bg='white')
    Status_entry = Entry(window,width=15,bg='white')
    Description_entry = Entry(window,width=15,bg='white')
    id_entry.grid(row=1,column=2)
    chairs_entry.grid(row=2,column=2)
    Status_entry.grid(row=3,column=2)
    Description_entry.grid(row=4,column=2)


    update_arg = partial(update_tables2,id,id_entry,chairs_entry,Status_entry,Description_entry)
    Done_btn=Button(window,text = 'Done',width = 0,command=update_arg)
    Done_btn.grid(row=6,column = 3,sticky =W)

def update_status2(id,id_entry,Status):
      idTable0 = id_entry.get()
      Status0=Status.get()
      mycursor2.execute("UPDATE project_db20_up1046879.Table SET Table.status =%s\
          where (idRestaurant = %s) and (idTable = %s)",(Status0,id,idTable0))
      mydb.commit()
      

def update_status(window,id):
    id_label=Label(window, text="Table-id:", font="none 11 bold").grid(row=0, column= 14, sticky=W)
    Status_label=Label(window, text="Status:", font="none 11 bold").grid(row=1, column= 14, sticky=W)
    id_entry = Entry(window,width=15,bg = 'white')
    Status_entry = Entry(window,width=15,bg='white')
    id_entry.grid(row=0,column=15)
    Status_entry.grid(row=1,column=15)

    update_arg = partial(update_status2,id,id_entry,Status_entry)
    Done_btn=Button(window,text = 'Done',width = 0,command=update_arg)
    Done_btn.grid(row=3,column = 16,sticky =W)
    
def tablesfunc(id,window):
  
  # for loop to destroy everything that's already in the frame we want to use
  for widget in window.winfo_children():
        widget.destroy()
  
  mycursor2.execute("SELECT * FROM project_db20_up1046879.Table where (idRestaurant = %s) ",(id,))

  ################ insert button
  insert_arg=partial(insert_tables,window,id)
  insert_btn=Button(window,text = 'New Table',width = 0,bg = 'cyan',command=insert_arg)
  insert_btn.grid(row=0,column = 10,sticky =W)
  ################

  ###### update Button
  update_arg=partial(update_table,window,id)
  update_btn=Button(window,text = 'Update Table',width = 0,bg = 'green',command=update_arg)
  update_btn.grid(row=0,column = 12,sticky =W)
  status_arg=partial(update_status,window,id)
  status_btn=Button(window,text = 'Update Status',width = 0,bg = 'green',command=status_arg)
  status_btn.grid(row=0,column = 13,sticky =W)
  ########

  ################ delete button
  delete_text = Entry(window,width=5,bg = 'white')
  delete_text.grid(row=0,column=5)
  delete_arg=partial(delete_tables,delete_text)
  delete_btn=Button(window,text='Delete Table',width = 0, bg = 'red',command=delete_arg)
  delete_btn.grid(row=0,column=6,sticky=W)
  ################

  ################ search button 
  textentry = Entry(window,width = 5, bg= "white")
  textentry.grid(row=0, column = 0, sticky = W)
  # pass arguements to search function
  search_arg=partial(search_tables,textentry,window)
  search_btn=Button(window,text = 'Search',width=0,command=search_arg)
  search_btn.grid(row=0,column = 1,sticky=W)
  ###################

  stg1 = "idTable    Chairs    Status    Description\n"
  msg=Message(window,text = stg1,width=400).grid(row=1,column=2,sticky=W)
  for x in mycursor2:
    idTable= x['idTable'] 
    chairs = x['chairs_number']
    status = x['status']
    description = x['Description']
    stg2 = str(idTable)+'               ' +str(chairs)+ '              '+str(status)+ '              '+ description +'\n'
    msg2=Message(window,text=stg2,width=400).grid(column=2,sticky=W)

### test function for buttons (not important) 
def donothing():
  print("Do nothing")
##########################################################################################################


# function to open the admin (restaurant) window 
# on a button click

def adminWindow(cursor,username,password):

  window.withdraw()
  # Toplevel object which will  
  # be treated as a new window 
  newWindow = Toplevel(window) 
  #set fullscreen
  newWindow.state('zoomed')
  # sets the title of the 
  # Toplevel widget 
  newWindow.title("Admin") 
  frame1=Frame(newWindow)
  frame1.grid(row=1)
  frame0 = Frame(newWindow)
  frame0.grid(row=0)

  cursor.execute("SELECT * FROM Restaurant WHERE (username = %s) AND (password = %s)",(username,password)) 
  details=cursor.fetchone()

  ### to pass arguements in button command
  tablesfunc_arg = partial(tablesfunc,details['idRestaurant'],frame1)
  customersfunc_arg=partial(customersfunc,details['idRestaurant'],frame1)
  menufunc_arg=partial(menufunc,frame1)
  deliveryfunc_arg=partial(deliveryfunc,details['idRestaurant'],frame1)
  reservationsfunc_arg=partial(reservationsfunc,details['idRestaurant'],frame1)
  ordersfunc_arg=partial(ordersfunc,details['idRestaurant'],frame1)
  statisticsfunc_arg = partial(statisticsfunc,details['idRestaurant'],frame1)
  ####
  myFont0 = font.Font(family='Helvetica',size = 11,weight = 'bold')
  myFont = font.Font(family='Helvetica',size = 11)
  # buttons:
  Label(frame0, text ='Welcome  '+details['name']+ '!',font = myFont0, relief = RAISED).grid(row=1, column= 0, sticky=E)
  Label(frame0, text ='Description : '+'\n'+details['address']+'\n'+details['phone'],font = myFont0, relief = RAISED).grid(row=2, column= 0, sticky=W)
  reservations = Button(frame0, text="Reservations", width=0,activebackground='blue', font = myFont,bg='cornflower blue', command=reservationsfunc_arg)
  tables = Button(frame0, text="Tables", width=0,activebackground='blue', font = myFont,bg='cornflower blue', command=tablesfunc_arg)
  orders = Button(frame0, text="Orders", width=0,activebackground='blue', font = myFont,bg='cornflower blue', command=ordersfunc_arg)
  customers = Button(frame0, text="Customers", width=0,activebackground='blue',bg='cornflower blue', font = myFont, command=customersfunc_arg)
  delivery = Button(frame0, text="Delivery", width=0,activebackground='blue',bg='cornflower blue', font = myFont, command=deliveryfunc_arg)
  menu = Button(frame0, text="Menu", width=0,activebackground='blue',bg='cornflower blue', font = myFont, command=menufunc_arg)
  statistics = Button(frame0, text="Statistics",activebackground='blue',bg='cornflower blue', font = myFont, width=0, command=statisticsfunc_arg)
  reservations.grid(row=5,column=1,padx=10, pady=10)
  tables.grid(row=5,column=2,padx=10, pady=10)
  orders.grid(row=5,column=3,padx=10, pady=10)
  customers.grid(row=5,column=4,padx=10, pady=10)
  delivery.grid(row=5,column=5,padx=10, pady=10)
  menu.grid(row=5,column=6,padx=10, pady=10)
  statistics.grid(row=5,column=6,padx=10, pady=10)




#button click function
def login():
    entered_text1 = textentry1.get() # this will collect the text from the entry box 
    entered_text2 = textentry2.get()
    # make sure the text box is clear
    output.delete(0.0, END)
    try:
        if entered_text1 in admin_dicitonary and admin_dicitonary[entered_text1] == entered_text2:
          adminWindow(mycursor2,entered_text1,entered_text2)
        else:
          msg = "User does not exist or incorrect password"
          output.insert(END , msg)
    except:
        msg = "Could not login "
        output.insert(END , msg)
    
def registerboxes():
    Label(window, text="Username(*):", font="none 12 bold").grid(row=6, column= 0, sticky=W)
    Label(window, text="Password(*):", font="none 12 bold").grid(row=7, column= 0, sticky=W)
    Label(window, text="Name(*):", font="none 12 bold").grid(row=8, column= 0, sticky=W)
    Label(window, text="Address(*):", font="none 12 bold").grid(row=9, column= 0, sticky=W)
    Label(window, text="Phone(*):", font="none 12 bold").grid(row=10, column= 0, sticky=W)
    username = Entry(window,width = 50, bg= "white")
    username.grid(row=6, column = 1, sticky = W)
    password = Entry(window,width = 50, bg= "white")
    password.grid(row=7, column = 1, sticky = W )
    restaurant_name = Entry(window,width = 50, bg= "white")
    restaurant_name.grid(row=8, column = 1, sticky = W)
    address = Entry(window,width = 50, bg= "white")
    address.grid(row=9, column = 1, sticky = W)
    phone = Entry(window,width = 50, bg= "white")
    phone.grid(row=10, column = 1, sticky = W)
    register_arg= partial(register,username,password,restaurant_name,address,phone)
    Button(window, text="DONE", width=0, command=register_arg,relief=RAISED).grid(row = 12, column = 1 , sticky = W)


def register(username,password,name,address,phone):
    username_ = username.get() # this will collect the text from the entry box 
    password_ = password.get()
    name_ = name.get()
    address_ = address.get()
    phone_ = phone.get()
    # make sure the text box is clear
    output.delete(0.0, END)
    try:
        if username_ in admin_dicitonary :
          msg = "Username already exists"
        else:
          mycursor2.execute("INSERT INTO Restaurant (`name`,`address`,`phone`,\
            `username`,`password`) VALUES (%s,%s,%s,%s,%s)",(name_,address_,phone_,username_,password_))
          mydb.commit()
          msg = "User created please login"
    except:
        msg = "Could not register "
    print(admin_dicitonary)
    output.insert(END , msg)
##########################################################################################################

## main

window = Tk()
window.title("Restaurant")

# create label for user login:
Label(window, text="Username:", font="none 12 bold").grid(row=1, column= 0, sticky=W)
# create a text entry box:
textentry1 = Entry(window,width = 50, bg= "white")
textentry1.grid(row=1, column = 1, sticky = W)
# create a label for password login:
Label(window, text="Password:", font="none 12 bold").grid(row=2, column= 0, sticky=W)
# create a text entry box:
textentry2 = Entry(window,width = 50, bg= "white",show ="*")
textentry2.grid(row=2, column = 1, sticky = W)
# login prompt:
Button(window, text="LOG IN", width=0, command=login).grid(row = 3, column = 1 , sticky = W)
# register promp:
Button(window, text="REGISTER", width=0, command=registerboxes).grid(row = 4 ,column = 1, sticky = W)

#create a textbox
output = Text(window,width = 50, height = 2, wrap = WORD, background="white")
output.grid(row=5, column=1, sticky =W)


## run the main loop:
window.mainloop()