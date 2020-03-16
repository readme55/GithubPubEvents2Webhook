import requests
import simplejson as json
from jsondiff import diff
import sys
import time
import datetime

# src
eventUrl = "https://api.github.com/users/dashevo/events/public"
# dest  (non-public so i put it in file and .gitignore)
f=open("./webhook.txt", "r")
if f.mode == 'r':
    webhook_url = f.read()

data_cur = ''
firstRun = True  # set True to skip existing data

while True:
    try:
        response = requests.get(eventUrl)
        print 'Github Public Events response: ' + response
        data_old = data_cur
        data_cur = json.loads(response.content)
        data_diff = diff(data_old, data_cur)

        # if list is empty
        if not data_diff:
            time.sleep(61)  # only 60/hour api calls on github-events allowed
            continue

        for item in data_diff[::-1]:  # start with last element
            msg = ''
            msg += ('__**Type:**__            __' + item['type'] + '__' +
                    '\\n')

            msg += ('**Repo:**            ' + item['repo']['name'] + '\\n')

            if 'ref' in item['payload']:
                msg += ('**Ref:**                ' + item['payload']['ref'] +
                        '\\n')

            msg += ('**Actor:**           ' + item['actor']['login'] +
                    '\\n').encode('ascii', 'ignore').decode('ascii')

            ## PushEvent (recognize from 'payload' objects)
            # if 'head' in item['payload']:
            #     msg += '**Link:**        ' + 'https://github.com/' + \
            #         item['repo']['name'] + '/commit/' + \
            #         item['payload']['head'] + '\\n'

            # (Multiple) Commit messages (Author Name + Message + HTML Link)
            if 'commits' in item['payload']:
                msg += '**Commits:**' + '\\n'
                for commit in item['payload']['commits']:
                    msg += ('**__Author__:**     ' +
                            commit['author']['name']).decode('ascii')
                    msg += ('**Message:**     ' + commit['message'] +
                            '\\n').encode('ascii', 'ignore').decode('ascii')
                    msg += ('**Link:**     ' + 'https://github.com/' +
                            item['repo']['name'] + '/commit/' + commit['sha'] +
                            '\\n')

                    # msg += ('**Author:**     ' + item['payload']['commits'][0]['author']['name']
                    #         ).decode('ascii')
                    # msg += ('**Message:**     ' +
                    #         item['payload']['commits'][0]['message'] + '\\n').encode(
                    #             'ascii', 'ignore').decode('ascii')

            ## PullRequestEvent, ReleaseEvent, IssueCommentEvent
            if 'action' in item['payload']:
                msg += ('**Action:**         ' + item['payload']['action'] +
                        '\\n')

            if 'pull_request' in item['payload']:
                msg += ('**Link:**       ' +
                        item['payload']['pull_request']['html_url'] + '\\n')
                msg += ('**Title:**       ' +
                        item['payload']['pull_request']['title'] +
                        '\\n').encode('ascii', 'ignore').decode('ascii')
                msg += ('**Body:**       ' +
                        item['payload']['pull_request']['body'] +
                        '\\n').encode('ascii', 'ignore').decode('ascii')

            if 'release' in item['payload']:
                msg += ('**Link:**       ' +
                        item['payload']['release']['html_url'] + '\\n')
                msg += ('**Name:**       ' +
                        item['payload']['release']['name'] + '\\n').encode(
                            'ascii', 'ignore').decode('ascii')
                msg += ('**Body:**       ' +
                        item['payload']['release']['body'] + '\\n').encode(
                            'ascii', 'ignore').decode('ascii')

            if 'issue' in item['payload']:
                msg += ('**Link:**       ' +
                        item['payload']['issue']['html_url'] + '\\n')
                msg += ('**Title:**       ' +
                        item['payload']['issue']['title'] + '\\n').encode(
                            'ascii', 'ignore').decode('ascii')
                msg += ('**Body:**       ' + item['payload']['issue']['body'] +
                        '\\n').encode('ascii', 'ignore').decode('ascii')

            ## PullRequestReviewCommentEvent
            if 'comment' in item['payload']:
                msg += ('**Body:**            ' +
                        item['payload']['comment']['body'] + '\\n').encode(
                            'ascii', 'ignore').decode('ascii')
                msg += ('**Link:**            ' +
                        item['payload']['comment']['html_url'] + '\\n')

            msg += '**Created at:**  ' + item['created_at'] + '\\n'

            ## Debug local
            # print msg

            if firstRun == False:
                myjson = '{"username": "GitHub-dashevo", "content": "' + msg + '"}'
                response = requests.post(
                    webhook_url,
                    myjson,
                    headers={'Content-Type': 'application/json'})
            print datetime.datetime.now()
            print 'Discord Webhook response: ' + response

        firstRun = False

    except TypeError:
        print("TypeError: prob API limit exceed! Sleeping 61 min")
        time.sleep(3660)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Goodbye")
        exit()