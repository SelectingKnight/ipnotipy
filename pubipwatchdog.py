import smtplib
import subprocess

# This will check if our public IP changed by comparing the freshly pulled
# IP against our pubip file that contains the last pulled IP address
def checkIfIpChanged(ip):
    ipFile = open("/home/mathew/.pubip", "r")
    if(ipFile.read() == ip):
        ipFile.close()
        return False
    else:
        ipFile.close()
        writeNewIPToFile(ip)
        return True

# This will write the new IP to the .pubip file if it has changed
def writeNewIPToFile(ip):
    ipFile = open("/home/mathew/.pubip", "w")
    ipFile.write(ip)
    ipFile.close()

# Sends our email with the new IP if it has changed.
def emailNewIP(ip):
    fromaddr = 'pubipwatchdog@gmail.com'
    toaddrs  = 'mathew.robinson3114@gmail.com'
    msg = ip


    # Credentials (if needed)
    username = 'pubipwatchdog'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# This is because I like C get over it.
def main():
    publicIP = subprocess.Popen(["curl", "icanhazip.com"], stdout=subprocess.PIPE).communicate()[0]
    print("String of PublicIP " + str(publicIP))
    if(checkIfIpChanged(str(publicIP))):
        #emailNewIP(str(publicIP))
        print(publicIP)
    else:
        print("IP didn't change.")

main()
