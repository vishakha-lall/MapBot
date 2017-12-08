from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
import json, requests, random, re
from chatbot import setup
from chatbot import message_to_bot
# Create your views here.
clf = setup()
learning_response = 0

class mapbotView(generic.View):

    def get(self, request, **kwargs):
        if self.request.GET['hub.verify_token'] == '9829096118':
                return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    print(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def post_facebook_message(fbid, received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAdAgdyXAyIBANZAZAwkS15IdM4lUyuUiQV351OLKd4t1ePkdG6IShx1dGbZC83rYkQAfyKtjIgoCWoFNWuqt9WM3fWGe1G7ejTyFdPsCJyQFjYwUZBTogwwZBZBclk7yi0tMMpQUtNnRlhRRk32WBAv5yuxfbWvyLBvrS8YAZAIGQW2Voxh48q'
    send_message = message_to_bot(received_message,clf)
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":send_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    print(status.json())
