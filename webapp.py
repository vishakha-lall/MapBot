from flask import Flask, render_template, request, jsonify
from chatbot import message_to_bot, setup

app = Flask(__name__)


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


if __name__ == "__main__":
    clf, learn_response = setup()
    app.run(debug=True)
