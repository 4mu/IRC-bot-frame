import socket
import ssl
import time
import datetime
import requests

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#HOST = "irc.libera.chat"
HOST = "" # server
PORT = 6697 # port of server
NICK = "" # Bot nickname
CHANNEL = "" # channel to join
start_time = datetime.datetime.now()

NICKSERV_USERNAME = "" # Username for nickserv
NICKSERV_PASSWORD = "" # Password for nickserv

face_response = ["idk", "woah", "rules"]

wrsock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1)
wrsock.connect((HOST, PORT))

nick_data = (f"NICK {NICK}\r\n")
wrsock.send(nick_data.encode())

username_data = ("USER uname uname2 uname3 : uname \r\n") # sets username
wrsock.send(username_data.encode())

wrsock.send(f"PRIVMSG NickServ :identify {NICKSERV_USERNAME} {NICKSERV_PASSWORD} \r\n".encode()) # signs into nickserv

wrsock.send("JOIN {CHANNEL} \r\n".encode())



def uptime():
	current_time = datetime.datetime.now()
	difference = current_time - start_time
	difference = str(difference - datetime.timedelta(microseconds = difference.microseconds))
	wrsock.send(f"PRIVMSG {CHANNEL} :Uptime: {difference}\r\n".encode())


def ipcommand(ip):
    if ip==ip:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        if res['status'] == 'success':
            wrsock.send(f"PRIVMSG {CHANNEL} :IP Info\r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :=========\r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ IP ]   ::   [ {ip} ]\r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ COUNTRY ]   ::   [ {res['country']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ REGION ]   ::   [ {res['regionName']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ CITY ]   ::   [ {res['city']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ ZIP ]   ::   [ {res['zip']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ TIMEZONE ]   ::   [ {res['timezone']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ ISP ]   ::   [ {res['isp']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ ORGANIZATION ]   ::   [ {res['org']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ LATITUDE ]   ::   [ {res['lat']} ] \r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :[ LONGITUDE ]   ::   [ {res['lon']} ] \r\n".encode())
            print("ip cmd executed")
        else:
            wrsock.send("PRIVMSG {CHANNEL} :Please enter a valid IP. \r\n".encode())



while True:

    result = wrsock.recv(1024).decode("utf-8")

    print(result)

    if result.find("?uptime") > -1:
        uptime()

    if result.find("?ip") > -1:
        try:
            ipcmd = result.split(":")[1]
            ip = ipcmd[4:-2]
            ipcommand(ip)
            print(f"'{ip}'")
        except:
            wrsock.send(f"PRIVMSG {CHANNEL} :Use me right!\r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :Usage: ?ip <ipv4>\r\n".encode())
            wrsock.send(f"PRIVMSG {CHANNEL} :Perhaps there was an error?\r\n".encode())

    if len(result) == 0:
        continue