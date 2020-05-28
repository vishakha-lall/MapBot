from flask import Flask, render_template, request, jsonify
from chatbot import message_to_bot, setup
import suggestive_chatbot
import config

app = Flask(__name__)
clf, learn_response = setup()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    global clf, learn_response

    user_input = request.form["usrInput"]
    if user_input:
        bot_text, learn_response = message_to_bot(user_input, clf, learn_response)
        return jsonify({"botText": bot_text})

    return jsonify({"error": "Missing data!"})


@app.route("/suggestions", methods=["POST"])
def suggestions():
    form_id = request.form["id"]
    if form_id == "form_directions":
        origin, destination = request.form.getlist("eles[]")[:-1]
        bot_text = suggestive_chatbot.directions_suggestion(origin, destination)
        return jsonify({"botText": bot_text})
    if form_id == "form_geocoding":
        location_text = request.form.getlist("eles[]")[:-1]
        bot_text = suggestive_chatbot.geocoding_suggestion(location_text)
        return jsonify({"botText": bot_text})
    if form_id == "form_timezone":
        location_text, tz_option = request.form.getlist("eles[]")[:-1]
        tz_options = {"T": "time", "TZ": "timezone"}
        if tz_option == "":
            bot_text = suggestive_chatbot.timezone_suggestion(location_text)
        elif tz_option in tz_options:
            bot_text = suggestive_chatbot.timezone_suggestion(
                location_text, tz_options[tz_option]
            )
        return jsonify({"botText": bot_text})
    if form_id == "form_elevation":
        location_text, location_comp_text = request.form.getlist("eles[]")[:-1]
        if location_comp_text != "":
            bot_text = suggestive_chatbot.elevation_suggestion(
                location_text, location_comp_text
            )
        else:
            bot_text = suggestive_chatbot.elevation_suggestion(location_text)
        return jsonify({"botText": bot_text})
    if form_id == "form_map":
        kwargs = {}
        location_text, zoom, size = request.form.getlist("eles[]")[:-1]
        if zoom != "":
            kwargs["zoom"] = zoom
        if size != "":
            kwargs["size"] = size
        bot_text = suggestive_chatbot.mapsstatic_suggestion(location_text, **kwargs)
        return jsonify({"botText": bot_text})

    return jsonify({"error": "Missing data!"})


TOKEN = config.tbot_token
# Creates a TelegramBot object with tbot_token present in `config.py`

# webhook of Telegram Bot already set to this endpoint (prerequisite)
@app.route(f"/telegram/{TOKEN}", methods=["POST"])
def telegram_webhook():
    from telegram import TelegramBot

    tbot = TelegramBot(TOKEN, clf, learn_response)
    webhook_update = request.get_json()
    print(webhook_update)
    done = tbot.start(webhook_update)
    if done:
        return jsonify({"Success": 200})
    else:
        return jsonify({"Failure": 500})


FB_VERIFY_TOKEN = config.fb_verify_token
FB_ACCESS_TOKEN = config.fb_access_token

# webhook of Facebook Bot already set to this endpoint with FB_VERIFY_TOKEN(prerequisite)
@app.route("/facebook", methods=["GET", "POST"])
def facebook_webhook():
    if request.method == "GET":
        token_sent = request.args.get("hub.verify_token")
        if token_sent == FB_VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return jsonify({"FB Verification Error": 401})

    elif request.method == "POST":
        from facebook import FacebookBot

        fb_bot = FacebookBot(FB_ACCESS_TOKEN, clf, learn_response)
        webhook_update = request.get_json()
        print(webhook_update)
        done = fb_bot.start(webhook_update)
        if done:
            return jsonify({"Success": 200})
        else:
            return jsonify({"Failure": 500})


if __name__ == "__main__":
    app.run(debug=True)
