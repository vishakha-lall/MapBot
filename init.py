import matplotlib.pyplot as plt
import io
import os
read csv
from chatbot import setup
from chatbot import message_to_bot
clf, learn_response = setup()    
while(True):
	received_message = input("You: ")
	send_message, learn_response = message_to_bot(received_message,clf,learn_response)
	print("MapBot: "+send_message)
return 1
