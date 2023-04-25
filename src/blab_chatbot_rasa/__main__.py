"""A module that is called from the command-line."""

from sys import argv

from blab_chatbot_bot_client.cli import BlabBotClientArgParser

from blab_chatbot_rasa.conversation_rasa import RasaWebSocketBotClientConversation

BlabBotClientArgParser(RasaWebSocketBotClientConversation).parse_and_run(argv[1:])
