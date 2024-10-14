import requests

def run(event, context):
    return requests.get('https://www.google.com').text