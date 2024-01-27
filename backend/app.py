from flask import Flask, request, jsonify
import json
from webscraper import posts_day, ticker_freq
from sentiment import get_sentiment

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/get_tickers', methods=['GET'])
def get_freq():
    return ticker_freq()

@app.route('/get_sentiments', methods=['GET'])
def get_sentiments():
    ticker_texts = posts_day()
    
    # Convert the string to a dictionary if necessary
    if isinstance(ticker_texts, str):
        ticker_texts = json.loads(ticker_texts)

    sentiment_ratings = {}

    for ticker, text in ticker_texts.items():
        sentiment_ratings[ticker] = get_sentiment(ticker, text)

    tickers = list(sentiment_ratings.keys())
    sentiments = list(sentiment_ratings.values())

    result = {"tickers": tickers, "sentiments": sentiments}
    return result

@app.route('/get_rankings', methods=['GET'])
def get_rankings():
    freq = ticker_freq()
    sentiments = get_sentiments()

    # Convert the returned objects to JSON strings if necessary
    if not isinstance(freq, (str, bytes, bytearray)):
        freq = json.dumps(freq)
    if not isinstance(sentiments, (str, bytes, bytearray)):
        sentiments = json.dumps(sentiments)

    freq = json.loads(freq)
    sentiments = json.loads(sentiments)

    for ticker, frequencies in freq.items():
        print(ticker, frequencies)

    for ticker, sentiment in sentiments.items():
        print(ticker, sentiment)

    # Create a dictionary to store the rankings
    rankings = {}
    for ticker in freq['tickers']:
        if ticker in sentiments['tickers']:
            freq_index = freq['tickers'].index(ticker)
            sentiment_index = sentiments['tickers'].index(ticker)
            rankings[ticker] = freq['frequencies'][freq_index] * sentiments['sentiments'][sentiment_index]

    # Sort the rankings dictionary by value in descending order and get the keys
    sorted_rankings = sorted(rankings.items(), key=lambda item: item[1], reverse=True)

    # Convert the sorted rankings to a dictionary
    sorted_rankings_dict = dict(sorted_rankings)

    result = {"tickers": list(sorted_rankings_dict.keys()), "indices": list(sorted_rankings_dict.values())}
    return json.dumps(result, indent=2)


if __name__ == '__main__':
    app.run(debug=True, port=5050)