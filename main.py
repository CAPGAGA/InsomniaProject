import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
import sqlite3
import os

root = Tk()

root.title('Insomnia Store')
root.iconphoto(True, tkinter.PhotoImage(file='./eye.png'))
root.geometry('1280x720')


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
    c.execute("""CREATE TABLE sessions (
            login_name text,
            session_number int,
            product text,
            price int,
            time text
            )""")
    c.execute("""CREATE TABLE income (
            login_name text,
            session_number int,
            income int,
            time text
            incass int
            )""")

    #Commit changes
    conn.commit()

    #Close connection

    conn.close()

#Creating users database or connecting to existing one
if os.path.exists(str(os.getcwd())+'\\Users.db') == True:
    pass
else:
    conn = sqlite3.connect('Users.db')

    #Creating cursor
    c = conn.cursor()

    #Create table

    c.execute("""CREATE TABLE users (
            login text,
            password text,
            user_type text
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
                                                            # Login page
login_page = Frame(store_notebook, width=100, heigh=100, bg='white')
login_page.pack(fill='both', expand=1)
store_notebook.add(login_page, text='Логин')


login_label = Label(login_page, text='Login:')
login_label.grid(row=1, column=1, sticky='we', padx=100)
password_label = Label(login_page, text="Password")
password_label.grid(row=2, column=1, sticky='we', padx=100)
login_field = Entry(login_page)
login_field.grid(row=1, column=2)
password_field = Entry(login_page)
password_field.grid(row=2, column=2)


def login():
    global current_session_number
    global users_login


    conn = sqlite3.connect('Users.db')

    c = conn.cursor()

    c.execute("SELECT * FROM users")
    users_info = c.fetchall()

    users_dict = {}

    for login, password, user_type in users_info:
        users_dict.update({login: password})
    login = login_field.get()
    password = password_field.get()

    if login in users_dict.keys():
        if password == users_dict.get(login):
            conn = sqlite3.connect('Products_store.db')
            c=conn.cursor()
            c.execute("SELECT MAX(session_number) FROM sessions")

            session_number = c.fetchall()
            session_number = list(session_number)[0][0]
            if session_number is None:
                session_number= 0
            current_session_number = session_number + 1
            users_login = login
            login_field.delete(0,END)
            password_field.delete(0,END)
            store_notebook.forget(store_notebook.select())

            # Add products tab

            product_add_page = Frame(store_notebook, width=600, heigh=600, bg='white')
            product_add_page.pack(fill='both', expand=1)
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

            # Input fields
            name_field = Entry(product_add_page)
            name_field.grid(row=2, column=2)

            ammount_field = Entry(product_add_page)
            ammount_field.grid(row=3, column=2)

            size_field = Entry(product_add_page)
            size_field.grid(row=4, column=2)

            price_field = Entry(product_add_page)
            price_field.grid(row=5, column=2)

            # Buttons

            # Add product button
            def add_product():
                # Add product to data base
                # Connect to data base
                conn = sqlite3.connect('Products_store.db')

                # Creating cursor
                c = conn.cursor()

                # Insert data

                c.execute("INSERT INTO products VALUES (:name, :ammount, :size, :price, :img)",
                          {
                              'name': name_field.get(),
                              'ammount': ammount_field.get(),
                              'size': size_field.get(),
                              'price': price_field.get(),
                              'img': img_filename
                          })

                # Commit changes
                conn.commit()

                # Close connection

                # Clear Text Boxes
                name_field.delete(0, END)
                ammount_field.delete(0, END)
                size_field.delete(0, END)
                price_field.delete(0, END)

            add_prod_button = Button(product_add_page, text="Add Product", command=add_product)
            add_prod_button.grid(row=3, column=3)

            # Browse for img button and preview widget

            browse_img_button = Button(product_add_page, text='Browse img')

            def open_img():
                global preview_img
                global img_filename
                img_filename = filedialog.askopenfilename(title='Open product image file',
                                                          filetypes=[('all files', '*.*')])
                preview_img = Image.open(img_filename)
                resized_img = preview_img.resize((200, 200))
                preview_img = ImageTk.PhotoImage(resized_img)
                preview_img_label = Label(product_add_page, image=preview_img)
                preview_img_label.grid(row=6, column=2)
                return preview_img, img_filename

            browse_img_button.config(command=open_img)

            # Products page
            main_frame = Frame(root, width=1280, heigh=720, bg='white')
            main_frame.pack(fill='both', expand=1)
            main_frame.grid_propagate(0)

            store_notebook.add(main_frame, text='Страница товаров')

            side_canvas = Canvas(main_frame, width=650, heigh=600, bg='white')
            side_canvas.pack(side='left', fill='both', expand=1)

            scroll_bar = Scrollbar(main_frame, orient='vertical', command=side_canvas.yview)
            scroll_bar.pack(side='right', fill='y')
            side_canvas.config(yscrollcommand=scroll_bar.set)

            side_canvas.bind('<Configure>', lambda e: side_canvas.configure(scrollregion=side_canvas.bbox('all')))

            products_page = Frame(side_canvas)
            side_canvas.create_window((0, 0), window=products_page, anchor='nw')

            busket_label = Label(products_page, text='Busket of prodcuts').grid(row=0, column=2)
            products_listbox = Listbox(products_page)
            products_listbox.grid(row=1, column=2, sticky='n', pady=20)

            note_label = Label(products_page, text='Notes')
            note_label.grid(row=0, column=3, sticky='we')
            notes_listbox = Listbox(products_page)
            notes_listbox.grid(row=1, column=3, columnspan=1, sticky='nwe')
            add_note_label = Label(products_page, text='Write note below').grid(row=1, column=3, sticky='s', pady=15)
            note_entry = Entry(products_page)
            note_entry.grid(row=2, column=3, sticky='n')

            def insert_note():
                notes_listbox.insert(END, note_entry.get())
                note_entry.delete(0, END)

            def delete_note():
                selected = notes_listbox.curselection()
                notes_listbox.delete(selected[0])

            add_note_button = Button(products_page, text='Add note', command=insert_note).grid(row=2, column=3,
                                                                                               sticky='new', pady=20)
            delete_note_button = Button(products_page, text='Delete note', command=delete_note).grid(row=2, column=3,
                                                                                                     sticky='new',
                                                                                                     pady=50)

            price_is_label = Label(products_page, text="Final price is:").grid(row=2, column=2, sticky='nw')
            return_label = Label(products_page, text='Total return is:').grid(row=2, column=2, sticky='nw', pady=60,
                                                                              ipady=5)

            # Displaying products on products page
            products_in_busket = []

            conn = sqlite3.connect("Products_store.db")

            c = conn.cursor()

            c.execute("SELECT *, oid FROM products")
            products = c.fetchall()
            # Geting images and prod's names from db
            products_to_show = {}
            products_name_price = {}
            for name, amount, size, price, filename, oid in products:
                products_to_show.update({name: filename})
                products_name_price.update({name: price})

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
                                         command=lambda name=name: selling_product(name)).grid(row=i + 1, column=col)
                elif i > (len(names) / 2):
                    col = 1
                    image = Image.open(images[i])
                    resized_img = image.resize((200, 200))
                    img_for_label = ImageTk.PhotoImage(resized_img)
                    S.save((img_for_label))
                    prod_button = Button(products_page, text=name, image=img_for_label, compound=TOP,
                                         command=lambda name=name: selling_product(name)).grid(row=r + 1, column=col)
                    r += 1

            conn.commit()

            conn.close()
            global final_price
            final_price = 0

            def selling_product(name):

                global final_price
                global total_price
                lambda: total_price.grid_forget()
                final_price += products_name_price.get(name)
                products_listbox.insert(END, name)
                total_price = Label(products_page, text=f'{final_price}')
                total_price.grid(row=2, column=2, sticky='ne')

            income_label = Label(products_page, text='Enter recived money:')
            income_label.grid(row=2, column=2, sticky='n', pady=25)
            income_entry = Entry(products_page, text="Income money")
            income_entry.grid(row=2, column=2, sticky='n', pady=45)

            def delete_from_buscket():
                global selected_item
                global final_price
                global total_price
                lambda: total_price.grid_forget()
                selected_item = products_listbox.curselection()
                name = products_listbox.get(ANCHOR)
                products_listbox.delete(selected_item[0])
                final_price -= products_name_price.get(name)
                total_price = Label(products_page, text=f'{final_price}').grid(row=2, column=2, sticky='ne')

            delet_from_buscket_button = Button(products_page, text='Delet selected item', command=delete_from_buscket)
            delet_from_buscket_button.grid(row=1, column=2, sticky='swe', ipady=0.5, pady=5)

            def calculate_outcome():
                outcome = float(income_entry.get()) - final_price
                outcome_label = Label(products_page, text=f'{outcome}', bg='green').grid(row=2, column=2, sticky='ne',
                                                                                         pady=70)

            calculate_button = Button(products_page, text="calculate outcome", command=calculate_outcome).grid(row=2,
                                                                                                               column=2,
                                                                                                               sticky='nwe',
                                                                                                               pady=90)

            name_amount = {}
            name_prise = {}

            def final_sale():
                global final_price

                conn = sqlite3.connect('Products_store.db')
                c = conn.cursor()
                c.execute('''SELECT * FROM products''')
                products = c.fetchall()
                busket_items = products_listbox.get(first=0, last=products_listbox.size())
                for name, size, amount, price, filename in products:
                    name_amount.update({name: amount})
                    if name in busket_items:
                        name_prise[name] = price
                for name_of_product in busket_items:
                    name_amount.update({name_of_product: int(name_amount.get(name_of_product) - 1)})

                for key, value in name_amount.items():
                    c.execute('''UPDATE products SET
                    ammount = :amount
                    WHERE product_name = :name''',
                              {'name': key,
                               'amount': value
                               })
                for name_of_product in busket_items:
                    c.execute("INSERT INTO sessions VALUES (:login_name, :session_number, :product,:price, :time)",
                              {
                                  'login_name': users_login,
                                  'session_number': current_session_number,
                                  'product': name_of_product,
                                  'price': name_prise.get(name_of_product),
                                  'time': datetime.now()
                              })
                c.execute("INSERT INTO income VALUES (:login_name, :session_number, :income, :time)",
                          {
                              'login_name': users_login,
                              'session_number': current_session_number,
                              'income': income_entry.get(),
                              'time': datetime.now()

                          })

                conn.commit()
                conn.close()

                products_listbox.delete(first=0, last=products_listbox.size())
                final_price = 0
                name_amount.clear()
                name_prise.clear()

            final_sale_button = Button(products_page, text='Sell items!', command=final_sale)
            final_sale_button.grid(row=2, column=2, sticky='nwe', pady=115)

            # Incass window
            def open_incss_window():

                global current_balnce_label

                incass_window = Toplevel()
                incass_window.title('Incass')
                incass_window.iconphoto(True, tkinter.PhotoImage(file='./eye.png'))
                incass_window.geometry('350x300')

                conn = sqlite3.connect('Products_store.db')
                c = conn.cursor()
                c.execute("""SELECT * FROM income""")
                income = c.fetchall()
                income_listbox = Listbox(incass_window)
                income_listbox.grid(row=1,column=0,columnspan=2,sticky='ew')
                total_income = 0
                for login_name, session_number, come, time in income:
                    if come == '':
                        pass
                    else:
                        total_income += int(come)
                        income_listbox.insert(END, (login_name, session_number, income, time))
                balnce_label = Label(incass_window, text='Current balance is:').grid(row=0,column=0)
                current_balnce_label = Label(incass_window, text=f'{total_income}')
                current_balnce_label.grid(row=0,column=1)
                redraw_label = Label(incass_window, text='Enter amount to redraw:').grid(row=2,column=0,sticky='w')
                redraw_entry = Entry(incass_window)
                redraw_entry.grid(row=2,column=1)

                def redraw():

                    global current_balnce_label

                    redraw_amount = int(redraw_entry.get())
                    left = total_income - redraw_amount
                    conn = sqlite3.connect('Products_store.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO income VALUES (:login_name, :session_number, :income, :time)",
                              {
                                  'login_name': 'Incass',
                                  'session_number': current_session_number,
                                  'income': -redraw_amount,
                                  'time': datetime.now()

                              })
                    current_balnce_label.destroy()
                    current_balnce_label = Label(incass_window, text=f'{left}')
                    current_balnce_label.grid(row=0, column=1)
                    conn.commit()
                    conn.close()

                redraw_button = Button(incass_window, text='Redraw money',command=redraw).grid(row=2,column=2)
                conn.commit()
                conn.close()
            incass_button = Button(products_page, text = 'Open incass window',command= open_incss_window)
            incass_button.grid(row=1, column=4,sticky='n',pady=25)

            def log_out():
                root.destroy()
                os.startfile("main.exe")


            log_out_button = Button(products_page, text='Log out', command=log_out)
            log_out_button.grid(row=1, column=4,sticky='nwe')


            # Labels

            product_add_label = Label(product_add_page, text="Страница добваления товара")
            products_page_label = Label(products_page, text="Страница товаров")

            product_add_label.grid(row=1, column=1)
            products_page_label.grid(row=0, column=2)

            # Config page
            log_page = Frame(store_notebook, width=600, heigh=600, bg='white')
            log_page.pack(fill='both', expand=1)
            store_notebook.add(log_page, text='Выписка')

            def open_edit_window():

                global edit_img
                global edit_img_filename
                global edit_preview_img
                global name_field_editor
                global ammount_field_editor
                global ize_field_editor
                global price_field_editor

                change_product_window = Toplevel()
                change_product_window.title('Change product info')
                change_product_window.iconphoto(True, tkinter.PhotoImage(file='./eye.png'))
                change_product_window.geometry('600x600')

                name_label_editor = Label(change_product_window, text="Product's name")
                name_label_editor.grid(row=2, column=1)

                ammount_label_editor = Label(change_product_window, text="Size of product")
                ammount_label_editor.grid(row=3, column=1)

                size_label_editor = Label(change_product_window, text="Ammount of product")
                size_label_editor.grid(row=4, column=1)

                price_label_editor = Label(change_product_window, text="Product price")
                price_label_editor.grid(row=5, column=1)

                img_label_editor = Label(change_product_window, text="Img of product")
                img_label_editor.grid(row=6, column=1)

                # Input fields
                name_field_editor = Entry(change_product_window)
                name_field_editor.grid(row=2, column=2)

                ammount_field_editor = Entry(change_product_window)
                ammount_field_editor.grid(row=3, column=2)

                size_field_editor = Entry(change_product_window)
                size_field_editor.grid(row=4, column=2)

                price_field_editor = Entry(change_product_window)
                price_field_editor.grid(row=5, column=2)

                product_id = oid_entry.get()

                conn = sqlite3.connect('Products_store.db')
                c = conn.cursor()
                c.execute("SELECT * FROM products WHERE oid = " + product_id)
                product_info = c.fetchall()

                for name, amount, size, price, edit_img_filename in product_info:
                    name_field_editor.insert(0, name)
                    ammount_field_editor.insert(0, amount)
                    size_field_editor.insert(0, size)
                    price_field_editor.insert(0, price)

                    preview_img = Image.open(edit_img_filename)
                    resized_img = preview_img.resize((200, 200))
                    edit_preview_img = ImageTk.PhotoImage(resized_img)
                    preview_img_label = Label(change_product_window, image=edit_preview_img)
                    preview_img_label.grid(row=6, column=2)

                # Add product button
                def edit_product():
                    global name_field_editor
                    global edit_img_filename
                    global ammount_field_editor
                    global ize_field_editor
                    global price_field_editor
                    global preview_img

                    # Edit product to data base
                    # Connect to data base
                    conn = sqlite3.connect('Products_store.db')

                    # Creating cursor
                    c = conn.cursor()

                    # Insert data

                    c.execute("""UPDATE products SET
                        product_name = :name,
                        ammount = :amount,
                        size = :size,
                        price = :price,
                        img = :img
                        WHERE oid = :oid""",

                              {'name': name_field_editor.get(),
                               'amount': ammount_field_editor.get(),
                               'size': size_field_editor.get(),
                               'price': price_field_editor.get(),
                               'img': edit_img,

                               'oid': product_id
                               })

                    # Commit changes
                    conn.commit()

                    # Close connection

                    # Clear Text Boxes
                    name_field_editor.delete(0, END)
                    ammount_field_editor.delete(0, END)
                    size_field_editor.delete(0, END)
                    price_field_editor.delete(0, END)
                    preview_img_label.destroy()

                add_prod_button = Button(change_product_window, text="Commit change", command=edit_product)
                add_prod_button.grid(row=3, column=3)

                # Browse for img button and preview widget

                browse_img_button = Button(change_product_window, text='Browse img')
                browse_img_button.grid(row=4, column=3)

                def open_img():
                    global edit_img
                    global edit_preview_img
                    global preview_img_edit
                    edit_img = filedialog.askopenfilename(title='Open product image file',
                                                          filetypes=[('all files', '*.*')])
                    preview_img_edit = Image.open(edit_img)
                    resized_img = preview_img_edit.resize((200, 200))
                    edit_preview_img = ImageTk.PhotoImage(resized_img)
                    preview_img_label = Label(change_product_window, image=edit_preview_img)
                    preview_img_label.grid(row=6, column=2)
                    return edit_preview_img, preview_img_edit, edit_img

                browse_img_button.config(command=open_img)

            open_edit_wondow_button = Button(log_page, text='Open editor', command=open_edit_window).grid(row=5,
                                                                                                          column=1)

            def delete_product():
                # Delete product from data base

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

                # Prining the log

                print_logs = ''
                for products in products:
                    print_logs += str(products) + "\n"
                log_label = Label(log_page, text=print_logs)
                log_label.grid(row=2, column=2)

                conn.commit()

                conn.close()
            log_label = Label(log_page, text = 'Products info').grid(row=1,column=2)
            log_button = Button(log_page, text="Show log", command=show_log)
            delete_product_button = Button(log_page, text="Delete product", command=delete_product)

            browse_img_button.grid(row=10, column=2)

            log_button.grid(row=1, column=1)
            delete_product_button.grid(row=4, column=1)

            # Image button and Preview widget

            # Ipnput fields

            oid_entry = Entry(log_page)

            oid_entry.grid(row=3, column=1)




        else:
            error_label = Label(login_page, text="Wrong login or password! Try again").grid(row=4, column=2)
    else:
        error_label = Label(login_page, text="Wrong login or password! Try again").grid(row=4, column=2)

    conn.close()


login_button = Button(login_page, text="Login", command=login)
login_button.grid(row=3, column=2)


def open_create_user_window():
    # Creating users tab

    create_user_window = Toplevel()
    create_user_window.title('Create User')
    create_user_window.iconphoto(True, tkinter.PhotoImage(file='./eye.png'))
    create_user_window.geometry('200x200')

    login_entry = Entry(create_user_window)
    login_entry.grid(row=1, column=1)
    password_entry = Entry(create_user_window)
    password_entry.grid(row=2, column=1)
    user_type_entry = Entry(create_user_window)
    user_type_entry.grid(row=3, column=1)

    login_l = Label(create_user_window, text='Login:').grid(row=1, column=0)
    password_l = Label(create_user_window, text='Password').grid(row=2, column=0)
    user_type_l = Label(create_user_window, text='User type').grid(row=3, column=0)

    def create_user():
        conn = sqlite3.connect('Users.db')

        c = conn.cursor()

        c.execute("INSERT INTO users VALUES (:login, :password, :user_type)",
                  {
                      'login': login_entry.get(),
                      'password': password_entry.get(),
                      'user_type': user_type_entry.get(),

                  })

        conn.commit()
        conn.close()

        login_entry.delete(0, END)
        password_entry.delete(0, END)
        user_type_entry.delete(0, END)

    create_user_button = Button(create_user_window, text="Create user", command=create_user)
    create_user_button.grid(row=4, column=1)


to_create_user_button = Button(login_page, text='Create user', command= open_create_user_window)
to_create_user_button.grid(row=1, column=3, columnspan=200)



root.mainloop()