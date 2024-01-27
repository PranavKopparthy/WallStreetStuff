import praw
import pandas as pd
import re
import json

user_agent = "wallstreet by /u/Idunno171"
reddit_authorized = praw.Reddit(client_id="xVFsZXp0M6JlSLDUXq1epQ",
                                    client_secret="NXpYN4U28kM1_N5l8LP95gR1tysr-A",
                                    user_agent=user_agent,
                                    username="Idunno171",
                                    password="Bubbles123!")

name_subreddit = "wallstreetbets"
subreddit = reddit_authorized.subreddit(name_subreddit)

def posts_day():
    
    posts = subreddit.top("day")

    posts_dict = {}
    
    ticker_pattern = r'\$([A-Z]+)'  # Regular expression pattern to match tickers

    for post in posts:
        # Combine title, description, and the first 10 comments as text
        top_comments = [comment.body for comment in post.comments.list() if isinstance(comment, praw.models.Comment)][:15]
        text = f"{post.title} {' '.join(top_comments)}"

        # Extract tickers from the text
        title_tickers = re.findall(ticker_pattern, text)

        # Append data to the dictionary
        for ticker in title_tickers:
            if ticker in posts_dict:
                posts_dict[ticker].append(text)
            else:
                posts_dict[ticker] = [text]

    return json.dumps(posts_dict, indent=2)

def ticker_freq():
    posts = subreddit.top("day")

    posts_dict = {}
    
    ticker_pattern = r'\$([A-Z]+)'  # Regular expression pattern to match tickers

    for post in posts:
        # Combine title, description, and the first 10 comments as text
        top_comments = [comment.body for comment in post.comments.list() if isinstance(comment, praw.models.Comment)][:15]
        text = f"{post.title} {' '.join(top_comments)}"

        # Extract tickers from the text
        title_tickers = re.findall(ticker_pattern, text)

        # Append data to the dictionary
        for ticker in title_tickers:
            if ticker in posts_dict:
                posts_dict[ticker] += 1
            else:
                posts_dict[ticker] = 1

     # Create lists of tickers and frequencies
    tickers = list(posts_dict.keys())
    frequencies = list(posts_dict.values())

    # Create a dictionary with the lists
    result = {"tickers": tickers, "frequencies": frequencies}
    return json.dumps(result, indent=2)