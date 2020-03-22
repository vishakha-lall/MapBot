from flask import Flask, jsonify
from chatbot import message_to_bot, setup

app = Flask(__name__)

@app.route('/chatbot/<user_input>', methods=['GET'])
def chat(user_input):
    try:
        response = message_to_bot(user_input, clf, learn_response)
    except:
        return jsonify({'message': ('Unable to get response', learn_response)}, 500)
    
    return jsonify({'message': response}, 200)

if __name__ == '__main__':
    clf, learn_response = setup()
    app.run(debug=False)