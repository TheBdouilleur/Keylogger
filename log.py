import keyboard

def log_keyboard_events():
    def on_press(event):
        print(f"name: {event.name}\ncode:{event.scan_code}\ntime:{event.time}")
        with open("dat.log","a") as logfile:
            logfile.write(f"\n{event.time}:Key {event.name} pressed (Code:{event.scan_code})")
        with open("dat.csv","a") as logfile:
            datfile.write(f"\n{event.time},{event.name}, {event.scan_code}")
    keyboard.on_press(on_press)
    keyboard.wait()

if __name__=="__main__":
    log_keyboard_events()