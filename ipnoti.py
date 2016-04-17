#!/bin/python2.7

import smtplib
import subprocess
import sys

# This will check if our public IP changed by comparing the freshly pulled
# IP against our pubip file that contains the last pulled IP address
def checkIfIpChanged(ip, fpath):
    ipFile = open(fpath + ".pubip", "r")
    if(ipFile.read() == ip):
        ipFile.close()
        return False
    else:
        ipFile.close()
        writeNewIPToFile(ip, fpath)
        return True

# This runs everytime the script does to verify the pubip file exists because
# if it didn't exist and we ran the rest of the script it would crash due to
# the way Python's open function works.
def doesPubIPfileExist(fpath):
    ipFile = subprocess.Popen(["ls", "-a", fpath],
                              stdout=subprocess.PIPE).communicate()[0]
    if".pubip" in ipFile:
        return
    else:
        ipFile = open(fpath + ".pubip", "w")
        ipFile.write("0.0.0.0")
        ipFile.close()
        return

# This will write the new IP to the .pubip file if it has changed
def writeNewIPToFile(ip, fpath):
    ipFile = open(fpath + ".pubip", "w")
    ipFile.write(ip)
    ipFile.close()

# Sends our email with the new IP if it has changed.
def emailNewIP(ip, uname, passwd):
    fromaddr = uname
    toaddrs  = 'mathew.robinson3114@gmail.com'
    msg = ip


    # Credentials (if needed)
    username = uname
    password = passwd

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# Interperets the command line args we get and returns the usable values
def scanCmdArguments():
    for index, arg in enumerate(sys.argv):
        if arg == "-f" or arg == "--file":
            # if we see the -p flag then the next element will be a space so
            # we go to the next next element.
            fpath = sys.argv[index + 1]
        elif arg ==  "-u" or arg == "--username":
            uname = sys.argv[index + 1]
        elif arg == "-p" or arg == "--password":
            passwd = sys.argv[index + 1]
    return fpath, uname, passwd

fpath, uname, passwd = scanCmdArguments()
doesPubIPfileExist(fpath)
publicIP = subprocess.Popen(["curl", "icanhazip.com"], stdout=subprocess.PIPE).communicate()[0]
if(checkIfIpChanged(str(publicIP), fpath)):
    emailNewIP(str(publicIP), uname, passwd)
