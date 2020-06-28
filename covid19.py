import tweepy
import xlwt
from xlwt import Workbook
from collections import Counter
from matplotlib import pyplot as plt
from datetime import datetime

credentials = {}
with open('credentials.txt') as f:
    for line in f:
        (key,val) = line.split( )
        credentials[key] = val

auth = tweepy.OAuthHandler(credentials['key'],credentials['secret'])
auth.set_access_token(credentials['access_token'],credentials['access_secret'])
api = tweepy.API(auth)
places = api.geo_search(query='United Kingdom',granularity='country')
place_id = places[2].id
tweets = []
location = []
wb = Workbook()
sheet1 = wb.add_sheet('Data2')
iter = 1
sheet1.write(0,0,'LOCATION')
sheet1.write(0,1,'TWEET TEXT')
for tweet in tweepy.Cursor(api.search, q='#covid19 place:'+place_id, rpp=100, lang='en').items(100000):
    location.append(tweet.place.full_name)
    tweets.append(tweet.text)
    sheet1.write(iter,0,tweet.place.full_name)
    sheet1.write(iter,1,tweet.text)
    iter+=1
    pass
wb.save('UnitedKingdom.xls')

a = Counter(location)
wb = Workbook()
sheet1  = wb.add_sheet("DataCount")
iter1 = 1
sheet1.write(0,0,'LOCATION')
sheet1.write(0,1,'COUNT')
for key in a.keys():
    sheet1.write(iter1,0,key)
    sheet1.write(iter1,1,a[key])
    iter1 += 1
wb.save("UnitedKingdomCount.xls")

plt.pie(a.values(),labels=a.keys())
plt.title("Tweets location across Ireland for #covid19")
