from chatbot import setup
from chatbot import message_to_bot

clf, learn_response = setup()
EXIT_CONVERSATION = "Bye! I'll miss you!"
while True:
    received_message = input("You: ")
    send_message, learn_response = message_to_bot(received_message, clf, learn_response)
    print("MapBot:", send_message)
    if send_message == EXIT_CONVERSATION:
        break
