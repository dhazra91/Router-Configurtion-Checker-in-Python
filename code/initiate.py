import time
import networkx as nx #to create the final topology graph showing the compliant and non-compliant routers
import Tkinter as tk #to create the compliance test GUI
import matplotlib.pyplot as plt
import datetime
import tftpy
import os
import difflib
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PIL import ImageTk, Image
import twilio_module as inform #to send a text to the network admin regarding the violation of the SLA
def accept_topology():
    while True:
        input=raw_input("Enter IP or X for proceeding:")
        if input != "X":
            ip_list.append(input)
            ip_flag.update({input:"2"})
        else:
             break

    for ip in ip_list:
        get_templates(ip)

def get_templates(ip):

    '''
    This function checks if the template for the orginal start-up config file exists for each of the 3 routers. If not, it
    downloads and saves the original start-up config file from each of the routers and creates a reference template for all 3.
    If it exists, it downloads and saves the current start-up config file and creates the template from it thereafter. Now it
    compares this new template with the reference template.Additionally, the original start-up and the crrent start-up config
    files are also compared.
    '''


    temp_file= "/home/netman/DB/"+ip+"template_final"

    if not os.path.exists(temp_file):
        print "CREATING TEMPLATES"
        connection = tftpy.TftpClient(ip, 69)
        connection.download('/startup-config',"/home/netman/DB/"+ip+"template")
        make_templates("/home/netman/DB/"+ip+"template",0)
    else:
        file_name="/home/netman/DB/"+ip+"current_template"
        #'fine_name' and 'file_name_compare' are the same.
        connection = tftpy.TftpClient(ip, 69)
        connection.download('/startup-config',file_name)
        make_templates(file_name,1)
        compare_templates(file_name+"_compare",temp_file,ip)
        compare_config(file_name,"/home/netman/DB/"+ip+"template",ip)


def make_templates(path,flag):

    '''
    This function creates the templates for the orginal start-up config file and the current start-up config file
    of the router corresponding to the IP being passed. These templates would check the number of networks issues under the routing
    protocols like RIP,OSPF and also check for route redistribution and SNMP configurations.
    '''

    if flag == 0:
        f=open(path)
        w=open(path+"_final","w+")
    else:
        f=open(path)
        w=open(path+"_compare","w+")


    l=f.readlines()
    for line in l:
        if line.startswith(" ip address"):
           w.write(line.split()[0]+" "+line.split()[1]+" XXX"+" "+"XXX\n")
        elif line.startswith("hostname"):
            w.write (line.split()[0]+" XXX")
        elif line.startswith("ip domain name"):
            w.write (line.split()[0]+" "+line.split()[1]+" "+line.split()[2]+" XXX\n")

        elif line.startswith("router ospf"):
            w.write (line.split()[0]+" "+line.split()[1]+" "+"X\n")
        elif line.startswith(" redistribute"):
            w.write (line.split()[0]+" "+line.split()[1]+" "+line.split()[2]+" XXX "+line.split()[4]+"\n")
        elif line.startswith(" network"):
            w.write (line.split()[0]+" "+"XXX\n")
        elif line.startswith("router rip"):
            w.write(line+"\n")
        elif line.startswith(" version"):
            w.write (line.split()[0]+" XXX\n")
        elif line.startswith(" redistribute"):
            w.write (line.split()[0]+" "+line.split()[2]+" XXX "+line.split()[5]+"XXX\n")
        elif line.startswith(" network"):
            w.write (line.split()[0]+" XXX\n")

        elif line.startswith("rmon event"):
            w.write (line.split()[0]+" "+line.split()[1]+" XXX\n")
        elif line.startswith("rmon alarm"):
            w.write (line.split()[0]+" "+line.split()[1]+" XXX\n")
        elif line.startswith("snmp-server"):
            w.write (line.split()[0]+"  XXX\n")
        else:
            w.write(str(line.strip())+"\n")

    w.close()


def compare_templates(current_template,root_template,ip):
    '''
    This function compares the templates for the orginal start-up config file and the current start-up config file
    corresponding to the router associated with the IP being passed. Those templates that match the original template are
    flagged with 1 and those that do not, are flagged with 0.
    '''
    f1=open(current_template,"r")
    f2=open(root_template,"r")

    a1=f1.readlines()
    a2=f2.readlines()

    if a1 != a2:
        print "not equal"
        write_topology_information(0,ip)


        #store into a directory with timestamp
    else:
        write_topology_information(1,ip)
        print "equal"


    f1.close()
    f2.close()

def compare_config(current_path,old_path,ip):
    '''
    The function 'compare_config' creates two files corresponding to the current and previous versions of the configuration
    files for each of the router. It then compares these two files and prints out the differences between these two versions
    and retains files for both the current and the previous versions and sends these differences to the network admin
    via both email and text to his/her cellphone.
    '''

    if ip=='198.51.100.3':
        router='Router 1'
    elif ip=='198.51.100.4':
        router='Router 2'
    elif ip=='198.51.100.5':
        router='Router 3'
    else:
        print "Invalid input"

    difference=[]
    file1 = open(current_path)
    file2 = open(old_path)
    current_file = file1.readlines()
    old_file = file2.readlines()
    if current_file != old_file:
        diff_object = difflib.Differ()
        diff_items = diff_object.compare(old_file, current_file)

        for line in diff_items:
            if line.startswith('- ') or line.startswith('+ '):
                difference.append(line)
        content='Please find the following configuration mismatch for '+str(router)+ '\nSLA violated!!!!\n'+str(difference)
        send_mail(content)
        inform.inform_phone(content)


