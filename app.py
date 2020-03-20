from flask import Flask, jsonify
from chatbot import message_to_bot, setup

app = Flask(__name__)

@app.route('/chatbot/<input_user>', methods=['GET'])
def chat(input_user):
    clf, learn_response = setup()
    try:
        response = message_to_bot(input_user, clf, learn_response)
    except:
        return jsonify({'chatbot': "Unable to get response"})
    
    return jsonify({'chatbot': response})

if __name__ == '__main__':
    app.run(debug=False)
