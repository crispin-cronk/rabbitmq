#!/usr/bin/env python
import pika
import json
import argparse

def shouldPrintJoke(joke, args):
    if args.score != None and (args.score >= joke['score']) or \
       args.filter and any(word not in (joke['title'] + joke['body']) for word in args.filter):
        return False
    return True

parser = argparse.ArgumentParser(prog='consumer')
parser.add_argument('-s', '--score', nargs='?', type=int)
parser.add_argument('-f', '--filter', nargs='*')
args = parser.parse_args()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='jokes')

def callback(ch, method, properties, body):
    joke = json.loads(body)
    if(shouldPrintJoke(joke, args)):
        print(joke)

channel.basic_consume(queue='jokes', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
