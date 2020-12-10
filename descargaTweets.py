#Libraries
import os
import tweepy as tw
import re
import nltk
import cleantext

import csv

#nltk.download('stopwords')

#API KEYS (Don't Share with anyone)
consumer_key= 'f6u2qHFTUmJdP6R8p7cpdC74z'
consumer_secret= 'UTW82wztu0NOwg3wl6wTA04CR3V4DseNPSBWjb6OsJRFfGxkb6'
access_token= '574202891-dAiMTfGqTlNCiKHNTPbDJqQ7gwBbQfc0tEUBz7VW'
access_token_secret= 'bKhB1HVNMO7pJ3X4CdBML9Xbz1nU2lwH04nGbf8Fy8KhM'


#Function that made the connection with Twitter API
def connection():
  auth = tw.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  return tw.API(auth, wait_on_rate_limit=True)

def main():
  #Terms and date that will work as a Filter
  # search_words = ['abusar','acoso','agresor','aislamiento','alarma','aprovecharse','depresión','desconfianza']
  search_words = ['bully']
  date_since = '2018-11-16'
  amount_of_results = 5

  option = int(input('Deseas introducir los palabras que se van a usar como criterior de búsqueda? 1-Si 0-No (Defecto palabras ...): '))
  if option:
    search_words = str(input('Introduce las palabras a búscar, en lugar de espacio como separador usa la \',\': ')).split(',')

  option = int(input('Deseas introducir la cantidad de tweets que deseas 1-Si 0-No (Defecto 5 tweets): '))
  if option:
    amount_of_results = int(input('Cuantos registros va a querer: '))
  
  option = int(input(f'Deseas introducir la fecha de inicio para la búsqueda 1-Si 0-No (Defecto 2018-11-16): '))
  if option:
    date_since = input('Introduce la fecha de inicio en la que se va a hacer la búsqueda de tweets (Formato yyyy-mm-dd): ')

  print('\n\nInicializando conexión con Twitter API')
  api = connection()
  if not api.verify_credentials():
    print('Error en la conexión')
    return False
  print('Aplicación conectada con Twitter API')

  # Collect the tweets
  tweets = tw.Cursor(api.search,
                q=search_words,
                lang="en",
                since=date_since
            ).items(amount_of_results)

  # fileExist = os.path.exists('tweets.csv')

  # csvRow = ''
  # csvRaw = ''

  # if not fileExist:
  #   csvRow = 'id;created_at;text;retweet_count;favorite_count\n'

  with open('tweets.csv', "+a", newline='',encoding='utf-8') as tweetsFile:
    tweet_writer = csv.writer(tweetsFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    tweet_writer.writerow(['id','created_at','text','retweet_count','favorite_count'])
    # Iterate and print tweets
    for index, tweet in enumerate(tweets):
      #Assing to the variable tweet the object json that tweet has so we can use it as a dictonary 
      tweet = tweet._json
      tweet_writer.writerow([tweet["id"],tweet["created_at"],tweet["text"],tweet["retweet_count"],tweet["favorite_count"]])

  # if fileExist:
  #   archivo = 
  #   archivo.writelines(csvRow)
  #   archivo.close()
  # else:
  #   archivo = open('tweets.csv', "w", encoding='utf-8')
  #   archivo.writelines(csvRow)
  #   archivo.close()

#Function that cleans the string it deletes special characters and contractions
def cleaner(text):
  text = delSomeCharacters(text)
  text = delEmojis(text)
  return text

#Function that deletes the emojis from the string 
def delEmojis(text):
  regrex_pattern = re.compile(pattern="["
                              u"\U0001F600-\U0001F64F"  # emoticons
                              u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                              u"\U0001F680-\U0001F6FF"  # transport & map symbols
                              u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                              "]+", flags=re.UNICODE)
  return regrex_pattern.sub(r'', text)

def delSomeCharacters(text):
  text = cleantext.clean(text, all= True)
  # text = text.lower()
  #Replacing all de url that could have the tweet
  # text = text.replace(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '')
  #Remove all characters that are not letters from the string
  # text = ''.join([i for i in text if not i.isdigit()])
  # text = text.replace(';','')
  # text = text.replace('.','')
  # text = text.replace(',','')
  # text = text.replace('#', '')
  # text = re.sub(r'\W+', ' ', text)
  return text

main()