def write_topology_information(flag,ip):
    '''
    This function updates the dictionary such that every management IP is tagged with a flag. If the flag for a
    router has not been received, it is automatically initialized with a flag of 2. It is ony when the final flag of the
    IP is either 0 or 1, the final compliance test results are dispalyed in the form of a connected topology with red and
    green routers.
    '''

    for key in ip_flag:
        if key == ip:
            ip_flag.update({key:flag})
    print ip_flag
    print len(ip_flag)
    count = 0
    for key in ip_flag:
        if ip_flag[key] == '2' :
           count = count+1

    print count
    if count==0:

        take_topology_decision(ip_flag)

def take_topology_decision(ip_flag):
    '''
    This function creates a list of the flags associated with each router. The 1st value, 2nd value, 3rd value of the list to
    the 1st, 3rd and 2nd router respectively. Depending on these values, the compliant routers are marked to be colored in green and the non-compliant routers are marked
    to be colored in red.
    '''
    print "Take topology loop"
    actionset=[]
    for key in ip_flag:
        actionset.append(ip_flag[key])

    print "Action Set"+str(actionset)
    sla_status(actionset)
    if actionset == [0,0,0]:
        display_topology([1,2,3],[])

    elif actionset == [0,0,1]:
        display_topology([1,3],[2])

    elif actionset == [0,1,0]:
        display_topology([1,2],[3])

    elif actionset == [0,1,1]:
        display_topology([1],[2,3])

    elif actionset == [1,0,0]:
        display_topology([2,3],[1])

    elif actionset == [1,0,1]:
        display_topology([3],[1,2])

    elif actionset == [1,1,0]:
        display_topology([2],[1,2])

    elif actionset == [1,1,1]:
        display_topology([],[1,2,3])
        message="SLA met for all 3 routers.\n No configuration mismatch observed."
        send_mail(message)
        inform.inform_phone(message)
    else:
        display_topology([2,3],[1])

def display_topology(list_red,list_green):
    '''
    This function creates the topology showing the compliant routers in red and the con-compliant routers in red.
    Each router is labelled with its respective management IP. The spring nature of topology places the routers in
    the network in a random manner such that router 1 is connected to router 2, which in turn is connected to router 3.
    '''

    print "Trying to Generate Graph"
    G=nx.cubical_graph()
    pos=nx.spring_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,
                           nodelist=list_green,
                           node_color='g',
                           node_size=500)
    nx.draw_networkx_nodes(G,pos,
                           nodelist=list_red,
                           node_color='r',
                           node_size=500)
    nx.draw_networkx_edges(G,pos,
                       edgelist=[(1,2),(2,3)],
                       width=5,alpha=0.5,edge_color='b')


    labels= {}
    labels[1]=ip_list[0]
    labels[2]=ip_list[1]
    labels[3]=ip_list[2]

    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    plt.savefig("/home/netman/graphs/photo.png")
    plt.show()


def sla_status(action_set):
    '''
    This function creates a red circle indicating SLA violation and  a green circle to indicate
    SLA conformity.

    '''
    global root
    root= tk.Tk()
    root.geometry('600x600')
    root.title('SLA STATUS')

    #frame for window margin
    parent = tk.Frame(root, padx=10, pady=10)
    parent.pack(fill=tk.BOTH, expand=True)
    #button to attempt to login


    if sum(action_set)!= 3:
       path = "/home/netman/DB/rc.png"
       #path = "/home/netman/Fall2014/comp.jpg"
       img = ImageTk.PhotoImage(Image.open(path))
       panel = tk.Label(root, image = img)
       panel.pack(side = "top", fill = "both")
    else:
       path = "/home/netman/DB/gc.jpg"
       #path = "/home/netman/Fall2014/comp.jpg"
       img = ImageTk.PhotoImage(Image.open(path))
       panel = tk.Label(root, image = img)
       panel.pack(side = "top", fill = "both")


    parent.mainloop()


def send_mail(message):
    '''
    This function sends an e-mail using SMTP to a network admin with information regarding the configuration
    mismatch between the current start-up config and the original sart-up config.
    '''

    fromaddr="deha0322rosa6650@gmail.com"
    toaddr="deha0322rosa6650@gmail.com"
    msg=MIMEMultipart()
    msg['From']=fromaddr
    msg['To']=toaddr
    msg['Subject']="Network Alert"
    msg.attach(MIMEText(message,'plain'))
    img_data = open("/home/netman/graphs/photo.png", 'rb').read()
    image = MIMEImage(img_data, name=os.path.basename("/home/netman/graphs/photo.png"))
    msg.attach(image)

    server = smtplib.SMTP('smtp.gmail.com', '587')
    server.ehlo()
    server.starttls()
    server.login('deha0322rosa6650@gmail.com', 'australia12')
    text=msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def main():

    global ip_list
    ip_list=[]
    global ip_flag
    ip_flag={}
    accept_topology()

if __name__ == "__main__":
    main()
