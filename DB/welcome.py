import Tkinter as tk
import eg
import login
import database_creator
from PIL import ImageTk, Image

# from http://effbot.org/tkinterbook/entry.html

def display():
    '''
    Display the introduction screen of application
    '''
    root.destroy()
    #import login
    login.main()

def main():
    '''
    This function creates the framework for the graphical user interface. Using the GUI, the admin
    and the user can login to run the compliance test. The GUI would create a portal to ask for the
    login credentials of anyone who wishes to run the compliance test.

    '''
    global root
    root= tk.Tk()
    root.geometry('2024x2024')
    root.title('WELCOME FOLKS')

    #frame for window margin
    parent = tk.Frame(root, padx=10, pady=10)
    parent.pack(fill=tk.BOTH, expand=True)

    #button to attempt to login
    path = "/home/netman/DB/compliance.jpg"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tk.Label(root, image = img)
    panel.pack(side = "top", fill = "both")

    b = tk.Button(parent, borderwidth=4, text="Launch Compliance Checker", width=100, pady=8, command=display)
    b.pack(side=tk.BOTTOM)
    parent.mainloop()




if __name__ == "__main__":
    main()
