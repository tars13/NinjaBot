import requests
import datetime
import time

# create a dictionary which keys are github usernames and values are slack IDs.
class4 = { "githubUserName" : "slackId"  }


def HW_control():
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    # The username of the github account whose repo we want to check at
    username = "github username"
    # url of sorted github repos
    repos_url = f"https://api.github.com/orgs/{username}/repos?sort=created"
    data = requests.get(repos_url).json()
    # the last repo's url
    repo_name = data[0]["name"]                                                     
    repo_link = data[0]["html_url"]

    # connect to the url of the last repo and get pull request senders
    last_repo_pulls_url = f"https://api.github.com/repos/{username}/{repo_name}/pulls"
    data = requests.get(last_repo_pulls_url).json()

    pulls = []

    # Get slack ids from github usernames
    for i in data:
        try:
            pulls.append(class4[i["user"]["login"]])
        except KeyError:
            continue
    slack_user_id = list(class4.values())

    # identify assignment non-submitters
    missing_HW = []


    for i in slack_user_id:
        if i not in pulls and i in slack_user_id:
            missing_HW.append(i)

    # message text
    board_message = f"""
    Those who have not done their <{repo_link}|*{repo_name}*> homework as of *{date}* : :ninjacoder:\n"""

    for i in missing_HW:
        board_message+="<@"+i+'>\n'

    load = {"type": "mrkdwn",
            "text":board_message}

    headers={"content-type":"application/json"}

    # Slack channel webhook
    slack_webhook = "https://hooks.slack.com/services/webhook"  

    # send slack channel
    sr = requests.post(url=slack_webhook, json=load, headers=headers)
    print("sr1",sr.status_code)

    # DM message text
    DM_message = f"""
    As of *{date}*, you have not submitted your <{repo_link}|*{repo_name}*> assignment yet.
    Please contact your mentor. :ninjacoder:\n"""

    # DM settings
    headers = {"Content-type": "application/json",
            "Authorization": "slack AuthorizationCode "}

    slack_webhook2 = "https://slack.com/api/chat.postMessage"

    print("missing_HW :", missing_HW)
    # send DM to anyone who didn't submit the assignment
    for i in missing_HW:  
        load2 = {"text":DM_message,
                "channel": i}
        sr2 = requests.post(url=slack_webhook2, json=load2, headers=headers)
        print("sr2",i,sr2.status_code)
        time.sleep(1)

