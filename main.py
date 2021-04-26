"""Little script encouraging you to use the the right mod for the right key;
it deletes badly pressed modifier shortcuts and shift text"""
from pynput import keyboard

kbd = keyboard.Controller()


def on_press(key):
    print(f"\n{key}",file="log.txt")


if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press) as l:
        l.join()
