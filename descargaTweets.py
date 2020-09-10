#Libraries
import os
import tweepy as tw
import pandas as pd

#API KEYS (Don't Share with anyone)
consumer_key= 'f6u2qHFTUmJdP6R8p7cpdC74z'
consumer_secret= 'UTW82wztu0NOwg3wl6wTA04CR3V4DseNPSBWjb6OsJRFfGxkb6'
access_token= '574202891-dAiMTfGqTlNCiKHNTPbDJqQ7gwBbQfc0tEUBz7VW'
access_token_secret= 'bKhB1HVNMO7pJ3X4CdBML9Xbz1nU2lwH04nGbf8Fy8KhM'

#Terms and date that will work as a Filter
search_words = ['#UAA']
date_since = '2018-11-16'

#Function that made the connection with Twitter API
def connection():
  auth = tw.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  return tw.API(auth, wait_on_rate_limit=True)

def main():
  api = connection()
  if not api.verify_credentials():
    print('Error in the connection')
    return False
  print('Sistem connected with Twitter API')

  # Collect the tweets
  tweets = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_since).items(1)

  csvRow = 'Autor;Texto;Fecha\n'

  # Iterate and print tweets
  for tweet in tweets:
    print(tweet.text)
    csvRow+= f'{str(tweet.user.name)};{str(tweet.text)};{str(tweet.created_at)}\n'
  archivo = open('tweets.csv', "w")
  archivo.writelines(csvRow)
  archivo.close()

main()