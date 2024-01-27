from openai import OpenAI
from config import openai_api_key

client = OpenAI(openai_api_key)

import re

def get_sentiment(ticker, text):
    # Convert text to a string if it's a list
    if isinstance(text, list):
        text = ' '.join(text)

    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "What is the sentiment of " + ticker + " " + text + "?. Return a number rating from -100 to 100"}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            # Extract the numerical sentiment rating from the content
            match = re.search(r'-?\d+', content)
            if match:
                return int(match.group())
    return get_sentiment(ticker, text) 
