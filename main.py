import keyboard

def on_press(event):
    print(f"name: {event.name}\ncode:{event.scan_code}\ntime:{event.time}")
    with open("dat.log","a") as logfile:
      logfile.write(f"\n{event.time}:Key {event.name} pressed (Code:{event.scan_code})")
    with open("dat.csv","a") as datfile:
      datfile.write(f"\n{event.time},{event.name}, {event.scan_code}")

keyboard.on_press(on_press)
keyboard.wait()
