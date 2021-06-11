import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os

root = Tk()

root.title('Insomnia Store')
root.iconphoto(True, tkinter.PhotoImage(file='C:/Users/ghast/PycharmProjects/InsominaProject/eye.png'))
root.geometry('600x600')

#Creating products database or connecting to existing one
if os.path.exists(str(os.getcwd())+'\\Products_store.db') == True:
    pass
else:
    conn = sqlite3.connect('Products_store.db')

    #Creating cursor
    c = conn.cursor()

    #Create table

    c.execute("""CREATE TABLE products (
            product_name text,
            size text,
            ammount int,
            price float,
            img text
            )""")

    #Commit changes
    conn.commit()

    #Close connection

    conn.close()

#Creating users database or connecting to existing one
if os.path.exists(str(os.getcwd())+'\\User.db') == True:
    pass
else:
    conn = sqlite3.connect('User.db')

    #Creating cursor
    c = conn.cursor()

    #Create table

    c.execute("""CREATE TABLE user (
            login text,
            password text,
            user_type text,
            )""")

    #Commit changes
    conn.commit()

    #Close connection

    conn.close()

class S():
    # To make an object 'accessible', and thus save
    # it from garbage collection.
    fred = []
    @classmethod
    def save(cls, x):
        cls.fred.append(x)

#Tabs

store_notebook = ttk.Notebook(root)
store_notebook.pack(pady=15)


    # Add products tab

product_add_page = Frame(store_notebook, width = 600, heigh = 600, bg = 'white')
product_add_page.pack(fill = 'both', expand =1)
store_notebook.add(product_add_page, text='Добавить товары')

# Labels

name_label = Label(product_add_page, text="Product's name")
name_label.grid(row=2, column=1)

ammount_label = Label(product_add_page, text="Ammount of product")
ammount_label.grid(row=3, column=1)

size_label = Label(product_add_page, text="Size of product")
size_label.grid(row=4, column=1)

price_label = Label(product_add_page, text="Product price")
price_label.grid(row=5, column=1)

img_label = Label(product_add_page, text="Img of product")
img_label.grid(row=6, column=1)

# Buttons
# Add product button
def add_product():
    #Add product to data base
    #Connect to data base
    conn = sqlite3.connect('Products_store.db')

    # Creating cursor
    c = conn.cursor()

    #Insert data

    c.execute("INSERT INTO products VALUES (:name, :ammount, :size, :price, :img)",
              {
                  'name' : name_field.get(),
                  'ammount' : ammount_field.get(),
                  'size' : size_field.get(),
                  'price': price_field.get(),
                  'img' : img_filename
              })

    #Commit changes
    conn.commit()

    #Close connection

    #Clear Text Boxes
    name_field.delete(0, END)
    ammount_field.delete(0, END)
    size_field.delete(0, END)
    price_field.delete(0,END)

add_prod_button = Button(product_add_page, text = "Add Product", command = add_product)

# Browse for img button and preview widget

browse_img_button = Button(product_add_page, text = 'Browse img')

def open_img():
    global preview_img
    global img_filename
    img_filename = filedialog.askopenfilename(title='Open product image file', filetypes=[('all files', '*.*')])
    preview_img = Image.open(img_filename)
    resized_img = preview_img.resize((200, 200))
    preview_img = ImageTk.PhotoImage(resized_img)
    preview_img_label = Label(product_add_page, image=preview_img)
    preview_img_label.grid(row=6, column=2)
    return preview_img, img_filename

browse_img_button.config(command = open_img)


    # Products page

products_page = Frame(store_notebook, width = 600, heigh = 600, bg = 'white')
products_page.pack(fill = 'both', expand =1)
store_notebook.add(products_page, text='Страница товаров')

#Displaying products on products page


conn = sqlite3.connect("Products_store.db")

c = conn.cursor()

c.execute("SELECT *, oid FROM products")
products = c.fetchall()
# Geting images and prod's names from db
products_to_show ={}
for name, amount, size, price, filename, oid in products:
    products_to_show.update({name:filename})

names = []
images = []
for name in products_to_show.keys():
    names.append(name)
for img in products_to_show.values():
    images.append(img)

