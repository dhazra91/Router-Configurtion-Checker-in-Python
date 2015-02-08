import database_creator
import login
import initiate

def admin(user):
    '''
    This function creates the
    '''

    while True:
        print "************  Welcome to Admin Console  *****************"
        print ""
        print "Welcome Admin :"+user
        print ""
        print " 1. View Existing Users "
        print " 2. Add  New Users"
        print " 3. Delete Existing Users"
        print " 4. View Available Templates"
        print " 5. Exit to Login again "



        choice = raw_input(" Enter your choice : ")
        if choice == "1":
           database_creator.view()

        elif choice == "2":
           user = raw_input(" Username: ")
           password = raw_input(" Password: ")
           role = raw_input(" Role(admin/user): ")
           database_creator.insert(user,password,role)

        elif choice == "3":
           user = raw_input(" Username: ")
           role = raw_input(" Role(admin/user): ")
           database_creator.delete(user,role)

        elif choice == "4":
           database_creator.list_dir()

        elif choice == "5":
           login.main()

def user(user):
    while True:
        print "*************  Welcome to User Console  *****************"
        print ""
        print "Welcome User :"+user
        print ""
        print "1.Start Compliance Check "
        print "2.Exit to Login again "

        choice = raw_input(" Enter your choice : ")

        if choice == "1":
            initiate.main()
        elif choice == "2":
            login.main()








