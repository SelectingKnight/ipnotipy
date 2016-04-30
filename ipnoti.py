#!/bin/python3

import smtplib
import requests
import subprocess
import sys
import os

homedir = os.getenv("HOME", "") + "/"
username = os.getenv("IPNOTI_USERNAME", "")
password = os.getenv("IPNOTI_PASSWORD", "")
target_email = os.getenv("IPNOTI_TARGET", "")

# This will check if our public IP changed by comparing the freshly pulled
# IP against our pubip file that contains the last pulled IP address
def hasIpChanged(ip):
    with open(homedir + ".pubip", "r+") as ipFile:
        if ipFile.read().strip() in ip.strip():
            return False
        else:
            ipFile.seek(0)
            ipFile.truncate()
            ipFile.write(ip)
            return True

# Sends our email with the new IP if it has changed.
def emailNewIP(ip):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(username, target_email, ip)
    server.quit()

r = requests.get("http://canhazip.com/")
ip = r.text
if(hasIpChanged(ip)):
    emailNewIP(ip)
