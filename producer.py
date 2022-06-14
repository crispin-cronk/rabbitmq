#!/usr/bin/env python
import pika
import requests
import json

def getJokes(url):
  response = requests.get(url=url)
  return response.json()

def sendJokes(jokes):
  connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = connection.channel()
  channel.queue_declare(queue='jokes')
  for joke in jokes:
    channel.basic_publish(exchange='',
                          routing_key='jokes',
                          body=json.dumps(joke))
  connection.close()
  

print('fetching jokes')
jokes = getJokes('https://raw.githubusercontent.com/taivop/joke-dataset/master/reddit_jokes.json')

print('sending jokes')
sendJokes(jokes)
