import requests
import logging
import logger_config
import urllib
from chatbot import message_to_bot

log = logging.getLogger(__name__)
log.info("Entered module: %s" % __name__)


class TelegramBot(object):
    """Class for TelegramBot housing functions required to interact with Telegram."""

    WEBAPP_URL = "https://christopher-mapbot.herokuapp.com/"
    GITHUB_REPO_URL = "https://github.com/vishakha-lall/MapBot/"
    GITHUB_ISSUES_URL = "https://github.com/vishakha-lall/MapBot/issues"
    slash_commands = {
        "/start": "Hey, did someone say my name? Here I am!\n\nValid commands are: start, about, help, report",
        "/about": f"Hi, I'm MapBot! Visit {WEBAPP_URL} to interact with my UI",
        "/help": f"I may know a lot about maps.\nWhere is Nairobi? What's the time at New York? How high is Mount Everest?\nI know them all. Want to know more about me? Head on to {GITHUB_REPO_URL}",  # noqa: E501
        "/report": f"Faced an issue with using me or do not like how I work? Head over to {GITHUB_ISSUES_URL} and let us know",
    }
    EXIT_CONVERSATION = "Bye! I'll miss you!"
    CONFUSED_CONVERSATION = "Sorry, I didn't get you. Could you try again?"

    @logger_config.logger
    def __init__(self, TELEGRAM_BOT_TOKEN: str, clf, learn_response) -> None:
        """Initiates a TelegramBot object with unique TELEGRAM_BOT_TOKEN and creates the base URL."""
        super(TelegramBot, self).__init__()
        self.TELEGRAM_BOT_TOKEN = TELEGRAM_BOT_TOKEN
        self.TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/"
        self.clf, self.learn_response = clf, learn_response
        logging.debug("MapBot ready")
        logging.debug("Telegram Bot ready")

    @logger_config.logger
    def send_message(self, text: str, chat_id: int) -> None:
        """Combine :text: and :chat_id:, create message and perform requests to Telegram Bot API."""
        url = (
            self.TELEGRAM_API_URL
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
    def get_data_from_webhook(self, webhook_update: dict) -> list:
        """Gets :webhook_update: and returns last update's :text: and :chat_id:."""
        try:
            text = webhook_update["message"]["text"]
        except Exception:
            logging.debug("Message not text")
            text = None
        try:
            chat_id = webhook_update["message"]["chat"]["id"]
        except Exception:
            logging.debug("No chat found")
            chat_id = None
        return (text, chat_id)

    @logger_config.logger
    def start(self, webhook_update: dict) -> bool:
        try:
            received_message, chat_id = self.get_data_from_webhook(webhook_update)
            logging.debug(received_message)
            logging.debug(chat_id)

            if received_message is None:
                # if latest message to bot is not of text format
                if chat_id is None:
                    # if there is no message and hence no chat_id (at bot start up)
                    pass  # do nothing
                else:
                    self.send_message(self.CONFUSED_CONVERSATION, chat_id)
            elif received_message.startswith("/"):
                # handling some slash-commands out of Telegram
                reply_message = self.slash_commands.get(received_message)
                if reply_message is None:
                    reply_message = self.CONFUSED_CONVERSATION
                self.send_message(reply_message, chat_id)
            else:
                logging.debug(
                    f"Message: '{received_message}' from chat_id: '{chat_id}'"
                )
                reply_message, self.learn_response = message_to_bot(
                    received_message, self.clf, self.learn_response
                )
                self.send_message(reply_message, chat_id)
                if reply_message == self.EXIT_CONVERSATION:
                    logging.debug(f"Ended chat with {chat_id}")
        except Exception as e:
            logging.debug(f"CRITICAL ERROR: {e}")
            return False
        else:
            return True
