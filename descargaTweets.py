#Libraries
import os
import tweepy as tw

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
  search_words = ['#UAA']
  date_since = '2018-11-16'
  amount_of_results = 5

  option = int(input('Deseas introducir los palabras que se van a usar como criterior de búsqueda? 1-Si 0-No (Defecto palabras ...): '))
  if option:
    search_words = str(input('Introduce las palabras a búscar, en lugar de espacio como separador usa la \',\': ')).split(',')

  option = int(input('Deseas introducir la cantidad de tweets que deseas 1-Si 0-No (Defecto 5 tweets): '))
  if option:
    amount_of_results = int(input('Cuantos registros va a querer: '))
  
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
                since=date_since).items(amount_of_results)

  csvRow = 'Autor;Texto;Fecha;Pais;Ciudad\n'

  # Iterate and print tweets
  for index, tweet in enumerate(tweets):
    #Assing to the variable tweet the object json that tweet has so we can use it as a dictonary 
    tweet = tweet._json
    print(f'Procesado tweet {index+1} de {amount_of_results}')
    country = 'None'
    city = 'None'
    #Validation that help us to know if the tweet has de information of the location
    if tweet["place"] != None:
      country = tweet["place"]["country"]
      city = tweet['place']['name']
    csvRow+= f'{tweet["user"]["name"]};{tweet["text"]};{tweet["created_at"]};{country};{city}\n'
  archivo = open('tweets.csv', "w")
  archivo.writelines(csvRow)
  archivo.close()

main()