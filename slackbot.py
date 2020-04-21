from slack import RTMClient
import ssl
import certifi
import requests
from config import slack_bot_token

# API ENDPOINT
URL = "http://localhost:5000/chatbot/"

ssl_context = ssl.create_default_context(cafile=certifi.where())


@RTMClient.run_on(event="message")
def mapbot(**payload):
    """
    This function is a listener for
    message events happening in the
    the workspace.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")

    # Ignore Bot Messages
    if bot_id == "":
        channel_id = data["channel"]
        # User message from slack
        text = data.get("text", "")
        text = text.split(">")[-1].strip()

        response = ""
        if "help" in text.lower():
            user = data.get("user", "")
            response = f"Hi <@{user}>! I am Mapbot :)"
        else:
            chatbot_response = requests.get(f"{URL}{text}").json()
            response = chatbot_response[0]["message"][0]

    # Sends the message to the slack
    web_client.chat_postMessage(channel=channel_id, text=response)


try:
    rtm_client = RTMClient(token=slack_bot_token, ssl=ssl_context)
    print("Mapbot is up and running!")
    rtm_client.start()
except Exception as err:
    print("Slack token or server error", err)
