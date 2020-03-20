# GithubPubEvents2Webhook

## Description
Parse all info from Github Public events `https://api.github.com/users/<name>/events/public` eg. `https://api.github.com/users/dashevo/events/public` and forward them to some (discord) webhook.

## TODO:
- fix rare http 400 / bad request error (when forwarding to discord webhook) -> check .encode('ascii' [...] and view output with repr() to find bug
- optimise output/infos