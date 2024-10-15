import requests

def run(event, context):
    result = requests.get('https://httpbin.org/get')
    return f'{result.status_code}'
