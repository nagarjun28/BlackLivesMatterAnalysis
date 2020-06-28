import tweepy
import xlwt
from xlwt import Workbook
from collections import Counter
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
credentials = {}
with open('credentials.txt') as f:
    for line in f:
        (key,val) = line.split( )
        credentials[key] = val

auth = tweepy.OAuthHandler(credentials['key'],credentials['secret'])
auth.set_access_token(credentials['access_token'],credentials['access_secret'])
api = tweepy.API(auth)
places = api.geo_search(query='USA',granularity='country')
place_id = places[0].id
tweets = []
location = []
wb = Workbook()
sheet1 = wb.add_sheet('Data2')
iter = 1
sheet1.write(0,0,'LOCATION')
sheet1.write(0,1,'TWEET TEXT')
for tweet in tweepy.Cursor(api.search, q='#blacklivesmatter place:'+place_id, rpp=100, lang='en').items(100000):
    location.append(tweet.place.full_name)
    tweets.append(tweet.text)
    sheet1.write(iter,0,tweet.place.full_name)
    sheet1.write(iter,1,tweet.text)
    iter+=1
    pass
wb.save('TwitterData1.xls')
a = Counter(location)

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))


def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:.1f}%".format(pct)


cmap = plt.get_cmap("tab20c")
wedges, texts, autotexts = ax.pie(a.values(), autopct=lambda pct: func(pct, list(a.values())),
                                  textprops=dict(color="w"), colors=cmap(np.arange(20)))

ax.legend(wedges, list(a.keys()),
          title="Locations",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Tweets location across USA for #blacklivesmatter")

plt.show()