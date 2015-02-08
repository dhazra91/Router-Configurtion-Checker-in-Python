import sqlite3

def view():
    '''
    This function enables the admin to view the existing users who have access to the compliance test
    '''
    cursor=db.cursor()
    cursor.execute("select * from deb_users")
    data = cursor.fetchall()
    for d in data:
      print d[1]+"|"+d[2]+"|"+d[3]

def insert(name,password,role):
    '''
    This function enables the admin to add the login credentials of the user and his/her role to the list of existing
    users who have access to the compliance test
    '''
    cursor=db.cursor()
    cursor.execute("INSERT INTO deb_users(name,pass,role)VALUES(?,?,?)",(name,password,role))
    db.commit()

def delete(name,role):
    '''
    This function enables the admin to delete any existing users who have access to the compliance test
    '''
    cursor=db.cursor()
    cursor.execute("DELETE FROM deb_users where name= ? and role=?",(name,role))
    db.commit()

def check(name,password):
    '''
    THe function checks the login credentials of the user and returns the role of the user
    '''
    cursor=db.cursor()
    cursor.execute("select * from deb_users where name= ? and pass= ?",(name,password))
    data = cursor.fetchall()
    for d in data:
      if d[1]==name and d[2]==password:
          return d[3]+" "+d[1]
      else:
          pass

def create_table():
    '''
    It creates a new table of users
    '''
    cursor=db.cursor()
    cursor.execute('''CREATE TABLE deb_users(id integer,name text,pass text,role text);''')

def list_dir():
    '''
    It lists down the final templates which are used for comparison.
    '''
    import os

    for filename in os.listdir("/home/netman/DB"):
        print  "-"+filename

db=sqlite3.connect("/home/netman/DB/shaktimaan.db")
view()


