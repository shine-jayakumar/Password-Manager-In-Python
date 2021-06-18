# Password Manager v.1
A  password manager with GUI written in Python. It can save website URLs, username, and passwords so you do not have to remember them. You can also generate random passwords on the go.

<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/passwordmanager.png" alt="Password Manager"/>

### Why a password Manager?
A couple of months ago I stumbled upon a YouTube video that talked about how much of your information is floating around on the internet and a simple search can reveal so much about you. One compromised website can reveal your password putting all other accounts at risk

A website like [have i been pwned?](https://haveibeenpwned.com/ "have i been pwned?") can show you if one of the services you signed up for was ever compromised. 

In a [survey conducted by Google](https://www.infosecurity-magazine.com/news/google-survey-finds-two-users/ "survey conducted by Google") with a pool of 3000 people, 51% admitted that they use the same favourite password for different websites.
I admit I am guilty too of this bad habit. Most of the times, it’s not the lack of knowledge that lands us into trouble but negligence.
I took my first step - I decided to write a simple password manager. Now, you can write your own or, just run this one.

### Features
- Save website, username, and passwords
- Quickly search websites
- Generate random password on the go
- Update and Delete passwords
- Import/Export passwords
- Protect passwords with a Master Password

### Requirements
- Password Manager was tested in Windows 10
- [SQL SERVER](https://www.microsoft.com/en-in/sql-server/sql-server-downloads "SQL SERVER")
- Python 3.7
- pyodbc==4.0.30

### Install Requirements
`pip install -r requirements.txt`

### How to launch?
`python passwordmanager.py` 

**OR**

`pythonw passwordmanager.py`

Set a **master password**

<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/setmasterpassword.JPG" alt="Set Master Password"/>

### Creating Desktop Shortcut
1. Go to **Desktop**, **right-click** and select **New**, then **Shortcut**
<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/shortcut_1.JPG" alt="Shortcut"/>

2. Type in the complete location for **pythonw.exe**, followed by location for **PasswordManager.py** enclosed in double quotes, 
and click on **Next**

**example**: 
c:\python38\pythonw.exe "d:\PasswordManager\passwordmanager.py"

<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/shortcut_2.JPG" alt="Shortcut"/>

3. Name the Shortcut as PasswordManager, and click on **Finish**
<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/shortcut_3.JPG" alt="Shortcut"/>

4. Right-click on the newly created shortcut, select **Properties**, set **Start In** directory to where passwordmanager.py is in, and click on **OK**

**example:** D:\PythonProjects\PasswordManager\

<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/shortcut_4.JPG" alt="Shortcut"/>

### Import Passwords
[How to export saved passwords in Google Chrome?](https://support.google.com/chrome/answer/95606?co=GENIE.Platform%3DDesktop&hl=en "articles for instructions on exporting your passwords from Google Chrome")

[How to export saved passwords in Microsoft Edge?](https://support.nordpass.com/hc/en-us/articles/360005501797-How-to-export-passwords-from-Edge- "How to export saved passwords in Microsoft Edge?")

Once passwords are exported to a .csv file, follow these steps:

1. Click on **Import** from File Menu in Password Manager
2. Browse to the location and select the .csv file containing passwords

<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/import.JPG" alt="Import Passwords"/>

### Export Passwords

Click on **Export** from the File Menu in Password Manager

<img src="https://github.com/shine-jayakumar/Password-Manager-In-Python/blob/main/ReadMe_Images/export.JPG" alt="Export Passwords"/>

Passwords will be exported to the location specified in 
`location=` 
in config.ini

Default export location is %USERPROFILE%\Documents
