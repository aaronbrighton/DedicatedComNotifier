import json
import requests
import boto3
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    
    url = "https://dedicated.com/includes/dedicated-servers-list-instant.php"
    headers = {
        'user-agent': 'my-app/0.0.1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://dedicated.com/dedicated-servers',
        'TE': 'Trailers'
    }

    response = requests.post(url, data = {'ajax': 'ajax'}, headers = headers)
    
    soup = BeautifulSoup(response.text, features="html.parser")
    trackingDict = {}
    for div in soup.find_all('div'):
        if div.get('class') != None and 'single' in div.get('class'):
            for div2 in div.find_all('div'):
                if div2.get('class')!= None and 'card-top' in div2.get('class'):
                    for h5 in div2.find_all('h5'):
                        for img in h5.find_all('img'):
                            config = img.get('alt')
                            trackingDict[config] = {};

                if div2.get('class')!= None and 'card-middle' in div2.get('class'):
                    for div3 in div2.find_all('div'):
                        if div3.get('class') != None and 'instant-availability' in div3.get('class'):
                            for ul in div3.find_all('ul'):
                                for li in ul.find_all('li'):
                                    local = li.get('data-location');
                                    trackingDict[config][local] = {};
                                    for p in li.find_all('p'):
                                        availability = p.text;
                                        trackingDict[config][local] = availability;
                                        
    if trackingDict[event['config']][event['local']] != 'Out':
        client = boto3.client('sns')
        client.publish(
            PhoneNumber=event['phone'],
            Message=event['config']+" is available in "+event['local']+" with quantity of "+trackingDict[event['config']][event['local']]
        )

    
    # TODO implement
    return {
        'availability': trackingDict[event['config']][event['local']]
    }
