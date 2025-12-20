import time
import sqlite3
import pywinctl
from pynput import keyboard, mouse
import schedule
from database import initialising_db

#global controllers:
key_press_count = 0
mouse_click_count = 0
last_active = time.time()

#active window detection
def get_active_window():
    try:
        window = pywinctl.getActiveWindow()
        return window.title if window else "unknown"
    except:
        return "unknown"
    
    #keyboard listener
def key_listener(key):
    global key_press_count, last_active
    key_press_count += 1
    last_active = time.time()


#mouse listener:
def mouse_listener(x,y, button, presses):
    global mouse_click_count, last_active
    mouse_click_count += 1
    last_active = time.time()


key_listener = keyboard.Listener(on_press=key_listener)
key_listener.start()

mouse_listener = mouse.Listener(on_click=mouse_listener)
mouse_listener.start()


#idle check:
def is_idle(idle_time=300):
    return (time.time() - last_active) > idle_time

#logging in to the database:

def log_act():
    global key_press_count, mouse_click_count

    app = get_active_window()
    now = int(time.time())

    conn = sqlite3.connect("app_database.db")
    cursor = conn.cursor()

    if is_idle():
        key_press_count = 0
        mouse_click_count = 0
        event_type = "idle"
        duration = 10
        return
    
    else:
        event_type = "usage"
        duration = 10


    cursor.execute("""
    INSERT INTO users (timestamp, event_tpes, app_name, duration, key_count, mouse_count, extra)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (now, event_type, app, duration, key_press_count, mouse_click_count, "none"))

    conn.commit()
    conn.close()    

    print(f"logged {event_type} | App: {app} | key press count : {key_press_count} | mouse click count : {mouse_click_count}")

    key_press_count = 0
    mouse_click_count = 0

#main loop:
def main():
    initialising_db()
    schedule.every(10).seconds.do(log_act)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
