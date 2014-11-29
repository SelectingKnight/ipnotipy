import smtplib
from subprocess import call

# This will check if our public IP changed by comparing the freshly pulled
# IP against our pubip file that contains the last pulled IP address
def checkIfIpChanged(ip):
    ipFile = open("/home/mathew/.pubip", "r")
    if(ipFile.read() == ip):
        return False
    else:
        writeNewIPToFile(ip)
        return True

# This will write the new IP to the .pubip file if it has changed
def writeNewIPToFile(ip):
    ipFile = open("/home/mathew/.pubip", "w")
    ipFile.write(ip)

# Sends our email with the new IP if it has changed.
def emailNewIP(ip):
    fromaddr = 'pubipwatchdog@gmail.com'
    toaddrs  = 'mathew.robinson3114@gmail.com'
    msg = ip


    # Credentials (if needed)
    username = 'pubipwatchdog'
    password = 'beans187'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# This is because I like C get over it.
def main():
    publicIP = call(["curl", "icanhazip.com"])
    if(checkIfIpChanged(string(publicIP)):
        emailNewIP(string(publicIP))
    else:
        print("IP didn't change.")

main()
