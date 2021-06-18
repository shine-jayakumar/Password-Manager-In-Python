
# Password Manager v.1
# Author: Shine Jayakumar
# Email:  shinejayakumar@yahoo.com


# MIT License
#
# Copyright (c) 2021 Shine Jayakumar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mb
from tkinter import filedialog

import pyodbc
import hashlib
import random
import string
import sys
import os
import csv
from datetime import date
from configparser import ConfigParser
import subprocess


# Populates multilist box
def update_results(rows):
    if rows:
        trvResults.delete(*trvResults.get_children())
        for row in rows:
            trvResults.insert('', 'end', values=[elem for elem in row])
    else:
        mb.showinfo('No Results', 'Nothing to show')


# show all
def refresh_results():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PasswordManager.dbo.passwords")
    rows = cursor.fetchall()
    update_results(rows)


# show frames
def enable_frames():
    passwordframe.forget()  # hide access password frame
    searchframe.pack(fill="both", expand="yes", padx=10, pady=10)
    resultframe.pack(fill="both", expand="yes", padx=10, pady=10)
    addframe.pack(fill="both", expand="yes", padx=10, pady=10)

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM PasswordManager.dbo.passwords')
    rows = cursor.fetchall()
    update_results(rows)


# sets an access password
def set_password(password):
    if password:
        hash = hashlib.sha256(password.encode()).hexdigest()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO PasswordManager.dbo.masterpassword VALUES(?)',
                       hash)
        conn.commit()
        mb.showinfo('Password Set', 'New password set')
    else:
        mb.showinfo('Password Field Empty', 'No password entered')


# check access password
def check_password(pwdfield):

    password_entered = pwdfield.get()

    if password_entered:  # is password field empty?

        cursor = conn.cursor()
        cursor.execute('SELECT TOP 1 * FROM PasswordManager.dbo.masterpassword')
        masterpassword = cursor.fetchone()

        hash = hashlib.sha256(password_entered.encode()).hexdigest()

        # if password set in db?
        if masterpassword:
            if masterpassword[0] == hash:
                enable_frames()
            else:
                mb.showerror('Invalid Password', 'Invalid Password')

        # set password if no password set
        else:
            set_pass_response = mb.askquestion('Password Not Set', 'No password set. Do you want to set it now?')
            if set_pass_response == 'yes':
                set_password(password_entered)
    else:
        mb.showinfo('Password Field Empty', 'You have not entered a password')


# filter results by url
def search_results(entSearch):

    searchText = entSearch.get()

    if searchText:
        cursor = conn.cursor()
        query = "SELECT * FROM PasswordManager.dbo.passwords WHERE website LIKE '%" + searchText + "%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        update_results(rows)

    else:
        mb.showinfo('Search Field Empty', 'Nothing to search')


# fetches all records and populates listbox
def clear_results():
    entrySearch.delete(0, END)
    refresh_results()


# adds new website
def add_new_website():
    website = entryAddWebsite.get()
    username = entryAddUsername.get()
    password = entryAddPassword.get()

    if website and username and password:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PasswordManager.dbo.passwords VALUES(?,?,?)",
                       website, username, password)
        conn.commit()
        mb.showinfo('Website Added', 'Website Added')
        entryAddWebsite.delete(0, END)
        entryAddUsername.delete(0, END)
        entryAddPassword.delete(0, END)
        refresh_results()

    else:
        mb.showerror('Fields Missing', 'One or more fields are empty')


# deletes a website
def delete_website():
    website = entryAddWebsite.get()
    username = entryAddUsername.get()
    password = entryAddPassword.get()

    if website and username and password:
        response = mb.askquestion('Confirm Delete', 'Are you sure you want to delete?')
        if response == 'yes':
            cursor = conn.cursor()
            query = f"DELETE FROM PasswordManager.dbo.passwords WHERE website='{website}' AND username='{username}' AND password='{password}'"
            cursor.execute(query)
            conn.commit()
            mb.showinfo('Website Deleted', 'Website has been deleted')
            entryAddWebsite.delete(0, END)
            entryAddUsername.delete(0, END)
            entryAddPassword.delete(0, END)
            refresh_results()

    else:
        mb.showerror('Fields Missing', 'One or more fields are empty')