r = 0
for i, name in enumerate(names):
    if i <= (len(names) / 2):
        col = 0
        image = Image.open(images[i])
        resized_img = image.resize((200, 200))
        img_for_label = ImageTk.PhotoImage(resized_img)
        S.save((img_for_label))
        prod_button = Button(products_page, text=name, image=img_for_label, compound=TOP,
                             command=lambda name=name: open_product_page(name)).grid(row=i + 1, column=col)
    elif i > (len(names) / 2):
        col = 1
        image = Image.open(images[i])
        resized_img = image.resize((200, 200))
        img_for_label = ImageTk.PhotoImage(resized_img)
        S.save((img_for_label))
        prod_button = Button(products_page, text=name, image=img_for_label, compound=TOP,
                             command=lambda name=name: open_product_page(name)).grid(row=r + 1, column=col)
        r += 1

conn.commit()

conn.close()


#Command for button to open product's page of this product
def open_product_page(name):

    product_page = Frame(store_notebook, width=600, heigh=600, bg='white')
    product_page.pack(fill='both', expand=1)
    store_notebook.add(product_page, text=f'Страница товара {name}')

    # Connecting to database and displaying product info

    conn = sqlite3.connect('Products_store.db')

    c = conn.cursor()

    c.execute("SELECT * FROM products")
    products = c.fetchall()

    for i in range(len(products)):
        if name == products[i][0]:
            product = products[i]

    # Dropdown widget

    entry_filed = Entry(product_page)
    entry_filed.pack()

    conn.commit()
    conn.close()

# Displaying products as buttons on products page







login_page = Frame(store_notebook, width = 600, heigh = 600, bg = 'white')
login_page.pack(fill = 'both', expand =1)
store_notebook.add(login_page, text='Логин')

log_page = Frame(store_notebook, width = 600, heigh = 600, bg = 'white')
log_page.pack(fill = 'both', expand =1)
store_notebook.add(log_page, text='Выписка')

incass_page = Frame(store_notebook, width = 600, heigh = 600, bg = 'white')
incass_page.pack(fill = 'both', expand =1)
store_notebook.add(incass_page, text='Инкасация')















#Labels

product_add_label = Label(product_add_page, text="Страница добваления товара")
products_page_label = Label(products_page, text="Страница товаров")

login_label = Label(products_page, text = "Login:")
loginid_label = Label(products_page, text = "LoginId")

product_add_label.grid(row=1, column=1)
products_page_label.grid(row=0,column=2)

login_label.grid(row=0, column=0)
loginid_label.grid(row=0, column=1)


#Buttons



def delete_product():
    #Delete product from data base

    conn = sqlite3.connect('Products_store.db')

    c = conn.cursor()

    c.execute("DELETE from products WHERE oid =" + oid_entry.get())

    conn.commit()

    conn.close()

def show_log():

    conn = sqlite3.connect("Products_store.db")

    c = conn.cursor()

    c.execute("SELECT *, oid FROM products")
    products = c.fetchall()
    #print(products)

    #Prining the log

    print_logs = ''
    for products in products:
        print_logs += str(products) + "\n"
    log_label = Label(log_page, text=print_logs)
    log_label.grid(row=1, column=2)

    conn.commit()

    conn.close()




to_addprod_button = Button(products_page, text = "Add products")
del_prod_button = Button(products_page, text = "Delete Products")
login_button = Button(login_page, text = "Login")
to_incass_button = Button(log_page, text = "Incass")
incass_button = Button(incass_page, text = "Incass")
log_button = Button(log_page, text = "Show log", command = show_log)
delete_product_button = Button(log_page, text = "Delete product", command = delete_product)


add_prod_button.grid(row=3 , column=3)
browse_img_button.grid(row=10, column=2)
to_addprod_button.grid(row=1,column=2)
to_incass_button.grid(row=1, column=3)
del_prod_button.grid(row=2, column=2)
login_button.grid(row=3, column=2)
log_button.grid(row=1, column=1)
to_incass_button.grid(row=2, column=1)
delete_product_button.grid(row=4, column=1)
incass_button.pack()
#Image button and Preview widget



#Ipnput fields

login_field = Entry(login_page)
password_field = Entry(login_page)
name_field = Entry(product_add_page)
ammount_field = Entry(product_add_page)
size_field = Entry(product_add_page)
price_field = Entry(product_add_page)

incass_entry = Entry(incass_page)
oid_entry =Entry(log_page)

login_field.grid(row=1, column=2)
password_field.grid(row=2,column=2)
name_field.grid(row=2, column=2)
ammount_field.grid(row=3, column =2)
size_field.grid(row=4, column =2)
price_field.grid(row=5, column =2)

incass_entry.pack()
oid_entry.grid(row=3, column=1)



#Login Page

def login():
    pass


root.mainloop()