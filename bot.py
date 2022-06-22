#!/usr/bin/python

import sqlite3
import requests
import json

varfile = open('vars.json', 'r')
var = json.load(varfile)

con = sqlite3.connect('test.db')
cur = con.cursor()
print("Opened database successfully")

def create_new_database():
    cur.execute(f"CREATE TABLE users (user, opt_in, {var['available_newsletters_str']})")
    
def user_check(user):
    print(user)
    userCheck = cur.execute(f"SELECT COUNT(*) FROM users WHERE user = {user}")
    if userCheck != 0:
        return True
    else:
        return False

def user(usr, action):
    if(action == "subscribe"):
        cur.execute(f'''INSERT INTO users (user, opt_in, {var['available_newsletters_str']}) VALUES ("{usr}", True, False, False)''')
        con.commit()
    elif(action == "unsubscribe"):
        cur.execute(f'''DELETE FROM users WHERE user="{usr}"''')
        con.commit()
    else:
        print("Invalid Statement(s) @ def user")

def change_subscriptions(usr, action, sub):
    if(action == "subscribe"):
        cur.execute(f'''UPDATE users SET {sub}=True WHERE user="{usr}"''')
        con.commit()
    elif(action == "unsubscribe"):
        cur.execute(f'''UPDATE users SET {sub}=False WHERE user="{usr}"''')
        con.commit()
    else:
        print("Invalid Statement(s) @ def change_subscriptions")

def send_message(type, text):
    cur.execute(f'''SELECT user FROM users WHERE {type}=True''')
    rows = cur.fetchall()
    for row in rows:
        print(row)
        r = requests.post(f"{var['signal_api_url']}/v2/send", json = {
            "number":var['source_number'],
            "recipients":row,
            "message":text
        })
        print(r.json())

def send_single_message(usr, text):
    r = requests.post(f"{var['signal_api_url']}/v2/send", json = {
        "number":var['source_number'],
        "recipients":[usr],
        "message":text
    })
    print(r.json())

def send_help_message(usr):
    r = requests.post(f"{var['signal_api_url']}/v2/send", json = {
        "number": var['source_number'],
        "recipients":[usr],
        "message":var['help_message'] 
    })
    print(r.json())


def check_messages():
    data = requests.get(f"{var['signal_api_url']}/v1/receive/{var['source_number']}").json()
    for d in data:
        try:
            message = d['envelope']['dataMessage']['message']
            source_user = d['envelope']['source']
            if "start" in message.lower():
                user(source_user, "subscribe")
                send_single_message(source_user, var['welcome_message'])
            if "stop" in message.lower():
                user(source_user, "unsubscribe")
                send_single_message(source_user, var['user_unsubscribed'])
            available_newsletters = var['available_newsletters'] 
            mentioned_newsletter = message.lower().split(" ")[1]
            if "subscribe" in message.lower():
                if mentioned_newsletter.lower() in available_newsletters:
                    change_subscriptions(source_user, "subscribe", mentioned_newsletter.lower())
                    send_single_message(source_user, f"{var['newsletter_subscribed']}{mentioned_newsletter}")
                else:
                    send_single_message(source_user,  f"{var['newsletter_not_found']}")                
            if "unsubscribe" in message.lower():
                if mentioned_newsletter.lower() in available_newsletters:
                    change_subscriptions(source_user, "unsubscribe", mentioned_newsletter.lower())
                    send_single_message(source_user, f"{var['newsletter_unsubscribed']}{mentioned_newsletter}")
                else:
                    send_single_message(source_user, f"{var['newsletter_not_found']}")
            if "help" in message.lower():
                send_help_message(source_user)
        except:
            return

def run():
    while True:
        check_messages()

run()    