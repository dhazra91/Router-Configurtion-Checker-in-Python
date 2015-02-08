import Tkinter as tk
import eg
import database_creator

# from http://effbot.org/tkinterbook/entry.html

def make_entry(parent, caption, width=None, **options):

    tk.Label(parent, text=caption).pack(side=tk.TOP)
    entry = tk.Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=tk.TOP, padx=10, fill=tk.BOTH)
    return entry

def enter(event):
    check_password()

def check_password():
    '''
    This function checks the login credentials and displays access based menus
    '''
    role=database_creator.check(user.get(),password.get())
    print role
    if role == None:
       print "Incorrect Credentials"
       main()
    else:
       root.destroy()

    if role.split()[0]== "admin":
        #print "ADMIN"
        eg.admin(role.split()[1])
    else:
        #print "USER"

        eg.user(role.split()[1])

def main():
    global root
    root= tk.Tk()
    root.geometry('300x160')
    root.title('Login')

    #frame for window margin
    parent = tk.Frame(root, padx=10, pady=10)
    parent.pack(fill=tk.BOTH, expand=True)

    #entries with not shown text
    global user
    user= make_entry(parent, "User name:", 16)
    global password
    password = make_entry(parent, "Password:", 16, show="*")

    #button to attempt to login
    b = tk.Button(parent, borderwidth=4, text="Login", width=10, pady=8, command=check_password)
    b.pack(side=tk.BOTTOM)
    password.bind('<Return>', enter)

    user.focus_set()
    parent.mainloop()

if __name__ =="__main__":
    main()

