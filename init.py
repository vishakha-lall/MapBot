from chatbot import setup
from chatbot import message_to_bot
clf, learn_response = setup()
while(True):
    received_message = input("You: ")
    send_message, learn_response = message_to_bot(received_message, clf, learn_response)
    print("MapBot:  " + send_message)
	if received_message.lower() == "bye" or received_message.lower() == "bye." or received_message.lower() == "bye!":															#exit loop
		break