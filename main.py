import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_ACCOUNT_SID = "AC4c838c0db6e65432e470c36066f731d9"
TWILIO_AUTH_TOKEN = "b23a966dd06abf318f09700aec0ed563"

STOCK_API_KEY = "DSG8JU273X174UA2"
NEWS_API_KEY = "a159945dbd0d4cbf8bde417b8dd87a01"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params={"function":"TIME_SERIES_DAILY",
                "symbol":STOCK_NAME,
                "apikey":STOCK_API_KEY}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data["4. close"]
print(yesterday_closing_price)

day_before_yesterday_data=data_list[1]
day_before_yesterday_closing_price=day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference=float(yesterday_closing_price)-float(day_before_yesterday_closing_price)
up_down=None
if difference>0:
    up_down="🔺"
else:
    up_down="🔻"

diff_percent=(difference/float(yesterday_closing_price))*100
print(diff_percent)

if  abs(diff_percent) > 1:
    news_params = {"apiKey":NEWS_API_KEY,
                   "qInTitle":COMPANY_NAME}
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles=news_response.json()["articles"]

    three_articles=articles[:3]
    print(three_articles)

    fmt_articles=[
        f"{STOCK_NAME}:{up_down}{diff_percent}%/nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in fmt_articles:
        message = client.messages.create(
            body=article,from_="+18782848601",to="phone-number")