import os
import time
import re
import requests
from slackclient import SlackClient

slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
mapbot_id = None

RTM_READ_DELAY = 1
EXAMPLE_COMMAND = "help"
MENTION_REGEX = "^<@(|[pipWU].+?)>(.*)"

# API endpoint currently running on localhost
URL = "http://127.0.0.1:5000/chatbot/"

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == mapbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if command is known
    """
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    response = None
    if command.startswith(EXAMPLE_COMMAND):
        response = "Hey There! I am MapBot. Nice to meet you"
    
    else:
        response = requests.get(url= URL+str(command)).json()
        response = response[0]['message'][0]
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == '__main__':
    if slack_client.rtm_connect(with_team_state=False):
        print("Mapbot started and running!")
        mapbot_id = slack_client.api_call("auth.test")["user_id"]

        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed")