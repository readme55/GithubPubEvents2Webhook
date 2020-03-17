import requests
import simplejson as json
from jsondiff import diff
import sys
import time
import datetime

# src
eventUrl = "https://api.github.com/users/dashevo/events/public"
# dest  (non-public so i put it in file and .gitignore)
f = open("./webhook.txt", "r")
if f.mode == 'r':
    webhook_url = f.read()
f.close()


## fetch github public events json file
# response = requests.get(eventUrl)
# print 'Github Public Events response: ' + str(response)
# data = json.loads(response.content)

# msg = "implementation of FundNewAccountActivity Hide Join DashPay action when sync not completed and\\nwhen balance is bellow minimum DashPay user creation fee\\n\\n Removed obsolete SporkUpdatedEventListenerink:             https://github.com/dashevo/dash-wallet/commit/9d8370e9b375823d925ffee3e4cc446d1644413b\\n__Author__:        Tomasz Ludek\\nMessage:    Merge branch evonet-develop into evonet-fund-new-account-confirm\\n\\n Conflicts:\\n    wallet/res/layout/activity_fund_new_account.xml\\n       wallet/src/de/schildbach/wallet/ui/FundNewAccountActivity.kt\\n wallet/src/de/schildbach/wallet/ui/WalletActivity.javaink:             https://github.com/dashevo/dash-wallet/commit/6b2848aa19ef3df322f839dd576646caee1dca66\\nCreated at:  2020-03-17T08:45:"
# msg = "s for evonet/palinka\n**Link:**             https://github.com/dashevo/dash-wallet/commit/f40339d6141a49b4f8fe1707214517eb2c030a3c\n**__Author__:**        tomasz-ludek\n**Message:**    Evonet: Add Shortcut Button | Create Username (#342)\n\n* Add 'Join DashPay' quick action (always visible)\n\n* Add mock implementation of FundNewAccountActivity\n\n* Hide 'Join DashPay' action when sync not completed and\nwhen balance is bellow minimum DashPay user creation fee\n\n* Removed obsolete SporkUpdatedEventListener\n**Link:**             https://github.com/dashevo/dash-wallet/commit/9d8370e9b375823d925ffee3e4cc446d1644413b\n**__Author__:**        Tomasz Ludek\n**Message:**    Merge branch 'evonet-develop' into evonet-fund-new-account-confirm\n\n# Conflicts:\n#        wallet/res/layout/activity_fund_new_account.xml\n#      wallet/src/de/schildbach/wallet/ui/FundNewAccountActivity.kt\n#        wallet/src/de/schildbach/wallet/ui/WalletActivity.java\n**Link:**             https://github.com/dashevo/dash-wallet/commit/6b2848aa19ef3df322f839dd576646caee1dca66\n**Created at:**  2020-03-17T08:45:"
# msg = ":**        tomasz-ludek**Message:**    Evonet: Add Shortcut Button | Create Username (#342)* Add 'Join DashPay' quick action (always visible)* Add mock implementation of FundNewAccountActivity* Hide 'Join DashPay' action when sync not completed andwhen balance is bellow minimum DashPay user creation fee* Removed obsolete SporkUpdatedEventListener**Link:**             https://github.com/dashevo/dash-wallet/commit/9d8370e9b375823d925ffee3e4cc446d1644413b**__Author__:**        Tomasz Ludek**Message:**    Merge branch 'evonet-develop' into evonet-fund-new-account-confirm# Conflicts:#  wallet/res/layout/activity_fund_new_account.xml#       wallet/src/de/schildbach/wallet/ui/FundNewAccountActivity.kt#   wallet/src/de/schildbach/wallet/ui/WalletActivity.java**Link:**             https://github.com/dashevo/dash-wallet/commit/6b2848aa19ef3df322f839dd576646caee1dca66**Created at:**  2020-03-17T08:45:27Z"
# msg = ":**        tomasz-ludek**Message:**    Evonet: Add Shortcut Button | Create Username (#342)* Add 'Join DashPay' quick action (always visible)* Add mock implementation of FundNewAccountActivity* Hide 'Join DashPay' action when sync not completed andwhen balance is bellow minimum DashPay user creation fee* Removed obsolete SporkUpdatedEventListener**Link:**             https://github.com/dashevo/dash-wallet/commit/9d8370e9b375823d925ffee3e4cc446d1644413b**__Author__:**        Tomasz Ludek**Message:**    Merge branch 'evonet-develop' into evonet-fund-new-account-confirm# Conflicts:#  wallet/res/layout/activity_fund_new_account.xml#       wallet/src/de/schildbach/wallet/ui/FundNewAccountActivity.kt#   wallet/src/de/schildbach/wallet/ui/WalletActivity.java**Link:**             https://github.com/dashevo/dash-wallet/commit/6b2848aa19ef3df322f839dd576646caee1dca66**Created at:**  2020-03-17T08:45:27Z"
msg = "t: Add Shortcut Button  Create Username (342)\\n Add Join DashPay quick action (always visible)\\n Add mock implementation of FundNewAccountActivity\\n Hide Join DashPay action when sync not completed and\\nwhen balance is bellow minimum DashPay user creation fee\\n Removed obsolete SporkUpdatedEventListener\\nLink:             https://github.com/dashevo/dash-wallet/commit/9d8370e9b375823d925ffee3e4cc446d1644413b\\n__Author__:        Tomasz Ludek\\nMessage:    Merge branch evonet-develop into evonet-fund-new-account-confirm\\n Conflicts:\\n  wallet/res/layout/activity_fund_new_account.xml\\n      wallet/src/de/schildbach/wallet/ui/FundNewAccountActivity.kt\\n        wallet/src/de/schildbach/wallet/ui/WalletActivity.java\\nLink:             https://github.com/dashevo/dash-wallet/commit/6b2848aa19ef3df322f839dd576646caee1dca66\\nCreated at:  2020-03-17T08:45:27Z\\n"

# msg = msg.replace('\n' , '\\n')

print msg

## send the msg to discord webhook
myjson = '{"username": "GitHub-dashevo", "content": "' + msg + '"}'
response = requests.post(
    webhook_url,
    myjson,
    headers={'Content-Type': 'application/json'})
print 'Discord Webhook response: ' + str(response)


