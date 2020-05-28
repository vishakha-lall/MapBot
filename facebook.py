import requests
import logging
import logger_config
from chatbot import message_to_bot

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


class FacebookBot(object):
    """Class for FacebookBot housing functions required to interact with Facebook Messenger."""

    @logger_config.logger
    def __init__(self, FB_ACCESS_TOKEN: str, clf, learn_response) -> None:
        """Initiates a FacebookBot object with unique FB_ACCESS_TOKEN and creates the base URL."""
        super(FacebookBot, self).__init__()
        self.FB_ACCESS_TOKEN = FB_ACCESS_TOKEN
        self.FB_API_URL = "https://graph.facebook.com/v7.0/me/messages"
        self.clf, self.learn_response = clf, learn_response
        logging.debug("MapBot ready")
        logging.debug("Facebook Messenger Bot ready")

    @logger_config.logger
    def handle_data_from_webhook(self, webhook_update: dict) -> None:
        try:
            for event in webhook_update["entry"]:
                messaging = event["messaging"]
                for message in messaging:
                    if (
                        message.get("message")
                        and message["message"].get("text")
                        and not message["message"].get("is_echo")
                    ):
                        received_message = message["message"]["text"]
                        sender_id = message["sender"]["id"]
                        self.respond(received_message, sender_id)
        except Exception as e:
            return e
        else:
            return "OK"

    @logger_config.logger
    def respond(self, received_message: str, sender_id: int) -> None:
        logging.debug(received_message)
        logging.debug(sender_id)
        reply_message, learn_response = message_to_bot(
            received_message, self.clf, self.learn_response
        )
        self.send_message(received_message, sender_id)

    @logger_config.logger
    def send_message(self, text: str, recipient_id: int):
        """Send a response to Facebook"""
        payload = {
            "message": {"text": text},
            "recipient": {"id": recipient_id},
            "notification_type": "regular",
        }
        auth = {"access_token": self.FB_ACCESS_TOKEN}
        response = requests.post(self.FB_API_URL, params=auth, json=payload)
        return response.json()

    @logger_config.logger
    def start(self, webhook_update: dict) -> bool:
        res = self.handle_data_from_webhook(webhook_update)
        if res == "OK":
            return True
        else:
            logging.debug(f"CRITICAL ERROR: {res}")
            return False
