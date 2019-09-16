#########################################################################################################################
# USED TO DELETE CTL FILE AND TOGGEL PROVISIONING ON DEVICES RUNNING CE8 CE9 and TC7                                    #
#  Note : Create a text file with IP's on every new line and save it as ip.txt                                          #
#         Create a text file with credentials in the following format (username,password)                               #
#         Result can be seen in the same folder with file name Report.txt                                               #
#         If you face any difficulty please reach me at prakuma9@cisco.com                                              #
#                                                                                                                       #
#########################################################################################################################




import paramiko
import re
import time

# Reading credentials
credentials = input(str("Enter the filename with credentials : "))
raw_creds = (open(credentials, 'r').readlines())
creds = raw_creds[0].split(',')
username = creds[0]
password = creds[1]

# Generating reports 
reporting_as_txtfile = (open('Report.txt','a'))

#Commands to be executed on CE8
ce8 = ['xpreferences accessmode internal','xCommand provisioning CUCM CTL Delete','xpreferences accessmode external','xConfiguration Provisioning Mode: OFF', 'xConfiguration Provisioning Mode: CUCM']

#Commands to be executed on CE9
ce9 = ['xpreferences accessmode internal','xCommand Security Certificates CUCM CTL Delete','xpreferences accessmode external','xConfiguration Provisioning Mode: OFF','xConfiguration Provisioning Mode: CUCM']

#Commands to be executed on TC7
tc7 = ['xCommand provisioning CUCM CTL Delete','xConfiguration Provisioning Mode: OFF','xConfiguration Provisioning Mode: CUCM']

def deleting_cucm_cert(ip):
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,username=username, password=password)
        connection = ssh.invoke_shell()
        time.sleep(1)
        connection.send("xstatus SystemUnit Software Version"+"\n")
        time.sleep(2)
        output = connection.recv(65535)
        output1 = str(output.decode('utf-8'))
        test1 = re.findall('ce9[.a-zA-Z0-9]*', output1)
        
        #######################################################If its CE 9 
        if test1 :
            print("Its a CE9 device")
            for i in ce9:
                try : 
                    connection.send(i + "\n")
                    time.sleep(2)
                    res = connection.recv(65535)
                    res1 = str(res.decode('utf-8'))
                    test = re.findall('OK', res1)
                    if test:
                        print("Executing commands"+ i + "\n")
                except Exception as e:
                    print(e.args)
                    pass
            reporting_as_txtfile.write(ip + "," +"Success"+"\n")
            print("DELETED CTL FILE AND TOGGELED PROVISIONING FOR DEVICE WITH IP "+ ip + "\n")
            exit
        
    
        ###################################################If its TC 7
        test2 = re.findall('TC7[.a-zA-Z0-9]*',output1)
        if test2:
            print("its a TC7 Device")
            for i in tc7:
                try : 
                    connection.send(i + "\n")
                    time.sleep(2)
                    res = connection.recv(65535)
                    res1 = str(res.decode('utf-8'))
                    test = re.findall('OK', res1)
                    if test:
                        print("Executing commands"+ i + "\n")
                except Exception as e:
                    print(e.args)
                    pass
            reporting_as_txtfile.write(ip + "," +"Success"+"\n")
            print("DELETED CTL FILE AND TOGGELED PROVISIONING FOR DEVICE WITH IP "+ ip + "\n")
            exit
        
        ####################################################If its CE 8
        test3 = re.findall('ce8[.a-zA-Z0-9]*',output1)
        
        if test3:
            print("Its a CE8 Device")
            for i in ce8:
                try : 
                    connection.send(i + "\n")
                    time.sleep(2)
                    res = connection.recv(65535)
                    res1 = str(res.decode('utf-8'))
                    test = re.findall('OK', res1)
                    if test:
                        print("Executing commands"+ i + "\n")
                except Exception as e:
                    print(e.args)
                    pass
            reporting_as_txtfile.write(ip + "," +"Success"+"\n")
            print("DELETED CTL FILE AND TOGGELED PROVISIONING FOR DEVICE WITH IP "+ ip + "\n")
            exit
    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials")
    except paramiko.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)


# Reading IP
ip = (open('ip.txt', 'r').readlines())
k = []
for i in ip:
    j = ((i.strip(',')).rstrip("\n"))
    deleting_cucm_cert(j)
