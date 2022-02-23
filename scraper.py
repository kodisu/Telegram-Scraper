from telethon import TelegramClient, events, sync
##DELETE anon file and anon session if not working or scraping a new chat

# import json
# import re
import requests

import os
os.environ["DISCORD_WEBHOOK"] = "your webhook"
os.environ["api_hash"] = ""
os.environ["app_id"] = ""
os.environ["channelName"] = "Your Telegram community chat"

from discord import Webhook, RequestsWebhookAdapter, File
webhook_url = os.environ['DISCORD_WEBHOOK']
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

api_id = os.environ['app_id']
api_hash = os.environ['api_hash']
client = TelegramClient('anon', api_id, api_hash)

import mysql.connector
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)
mycursor = mydb.cursor()

def insert(sql, val):
  mycursor.execute(sql, val)
  mydb.commit()
  print("new Insert:", mycursor.lastrowid)

def select(sql, val):
  myresult = None
  try: 
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
  except mysql.connector.errors.ProgrammingError:
    print("error in sql select")
  return myresult

def extract_int_from_string(new_string):
  emp_str = ""
  for m in new_string:
    if m.isdigit():
        emp_str = emp_str + m
  return int(emp_str)

def extract_int(the_string):
  # get reply message id 
  words = the_string.split()
  return extract_int_from_string(words[0])

@client.on(events.NewMessage(chats=os.environ['channelName']))
async def my_event_handler(event):
  global last_sender
  global last_sender_username
  global last_avatar
  # try:
  # save message id to db (for replies)
  # db[event.id]=event.raw_text
  # print("message_id: ", event.id, "\nfrom: ", event.from_id, "\nmessage: ", event.raw_text)
  print(event.raw_text)
  # maybe needs async await?
  sql = "INSERT INTO messages (eventid, rawtext) VALUES (%s, %s) ON DUPLICATE KEY UPDATE rawtext = VALUES(rawtext);"
  val = (int(event.id), str(event.raw_text))
  insert(sql, val)

  if event.from_id != last_sender:
      last_sender = event.from_id
      sql = "SELECT * FROM members WHERE id = %s"
      val = (str(event.from_id),)
      db_result = select(sql, val)
      if db_result is not None and str(event.from_id) == db_result[0]:
      # if str(event.from_id) in db.keys():
        # webhook.send("**"+db_result[1]+":**", username=last_sender_username)
        last_sender_username = db_result[1]
        try:
          sql = "SELECT * FROM pfps WHERE id = %s"
          val = (str(event.from_id),)
          last_avatar = select(sql, val)[1]
        except: 
          last_avatar = ""
      else:
        # webhook.send("**"+str(event.from_id)+":**", username=last_sender_username)
        last_sender_username = str(event.from_id)
        last_avatar = ""
  
  #try except if original message (that is being replied to) isnt found
  try:
    # if message is a reply
    if event.reply_to is not None:
      # find messsage in db
      message_id = extract_int(str(event.reply_to))
      sql = "SELECT * FROM messages WHERE id = %s"
      val = (message_id,)
      message = select(sql, val)
      print("reply:", message[1])

      # print reply message with > and italitics
      webhook.send("> "+str(message[1]), username=last_sender_username, avatar_url=last_avatar)
  except TypeError:
    print("no original reply message stored")
  except:
    print("Other error in try/except in replies")



  # print out the reply
  webhook.send(str(event.raw_text), username=last_sender_username, avatar_url=last_avatar)


with client:
  client.run_until_disconnected()

