import chatbot
import unittest

clf, learn_response = chatbot.setup()


class ChatBotTest(unittest.TestCase):
    def test_message_to_bot_directions(self):
        user_text = "What's the distance between Chicago and California?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertIn(
            bot_text,
            [
                "https://www.google.com/maps/dir/?api=1&origin=chicago&destination=california",
                "https://www.google.com/maps/dir/?api=1&origin=california&destination=chicago",
            ],
        )

    def test_message_to_bot_geocoding(self):
        user_text = "Where is Stockholm located?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(
            bot_text,
            "https://maps.google.com/?q=Stockholm,+Sweden&ftid=0x465f763119640bcb:0xa80d27d3679d7766",
        )

        user_text = "Where is New York?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(
            bot_text,
            "https://maps.google.com/?q=New+York,+NY,+USA&ftid=0x89c24fa5d33f083b:0xc80b8f06e177fe62",
        )

    def test_message_to_bot_timezone(self):
        user_text = "Which timezone is Missouri located in?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(bot_text, "America/Chicago")

        user_text = "What time is it now in California?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertIsInstance(bot_text, str)

        user_text = "What time is it now in New York?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertIsInstance(bot_text, str)

    def test_message_to_bot_elevation(self):
        user_text = "What is the height of Mount Everest?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(bot_text, "8809.1767578125 metres")

        user_text = "How high is Shimla from the sea level?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(bot_text, "2196.8125 metres")

    def test_message_to_bot_mapsstatic(self):
        import config

        user_text = "How does New York look in a map?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(
            bot_text,
            f"https://maps.googleapis.com/maps/api/staticmap?center=new+york&zoom=13&size=600x350&key={config.key}",
        )

        user_text = "Where is Nairobi on a map?"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(
            bot_text,
            f"https://maps.googleapis.com/maps/api/staticmap?center=nairobi&zoom=13&size=600x350&key={config.key}",
        )

        user_text = "Show me a map of Stockholm"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(
            bot_text,
            f"https://maps.googleapis.com/maps/api/staticmap?center=stockholm&zoom=13&size=600x350&key={config.key}",
        )

    def test_message_to_bot_places(self):
        user_text = "Harvard University"
        bot_text, learn_response = chatbot.message_to_bot(
            user_text, clf, chatbot.LearnResponse.MESSAGE.name
        )
        self.assertEqual(
            bot_text,
            "Harvard University: https://maps.google.com/?cid=6428825095529310192",
        )
