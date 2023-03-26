import time
import random
import requests
import numpy as np
import pandas as pd

#VARS
zone1 = np.arange(0.91185, 0.91258, 0.00001)
zone2 = np.arange(0.91759, 0.91859, 0.00001)
zone3 = np.arange(20,30)
zone4 = np.arange(30,40)
tolerance = 0.00001
url = ("YOUR DISCORD WEBHOOK HERE")
title = ("Price Alert")

#OANDA API
key = "YOUR OANDA API KEY"
id = "YOUR OANDA ACCOUNT ID"
PRICING_PATH = f"/v3/accounts/{id}/pricing"
API = "api-fxpractice.oanda.com"
STREAM_API = "stream-fxpractice.oanda.com/"
headers = {"Authorization": "Bearer "+ key}


#SEND TO DISCORD WEBHOOK
def send(desc):
        global title
        data = {
            "content" : "",
        }
        data["embeds"] = [
            {
                "description" : desc,
                "title" : title
            }
        ]

        result = requests.post(url, json = data)
        print("done")
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            pass


def get_bid_price(instrument):
    global currentPrice
    query = {"instruments": instrument} 
    response = requests.get("https://"+API+PRICING_PATH, headers=headers, params=query)
    json_response = response.json()

    prices = json_response["prices"][0]["bids"][0]["price"]
    prices = float(prices)

    time_str = json_response["time"]
    time = pd.to_datetime(time_str)
    currentPrice = prices
    print(currentPrice)
    #send(str(currentPrice))
    #check for price in zones the trigger send
    if any(abs(x - currentPrice) < tolerance for x in zone1):
        desc = ("Price In Zone 1")
        send(desc)

    elif any(abs(x - currentPrice) < tolerance for x in zone2):
        desc = ("Price In Zone 2")
        send(desc)

    elif any(abs(x - currentPrice) < tolerance for x in zone3):
        desc = ("Price In Zone 3")
        send(desc)

    elif any(abs(x - currentPrice) < tolerance for x in zone4):
        
        desc = ("Price In Zone 4")
        send(desc)

while True:
    get_bid_price("AUD_CAD") #you can use any forex pair