# updates the website url/username/password
def update_website():
    website = entryAddWebsite.get()
    username = entryAddUsername.get()
    password = entryAddPassword.get()

    oldWebsite = tmpWebsite.get()
    oldUsername = tmpUsername.get()
    oldPassword = tmpPassword.get()

    if website and username and password:
        response = mb.askquestion('Confirm Update', 'Are you sure you want to update?')
        if response == 'yes':
            cursor = conn.cursor()
            query = f"UPDATE PasswordManager.dbo.passwords SET website='{website}', username='{username}', password='{password}' WHERE website='{oldWebsite}' AND username='{oldUsername}' AND password='{oldPassword}'"
            cursor.execute(query)
            conn.commit()
            mb.showinfo('Website Updated', 'Website has been updated')
            entryAddWebsite.delete(0, END)
            entryAddUsername.delete(0, END)
            entryAddPassword.delete(0, END)
            refresh_results()

    else:
        mb.showerror('Fields Missing', 'One or more fields are empty')


# focus on current row selected from listbox
def get_row(event):
    rowid = trvResults.identify_row(event.y)
    item = trvResults.item(trvResults.focus())
    entryAddWebsite.delete(0, END)
    entryAddUsername.delete(0, END)
    entryAddPassword.delete(0, END)

    tmpWebsite.set(item['values'][0])
    tmpUsername.set(item['values'][1])
    tmpPassword.set(item['values'][2])
    tw = item['values'][0]
    entryAddWebsite.insert(0, item['values'][0])
    entryAddUsername.insert(0, item['values'][1])
    entryAddPassword.insert(0, item['values'][2])


# generates random password
def generate_password():
    sample = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*"
    password = random.sample(sample, int(PASSLENGTH))
    password = "".join(password)
    entryAddPassword.delete(0, END)
    entryAddPassword.insert(0, password)
    tmpPassword.set(password)


# copies to clipboard
def copy_to_clipboard():

    password = tmpPassword.get()
    if password:
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(password)
        r.update()  # now it stays on the clipboard after the window is closed
        r.destroy()
    else:
        mb.showinfo('No Password', 'Nothing to copy')


def import_csv():

    rows = []

    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("All files",
                                                      "*.*")))

    if filename:

        # read csv
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)

            cursor = conn.cursor()

            # skip first row and import everything else
            for row in rows[1:]:
                cursor.execute("INSERT INTO PasswordManager.dbo.passwords VALUES(?,?,?)", row[1], row[2], row[3])
            conn.commit()
            mb.showinfo('Imported Passwords', 'Imported ' + str(csvreader.line_num - 1) + ' passwords')
            refresh_results()


def export_csv():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PasswordManager.dbo.passwords")
    rows = cursor.fetchall()

    if rows:
        filename = ''

        if EXPORT_LOCATION:
            filename = EXPORT_LOCATION + '\passwords_' + date.today().strftime("%m_%d_%Y") + '.csv'
        else:
            filename = os.environ['USERPROFILE'] + '\Documents\passwords_' + date.today().strftime("%m_%d_%Y") + '.csv'

        with open(filename, 'w', newline='') as export_fh:
            export_writer = csv.writer(export_fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            export_writer.writerow(['website', 'username', 'password'])
            for row in rows:
               # export_writer.writerow(list(row))
                export_writer.writerow(list(row))

            mb.showinfo('Export Password', 'Successfully export ' + str(len(rows)) + ' passwords\n\nPasswords saved at: ' + filename)


# initialize variables
def init_settings():
    global SERVER, USERNAME, PASSWORD, PASSLENGTH, EXPORT_LOCATION

    settings = ConfigParser()

    if settings.read('config.ini'):
        SERVER = settings.get('Server', 'servername')
        USERNAME = settings.get('Server', 'username')
        PASSWORD = settings.get('Server', 'password')
        PASSLENGTH = settings.get('Password', 'passlength')
        EXPORT_LOCATION = settings.get('Export', 'location')

    else:
        mb.showerror('Config File Missing', 'Configuration file - config.ini is missing')
        sys.exit()


def open_settings():

    subprocess.Popen([os.environ['windir'] + '\System32\\notepad.exe', 'config.ini'])


def about():
    about_text = '''
    Password Manager v.1
    Copyright (c) 2021 Shine Jayakumar
    MIT License 
    
    Author: Shine Jayakumar
    Email : shine_hack@yahoo.com
    
    Password Manager is a free password manager
    written in Python
    '''
    mb.showinfo('About', about_text)

os.chdir(os.path.dirname(__file__))

init_settings()

conn = ''

# connect with username and password
if USERNAME and PASSWORD:
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=" + SERVER + ";"
        "UID="+USERNAME+";"
        "PWD="+PASSWORD
    )

# use Windows Authentication
else:
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server="+SERVER+";"   
        "Trusted_Connection=yes;"
    )

