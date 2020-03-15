from tkinter import * 
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3
import datetime

def hash(text):
    hashedtext = ''
    for i in text:
        if i == ' ':
            hashedtext += ' '
            continue
        asciival = ord(i) - 25
        hashedtext += chr(asciival)
    return hashedtext

def unhash(text):
    unhashedtext = ''
    for i in text:
        if i == ' ':
            unhashedtext += ' '
            continue
        unhashedtext += chr(ord(i) + 25)
    return unhashedtext

def create_master():
    with open('masterpass.txt', 'w') as f:
        f.write(hash("password123"))

def check_master():
    with open('masterpass.txt', 'r') as f:
        unhashedpass = unhash(f.read())
    return unhashedpass

def update():
    if company_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror("Error", "Failed to Update Password, because of empty field")
    else:
        create_table()
        index = simpledialog.askinteger("Enter Row", "Which Row would you like to delete?",parent=app)
        password_list.delete(0,END)
        c.execute(f"UPDATE secretpassword SET 'password' = '{hash(password_entry.get())}' WHERE rowid = '{index}'")
        conn.commit()
        c.execute(f"UPDATE secretpassword SET 'company' = '{company_entry.get()}' WHERE rowid = '{index}'")
        conn.commit()
        read_from_db()

def create_table():
    global conn, c
    conn = sqlite3.connect('secretpassword.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS secretpassword (password TEXT, date_created TEXT, company TEXT)")

def insert():
    if company_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror("Error", "Failed to Insert Password, because of empty field")
    else:
        create_table()
        password_list.delete(0,END)
        x = datetime.datetime.now()
        hashedtext = hash(str(password_entry.get()))
        c.execute(f"INSERT INTO secretpassword VALUES('{hashedtext}', '{x}', '{company_entry.get()}')")
        conn.commit()
        read_from_db()

def delete():
    create_table()
    index = simpledialog.askinteger("Enter Row", "Which Row would you like to delete?",parent=app)
    deletequestion = messagebox.askquestion("DELETE PASSWORD", "Are you sure you want to delete?", icon = 'warning')
    if deletequestion == 'yes':
        c.execute(f"DELETE FROM secretpassword WHERE rowid = '{index}'")
        conn.commit()
        password_list.delete(0,END)
        read_from_db()
        print(index)
    else:
        pass

def read_from_db():
    create_table()
    c.execute('SELECT * FROM secretpassword')
    data = c.fetchall()
    i = 1
    for row in data:
        password_list.insert(END, str(i) + ". ""password: " + unhash(row[0]) + " Company: " + row[2] + ", Date Modified: " + row[1])
        i+=1

def clear():
    company_entry.delete(0, END)
    password_entry.delete(0, END)
    password_list.delete(0,END)
    read_from_db()


app = Tk()

# Password
password_label = Label(app, text='Password', font=('bold', 14), pady=20)
password_label.grid(row=0, column=0)
password_entry = Entry(app)
password_entry.grid(row=0, column=1)


# Company
company_label = Label(app, text='Company Name', font=('bold', 14), pady=20, padx= 15)
company_label.grid(row=0, column=2, sticky=W)
company_entry = Entry(app)
company_entry.grid(row=0, column=3, padx=20, pady=1)


#Listbox
password_list = Listbox(app, height=10, width=75)
password_list.grid(row=3, column=0, columnspan=5, rowspan=5, sticky=W, padx=20)

#Scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3, padx=20)

# Buttons
add_btn = Button(app, text="Add Password", width=12, command=insert)
add_btn.grid(row=2, column=0, pady=20, padx=30)

remove_btn = Button(app, text="Remove Password", width=12, command=delete)
remove_btn.grid(row=2, column=1, pady=20)

update_btn = Button(app, text="Update Password", width=12, command=update)
update_btn.grid(row=2, column=2, pady=20)

clear_btn = Button(app, text="Clear", width=12, command=clear)
clear_btn.grid(row=2, column=3, pady=20)

create_master()

running = True
tries = 0

while running:
    tries = 1 + tries
    masterpass = simpledialog.askstring("Enter Password", "Enter Master Password",parent=app)
    mastercheck = check_master()
    if masterpass == mastercheck:
        running = False
    if tries >= 50:
        quit()


read_from_db()
app.title("Password Manager")
app.geometry('615x350')
app.resizable(False, False)
app.mainloop()
