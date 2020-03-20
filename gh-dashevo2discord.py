import requests
import simplejson as json
from jsondiff import diff
import sys
import time
import datetime

# src
eventUrl = "https://api.github.com/users/dashevo/events/public"
# eventUrl = "https://api.github.com/users/dashpay/events/public"

# dest  (non-public so i put it in file and .gitignore)
f = open("./webhook.txt", "r")
if f.mode == 'r':
    webhook_url = f.read()
f.close()
webhook_url = webhook_url.replace('\n',
                                  '')  # needed for linux, not for windows
# count commits
endTime = "23:00"
cntMasterCommit = 0
cntOtherCommit = 0
commitMasterList = []
commitOtherList = []

modifiedSince = ''
curId = 0
firstRun = True  # set True to skip existing data

while True:
    try:
        # output statistic:
        if str(datetime.datetime.now())[11:16] == endTime:
            msgStats = "**Daily Commit Summary on Master: " + str(cntMasterCommit) + "\\n"
            for item in list(dict.fromkeys(commitMasterList)):  # remove duplicates with dict
                msgStats += '   ' + item + "\\n"
            msgStats += "Daily Commit Summary on any other Branch: " + str(cntOtherCommit) + "\\n"
            for item in list(dict.fromkeys(commitOtherList)):
                msgStats += '   ' + item + "\\n"
            msgStats += "**"
            cntMasterCommit = 0
            cntOtherCommit = 0
            commitMasterList = []
            commitOtherList = []
            myjson = '{"username": "GitHub-dashevo", "content": "' + msgStats + '"}'
            response = requests.post(webhook_url, myjson, headers={'Content-Type': 'application/json'})

        # check if modified since last request (https://developer.github.com/v3/#conditional-requests)
        cur_header = {'If-Modified-Since': modifiedSince}
        response = requests.get(eventUrl, headers=cur_header)
        header = response.headers
        if modifiedSince != header['Last-Modified']:
            modifiedSince = header['Last-Modified']
        else:
            print("."),
            time.sleep(60)  # only 60/hour api calls on github-events allowed
            continue

        # fetch github public events json file
        response = requests.get(eventUrl)
        print 'Github Public Events response: ' + str(response)
        data = json.loads(response.content)

        # chasing some bug, saved local json
        # f = open("./dashevo-problem.json", "r")
        # if f.mode == 'r':
        #     data = json.loads(f.read())
        # f.close()
        ##################

        # use Id to check for updated events and skip already processed events
        processedId = curId

        for item in data[::-1]:  # start with last element (earliest date)
            time.sleep(3)  # http 429 error if too many/fast requests

            if long(processedId) >= long(
                    item['id']):  # check for new event by comparing id's
                continue
            else:
                curId = item['id']  # new event to process, save newest id

            msg = ''
            msg += ('__**Type:**__            __' + item['type'] + '__' + '\\n')

            msg += ('**Repo:**            ' + item['repo']['name'] + '\\n')

            if 'ref' in item['payload']:
                msg += ('**Ref:**                ' + item['payload']['ref'] + '\\n')

            msg += ('**Actor:**           ' + item['actor']['login'] + '\\n').encode('ascii', 'ignore').decode('ascii')

            # PushEvent (recognize from 'payload' objects)
            # item['payload']['head'] is duplicate from one of the commits below
            # (Multiple) Commit messages (Author Name + Message + HTML Link)
            if 'commits' in item['payload']:
                msg += '**Commits:**' + '\\n'
                for commit in item['payload']['commits']:
                    msg += ('**__Author__:**        ' + commit['author']['name'] + '\\n')
                    msg += ('**Message:**       ' + commit['message']) + '\\n'
                    msg += ('**Link:**          ' + '<https://github.com/' + item['repo']['name'] + '/commit/' + commit['sha'] + '>\\n')
                    # Statistics
                    # count Master commits
                    if item['payload']['ref'] == "refs/heads/master" or item['payload']['ref'] == "master":
                        cntMasterCommit += 1
                        commitMasterList.append(item['repo']['name'])
                    # count any other commits
                    else:
                        cntOtherCommit += 1
                        commitOtherList.append(item['repo']['name'] + " : " + item['payload']['ref'])

            # PullRequestReviewCommentEvent
            if 'comment' in item['payload']:
                msg += ('**Body:**            ' + item['payload']['comment']['body']) + '\\n'
                msg += ('**Link:**            ' + '<' + item['payload']['comment']['html_url'] + '>\\n')

            ## PullRequestEvent, ReleaseEvent, IssueCommentEvent
            if 'action' in item['payload']:
                msg += ('**Action:**         ' + item['payload']['action'] + '\\n')

            if 'pull_request' in item['payload']:
                msg += ('**Link:**          ' + '<' + item['payload']['pull_request']['html_url'] + '>\\n')
                msg += ('**Title:**         ' + item['payload']['pull_request']['title'] + '\\n')
                msg += ('**Body:**    ' + item['payload']['pull_request']['body']) + '\\n'

            if 'release' in item['payload']:
                msg += ('**Link:**          ' + '<' + item['payload']['release']['html_url'] + '>\\n')
                msg += ('**Name:**          ' + item['payload']['release']['name'] + '\\n')
                msg += ('**Body:**     ' + item['payload']['release']['body']) + '\\n'

            if 'issue' in item['payload']:
                msg += ('**Link:**          ' + '<' + item['payload']['issue']['html_url'] + '>\\n')
                msg += ('**Title:**         ' + item['payload']['issue']['title'] + '\\n')
                msg += ('**Body:**    ' + item['payload']['issue']['body']) + '\\n'

            msg += '**Created at:**  ' + item['created_at'] + '\\n'

            # escape some special characters for json object
            msg = msg.replace('"', '\\"').replace('\r\n', '\\n').replace('\n', '\\n').replace('\t', '\\t').encode('ascii', 'ignore').decode('ascii')

            # Debug local
            # print '======================'
            # print ''
            # print repr(msg)   # print raw msg
            # print ''
            # print msg
            # exit()

            if firstRun == False:
                # check if msg lenght > 2000 (max discord content chars) - cheers devs! :D
                if len(msg) > 1999:
                    m = (len(msg) / 1999) + 1  # split msg into m parts
                    for i in xrange(1, m + 1):  # eg. xrange(1,6) will include 1 and exclude 6
                        time.sleep(10)  # http error 429 if too many/fast requests
                        deltaMsg = msg[((i - 1) * 1999):(i * 1999)]
                        myjson = '{"username": "GitHub-dashevo", "content": "' + deltaMsg + '"}'
                        response = requests.post(webhook_url, myjson, headers={'Content-Type': 'application/json'})
                        print 'Discord Webhook response: ' + str(response)
                        # error logging
                        if response.status_code != 204:
                            print 'Error http status code: ' + str(response.status_code)
                            print ''
                            print deltaMsg
                            errMsg = "########################\\nHTTP Error: " + str(response.status_code) + "\\nEvent id: " + str(
                                curId) + "\\nHello, im a bug. Come and find me! https://github.com/readme55/GithubPubEvents2Webhook\\n" + "########################\\n"
                            myjson = '{"username": "GitHub-dashevo", "content": "' + errMsg + '"}'
                            response = requests.post(webhook_url, myjson, headers={'Content-Type': 'application/json'})
                        ####################
                else:
                    # send the msg to discord webhook
                    myjson = '{"username": "GitHub-dashevo", "content": "' + msg + '"}'

                    response = requests.post(webhook_url, myjson, headers={'Content-Type': 'application/json'})

                    # error logging
                    print 'Discord Webhook response: ' + str(response)
                    if response.status_code != 204:  # TODO 400 is bad request, else is not bug
                        print 'Error http status code: ' + str(response.status_code)
                        errMsg = "########################\\nHTTP Error: " + str(response.status_code) + "\\nEvent id: " + str(
                            curId) + "\\nHello, im a bug. Come and find me! https://github.com/readme55/GithubPubEvents2Webhook\\n" + "########################\\n"

                        myjson = '{"username": "GitHub-dashevo", "content": "' + errMsg + '"}'

                        response = requests.post(webhook_url, myjson, headers={'Content-Type': 'application/json'})

                    ###################

            print datetime.datetime.now()

        firstRun = False

    except TypeError:
        print("TypeError")
        continue
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Goodbye")
        exit()
