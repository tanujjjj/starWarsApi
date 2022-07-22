from asyncio.windows_events import NULL
from http.client import responses
from urllib import response
import requests
import json
import pandas as pd
import numpy as np


def loadApi(results, api_link):
    while True:
        response = requests.get(api_link)
        api_results = json.loads(response.content)
        results = results+api_results['results']
        print(api_results['next'])
        if(api_results['next'] == None):
            return results
        else:
            api_link = api_results['next']


def top10Char(results):
    topTen = sorted(results, key=lambda d: len(d['films']), reverse=True)
    topTen = topTen[:10]
    return(topTen)


def sortByHeight(topTen):
    topTenByHeight = sorted(
        topTen, key=lambda d: d['height'], reverse=True)
    return topTenByHeight


def createCSV(topTen):
    for i in range(10):
        topTen[i]['films'] = len(topTen[i]['films'])
    df = pd.DataFrame(topTen)
    df = df[['name', 'species', 'height', 'films']]
    df.columns.str.replace('films', 'appearances')
    df.to_csv('starWarsTopTen.csv')
    return df


api_link = 'https://swapi.dev/api/people/'
results = []
results = loadApi(results, api_link)  # Load data

# Req 1:Sort characters by number of Films heighest first (1st proplem)
topTen = top10Char(results)
topTenChar = []
for i in topTen:
    topTenChar.append(i['name'])
print("The top Ten Characters who appear in the most Star Wars films are:", topTenChar)

# Req2:Sort (1st prblem) by height... tallest first
topTenByHeight = sortByHeight(topTen)
for i in topTen:
    topTenChar.append(i['name'])
print("The top Ten Characters who appear in the most Star Wars films in order of Height:", topTenChar)

# Req3 : Create csv
df = createCSV(topTenByHeight)

# Req4:	Send the CSV to httpbin.org
file = open("starWarsTopTen.csv", "rb")
resp = requests.post('http://httpbin.org/post',
                     data=file)
