import sqlite3
import time
import datetime
import threading
#import call

con = sqlite3.connect("duty.sqlite", check_same_thread = False)
cur = con.cursor()
lock = threading.Lock()
users = cur.execute("select * from users").fetchall()

print users

def next_user(incident_key):
    lock.acquire()
    index = cur.execute("select status from events where incident_key = ?", (incident_key,)).fetchone()[0]
    cur.execute("update events set status = status + 1 where incident_key = ?", (incident_key,))
    con.commit()
    lock.release()
    return (index, users[index % len(users)])

def resolved(incident_key):
    lock.acquire()
    events = cur.execute("select * from events where status >= 0 and incident_key = ?", (incident_key,)).fetchall()
    lock.release()
    if(len(events) == 0):
        return True
    else:
        return False

def caller(incident_key):
    while True:
        if resolved(incident_key):
            print("[{0}] Resolved".format(incident_key))
            return
        else:
            (index, user) = next_user(incident_key)
            
            print("[{0}] [call {1}] calling {2}".format(incident_key, index, user[0]))
            time.sleep(2)

while True:
    lock.acquire()
    events = cur.execute("select * from events where status = 0").fetchall()
    lock.release()

    for event in events:
        print("New event: {0}".format(event))
        t = threading.Thread(target=caller, args=(event[1],))
        t.start()

    time.sleep(2)
