#!/bin/python3

import smtplib
import subprocess
import sys
import os
import urllib.request

homedir = os.getenv("HOME", "")
username = os.getenv("IPNOTI_USERNAME", "")
password = os.getenv("IPNOTI_PASSWORD", "")
target_email = os.getenv("IPNOTI_TARGET", "")

# This will check if our public IP changed by comparing the freshly pulled
# IP against our pubip file that contains the last pulled IP address
def checkIfIpChanged(ip):
    with open(homedir + ".pubip", "r+") as ipFile:
        if(ipFile.read() == ip):
            return False
        else:
            ipFile.write(ip)
            return True

# Sends our email with the new IP if it has changed.
def emailNewIP(ip):
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(username, target_email, ip)
    server.quit()

publicIP = urllib.request.urlopen("http://canhazip.com/").read()
if(checkIfIpChanged(str(publicIP))):
    emailNewIP(str(publicIP))
