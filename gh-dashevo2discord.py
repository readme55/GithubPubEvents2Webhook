import requests
import simplejson as json
from jsondiff import diff
import sys
import time

eventUrl = "https://api.github.com/users/dashevo/events/public"
webhook_url = "xxx"
data_cur = ''
firstRun = False    # set True to skip existing data

while True:
    response = requests.get(eventUrl)

    data_old = data_cur
    data_cur = json.loads(response.content)
    data_diff = diff(data_old, data_cur)

    # if list is empty    
    # if not data_diff:

    #if list is not empty    
    if data_diff:
        for item in data_diff[::-1]:    # start with last element
            msg = ''
            msg += ('__**Type:**__            __' + item['type'] + '__' + '\\n')
            msg += ('**Actor:**           ' + item['actor']['login'] + '\\n').encode('ascii', 'ignore').decode('ascii')
            msg += ('**Repo:**            ' + item['repo']['name'] + '\\n')

            if 'ref' in item['payload']:
                msg += ('**Ref:**                ' + item['payload']['ref'] + '\\n')
            if 'commits' in item['payload']:
                # print item['payload']['commits'][0]['author']['name']
                msg += ('**Message:**     ' + item['payload']['commits'][0]['message'] + '\\n').encode('ascii', 'ignore').decode('ascii')

            if 'action' in item['payload']:
                msg += ('**Action:**         ' + item['payload']['action'] + '\\n')
            if 'comment' in item['payload']:
                msg += ('**Body:**            ' + item['payload']['comment']['body'] + '\\n').encode('ascii', 'ignore').decode('ascii')
                # if 'original_commit_id' in item['payload']['comment']:
                    # Filter for PushEvents, else wrong data when eg PullRequestReviewCommentEvent    
                    # msg += '**Link:**        ' + 'https://github.com/' + item['repo']['name'] + '/commit/' + item['payload']['comment']['original_commit_id'] + '\\n'

            msg += '**Created at:**  ' + item['created_at'] + '\\n'
            # msg += '==================================' + '\\n'
            print msg
            
            # if firstRun == False:
            #     myjson = '{"username": "GitHub-dashevo", "content": "' + msg + '"}'
            #     response = requests.post(
            #         webhook_url, myjson,
            #         headers={'Content-Type': 'application/json'
            #         }
            #     )
                # print response
                # exit()

    firstRun = False
    print "sleep"
    time.sleep(5)
