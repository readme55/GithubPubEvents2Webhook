import requests
import simplejson as json
from jsondiff import diff
import sys
import time
import datetime

# src
eventUrl = "https://api.github.com/users/dashevo/events/public"
# dest
webhook_url = "xxx"
data_cur = ''
firstRun = True    # set True to skip existing data

while True:
    response = requests.get(eventUrl)

    data_old = data_cur
    data_cur = json.loads(response.content)
    data_diff = diff(data_old, data_cur)

    # if list is empty
    if not data_diff:
        # print "sleep"
        time.sleep(61)  # only 60/hour api calls on github-events allowed
        continue

    for item in data_diff[::-1]:    # start with last element
        msg = ''
        msg += ('__**Type:**__            __' +
                item['type'] + '__' + '\\n')
        msg += ('**Actor:**           ' +
                item['actor']['login'] + '\\n').encode('ascii', 'ignore').decode('ascii')
        msg += ('**Repo:**            ' + item['repo']['name'] + '\\n')

        if 'ref' in item['payload']:
            msg += ('**Ref:**                ' +
                    item['payload']['ref'] + '\\n')

        # Filter for PushEvents
        if 'head' in item['payload']:
            msg += '**Link:**        ' + 'https://github.com/' + \
                item['repo']['name'] + '/commit/' + \
                item['payload']['head'] + '\\n'

        if 'commits' in item['payload']:
            # msg += (item['payload']['commits'][0]['author']['name']).decode('ascii')
            msg += ('**Message:**     ' + item['payload']['commits'][0]
                    ['message'] + '\\n').encode('ascii', 'ignore').decode('ascii')

        if 'action' in item['payload']:
            msg += ('**Action:**         ' +
                    item['payload']['action'] + '\\n')
        if 'comment' in item['payload']:
            msg += ('**Body:**            ' + item['payload']['comment']
                    ['body'] + '\\n').encode('ascii', 'ignore').decode('ascii')
            # if 'original_commit_id' in item['payload']['comment']:

        msg += '**Created at:**  ' + item['created_at'] + '\\n'
        # msg += '==================================' + '\\n'
        # print msg

        if firstRun == False:
            myjson = '{"username": "GitHub-dashevo", "content": "' + msg + '"}'
            response = requests.post(
                webhook_url, myjson,
                headers={'Content-Type': 'application/json'}
            )
        print datetime.datetime.now()
        print response
        # exit()

    firstRun = False
