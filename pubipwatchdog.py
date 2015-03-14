#!/bin/python2.7

import smtplib
import subprocess
import sys

# This will check if our public IP changed by comparing the freshly pulled
# IP against our pubip file that contains the last pulled IP address
def checkIfIpChanged(ip):
    ipFile = open(sys.argv[1] + ".pubip", "r")
    if(ipFile.read() == ip):
        ipFile.close()
        return False
    else:
        ipFile.close()
        writeNewIPToFile(ip)
        return True

def doesPubIPfileExist():
    ipFile = subprocess.Popen(["ls", "-a", sys.argv[1]], stdout=subprocess.PIPE).communicate()[0]
    if".pubip" in ipFile:
        return
    else:
        ipFile = open(sys.argv[1] + ".pubip", "w")
        ipFile.write("0.0.0.0")
        ipFile.close()
        return

# This will write the new IP to the .pubip file if it has changed
def writeNewIPToFile(ip):
    ipFile = open(sys.argv[1] + ".pubip", "w")
    ipFile.write(ip)
    ipFile.close()

# Sends our email with the new IP if it has changed.
def emailNewIP(ip):
    fromaddr = 'pubipwatchdog@gmail.com'
    toaddrs  = 'mathew.robinson3114@gmail.com'
    msg = ip


    # Credentials (if needed)
    username = ''
    password = ''

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# This is because I like C get over it.
def main():
    doesPubIPfileExist()
    publicIP = subprocess.Popen(["curl", "icanhazip.com"], stdout=subprocess.PIPE).communicate()[0]
    if(checkIfIpChanged(str(publicIP))):
        #emailNewIP(str(publicIP))
        print(publicIP)
        print("SUccess")

main()
