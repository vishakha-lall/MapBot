import requests
import json
import time
import logging
import logger_config
import urllib


log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


class TelegramBot(object):
    """Class for TelegramBot housing functions required to interact with Telegram."""

    @logger_config.logger
    def __init__(self, TOKEN: str) -> None:
        """Initiates a TelegramBot object with unique Telegram BOT_TOKEN and creates the base URL."""
        super(TelegramBot, self).__init__()
        self.TOKEN = TOKEN
        self.URL = f"https://api.telegram.org/bot{TOKEN}/"
        logging.debug("Telegram Bot ready")

    @logger_config.logger
    def send_message(self, text: str, chat_id: int) -> None:
        """Combine :text: and :chat_id:, create message and perform requests to Telegram Bot API."""
        url = (
            self.URL
            + "sendMessage"
            + "?"
            + urllib.parse.urlencode({"text": text, "chat_id": chat_id})
        )
        self.get_url(url)

    @logger_config.logger
    def get_url(self, url: str) -> str:
        """Gather response from :url: and decode using 'utf8'."""
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    @logger_config.logger
    def get_json_from_url(self, url: str) -> dict:
        """Takes :url: and returns json-like object of response."""
        content = self.get_url(url)
        js = json.loads(content)
        return js

    @logger_config.logger
    def get_updates(self) -> dict:
        """Gets json-like object of message Updates to bot."""
        url = self.URL + "getUpdates"
        js = self.get_json_from_url(url)
        return js

    @logger_config.logger
    def get_last_chat_id_and_text(self) -> (str, int):
        """Fetches :updates: and returns last update's :text: and :chat_id:."""
        updates = self.get_updates()
        try:
            text = updates["result"][-1]["message"]["text"]
        except Exception:
            logging.debug("Message not text")
            text = None
        chat_id = updates["result"][-1]["message"]["chat"]["id"]
        return (text, chat_id)


if __name__ == "__main__":
    import config

    TOKEN = config.tbot_token
    # Creates a TelegramBot object with tbot_token present in `config.py`
    tbot = TelegramBot(TOKEN)

    from chatbot import setup
    from chatbot import message_to_bot

    clf, learn_response = setup()
    EXIT_CONVERSATION = "Bye! I'll miss you!"
    CONFUSED_CONVERSATION = "Sorry, I didn't get you. Could you try again?"
    logging.debug("MapBot ready")

    last_textchat = (None, None)
    # initialized to continously check for new messages
    try:
        while True:
            received_message, chat_id = tbot.get_last_chat_id_and_text()
            logging.debug(received_message)
            logging.debug(chat_id)

            if (received_message, chat_id) != last_textchat:
                # checking if any new messages have arrived since the last message

                if received_message is None:
                    # if latest message to bot is not of text format
                    print(chat_id)
                    tbot.send_message(CONFUSED_CONVERSATION, chat_id)
                else:
                    logging.debug("Received: " + received_message)
                    reply_message, learn_response = message_to_bot(
                        received_message, clf, learn_response
                    )
                    tbot.send_message(reply_message, chat_id)
                    if reply_message == EXIT_CONVERSATION:
                        break

                last_textchat = (received_message, chat_id)
            # Wait for 0.5 secs before rechecking for new messages. (good for server)
            time.sleep(0.5)

    except Exception as e:
        logging.debug("EXCEPTION OCCURRED")
        logging.debug(e)
