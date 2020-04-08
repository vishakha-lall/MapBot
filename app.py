from flask import Flask, jsonify, request
from chatbot import message_to_bot, setup
from config import slack_client_id, slack_client_secret
from config import slack_oauth_scope
import certifi
import ssl
import slack

CLIENT_ID = slack_client_id
CLIENT_SECRET = slack_client_secret
OAUTH_SCOPE = slack_oauth_scope

app = Flask(__name__)
ssl_context = ssl.create_default_context(cafile=certifi.where())


@app.route("/chatbot/<user_input>", methods=["GET"])
def chat(user_input):
    try:
        response = message_to_bot(user_input, clf, learn_response)
    except Exception as e:
        print(e)
        return jsonify({"message": ("Unable to get response", learn_response)}, 500)

    return jsonify({"message": response}, 200)


@app.route("/begin_auth", methods=["GET"])
def pre_install():
    return f"""<a href="https://slack.com/oauth/authorize?
            scope={OAUTH_SCOPE}&client_id={CLIENT_ID}">
            <img alt=""Add to Slack"" height="40" width="139"
            src="https://platform.slack-edge.com/img/add_to_slack.png"
            srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x,
            https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
            """


@app.route("/post_auth", methods=["GET", "POST"])
def post_install():
    """
        After user authorizes the bot to access its workspace slack
        generates a temporary code which this function exchanges with
        the BOT_USER_ACCESS_TOKEN
    """
    # Retrieve the auth code from the request params
    auth_code = request.args["code"]
    # An empty string is a valid token from this request
    client = slack.WebClient(token="", ssl=ssl_context)
    # Request the auth token from slack
    response = client.oauth_access(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=auth_code
    )
    BOT_TOKEN = response["bot"]["bot_access_token"]
    f = open("ENV/.env", "a")
    f.write(f"\nSLACK_BOT_TOKEN={BOT_TOKEN}")
    f.close()
    return "<h2 align='center'>Auth Completed! You may close this window</h2>"


if __name__ == "__main__":
    clf, learn_response = setup()
    app.run(debug=True)