if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM master.dbo.sysdatabases WHERE name='PasswordManager'")

    # if db doesn't exist, create it
    if not cursor.fetchall():
        conn.autocommit = True
        conn.execute('CREATE DATABASE PasswordManager')
        conn.execute('CREATE TABLE PasswordManager.dbo.masterpassword(password NVARCHAR(max))')
        conn.execute('CREATE TABLE PasswordManager.dbo.passwords(website NVARCHAR(max), username NVARCHAR(max), password NVARCHAR(max))')



# Creating tkinter window
window = Tk()
window.title('Password Manager v.1')
window.iconbitmap(r'images\password.ico')
window.geometry('650x500')
window.resizable(False, False)


# Menu bar
menubar = Menu(window)
window.config(menu=menubar)

# File menu
file_menu = Menu(menubar)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Import', command=import_csv)
file_menu.add_command(label='Export', command=export_csv)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=window.quit)

edit_menu = Menu(menubar)
menubar.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Settings', command=open_settings)


# Help Menu
help_menu = Menu(menubar)
menubar.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='About', command=about)

# to store url/username/password
# useful during update when user would change content of the text box
tmpWebsite = StringVar()
tmpUsername = StringVar()
tmpPassword = StringVar()



#password
passwordframe = LabelFrame(window, text="Master Password")
passwordframe.pack(fill="both", expand="yes", padx=10, pady=10)
Label(passwordframe, text="Password", width=10).grid(row=0, column=0, padx=1, pady=3)
entryPassword = Entry(passwordframe, show="*", width=20)
entryPassword.grid(row=0, column=1, padx=2, pady=3)
iconUnlock = PhotoImage(file=r"images\open-padlock.png")
btnUnlock = Button(passwordframe, image=iconUnlock, command=lambda: check_password(entryPassword)).grid(row=0, column=3, padx=2, pady=2)


# Search
searchframe = LabelFrame(window, text="Search")
Label(searchframe, text="Search").grid(row=0, column=0, padx=1, pady=3)
entrySearch = Entry(searchframe, width=20)
entrySearch.grid(row=0, column=1, padx=2, pady=3)

iconSearch = PhotoImage(file=r"images\search.png")
iconClear = PhotoImage(file=r"images\close.png")
btnSearch = Button(searchframe, image=iconSearch, command=lambda: search_results(entrySearch)).grid(row=0, column=3, padx=2, pady=2)
btnClear = Button(searchframe, image=iconClear, command=clear_results).grid(row=0, column=4, padx=2, pady=2)



# Website/Username/Password - Results
resultframe = LabelFrame(window, text="Passwords")
trvResults = Treeview(resultframe, columns=(1,2,3), show="headings", height="6", selectmode="browse")
trvResults.pack()
trvResults.heading(1, text="Website")
trvResults.heading(2, text="Username")
trvResults.heading(3, text="Password")
trvResults.bind('<Double 1>', get_row)

vertical_sbar = Scrollbar(trvResults, orient='vertical', command=trvResults.yview)
trvResults.configure(yscrollcommand = vertical_sbar.set)
vertical_sbar.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)

# Add new
addframe = LabelFrame(window, text="Add New")
Label(addframe, text="Website URL").grid(row=0, column=0, padx=1, pady=3)
entryAddWebsite = Entry(addframe, width=50)
entryAddWebsite.grid(row=0, column=1, padx=2, pady=3)

Label(addframe, text="Username").grid(row=1, column=0, padx=1, pady=3)
entryAddUsername = Entry(addframe, width=50)
entryAddUsername.grid(row=1, column=1, padx=2, pady=3)

Label(addframe, text="Password").grid(row=2, column=0, padx=1, pady=3)
entryAddPassword = Entry(addframe, width=50)
entryAddPassword.grid(row=2, column=1, padx=2, pady=3)
iconGenPwd = PhotoImage(file=r"images\magic-wand.png")
btngenerate_password = Button(addframe, image=iconGenPwd, command=generate_password).grid(row=2, column=2, padx=1, pady=2)

# icons for buttons
iconAdd = PhotoImage(file=r"images\add.png")
iconUpdate = PhotoImage(file=r"images\update.png")
iconDelete = PhotoImage(file=r"images\trash.png")
iconCopy = PhotoImage(file=r"images\copy.png")



btnCopy = Button(addframe, image=iconCopy, command=copy_to_clipboard).grid(row=2, column=3, padx=(10,0), pady=0)
btnadd_new_website = Button(addframe, image=iconAdd, command=add_new_website).grid(row=2, column=5, padx=1, pady=0)
btnupdate_website = Button(addframe, image=iconUpdate, command=update_website).grid(row=2, column=6, padx=1, pady=0)
btndelete_website = Button(addframe, image=iconDelete, command=delete_website).grid(row=2, column=7, padx=1, pady=0)


window.mainloop()