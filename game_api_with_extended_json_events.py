#!/usr/bin/env python
#Import json, kafka and flask
import json
from kafka import KafkaProducer
from flask import Flask, request

#Define the app
app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')

#Define kafka function to receive topic and event.  Added the request line to receive additional fields in the headers.
def log_to_kafka(topic, event):
    event.update(request.headers)
    producer.send(topic, json.dumps(event).encode())
    
@app.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None
    return '''<h1>The language value is: {}</h1>'''.format(language)

#Setting up the default address.  The default response returns a string.
# Define default_event.  Passes to the log_to_kafka function 'events' as the default event.
@app.route("/")
def default_response():
    default_event = {'event_type': 'default'}
    log_to_kafka('events', default_event)
    return "This is the default response!\n"

#Post purchase_a_sword, calls the purchase_sword function, returns the string.
@app.route("/purchase_a_sword")
def purchase_a_sword():
    purchase_sword_event = {'event_type': 'purchase_sword'}
    log_to_kafka('events', purchase_sword_event)
    return "Sword Purchased!\n"

#Post purchase_a_frog, calls the purchase_frog function, returns the string.
@app.route("/purchase_a_frog")
def purchase_a_frog():
    purchase_frog_event = {'event_type': 'purchase_frog'}
    log_to_kafka('events', purchase_frog_event)
    return "Frog Purchased!\n"

