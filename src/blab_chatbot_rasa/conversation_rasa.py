"""A module that interacts with the APIs of Rasa and BLAB Controller."""
from typing import Any

import requests
from blab_chatbot_bot_client.conversation_websocket import (
    WebSocketBotClientConversation,
)
from blab_chatbot_bot_client.data_structures import (
    Message,
    MessageType,
    OutgoingMessage,
)
from overrides import overrides

from blab_chatbot_rasa.rasa_settings_format import BlabRasaClientSettings


class RasaWebSocketBotClientConversation(
    WebSocketBotClientConversation[BlabRasaClientSettings]
):
    """Performs the communication between Rasa and BLAB Controller."""

    def send_message_to_rasa(self, text: str) -> list[dict[str, Any]]:
        """Send a text message to the Rasa bot (on behalf of the user).

        Args:
        ----
            text: the message text

        Returns:
        -------
            the list of raw messages returned by the bot
        """
        r = requests.post(
            self.settings.RASA_SETTINGS["ADDRESS"],
            json={"sender": "conv_" + self.conversation_id, "message": text},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()

    @classmethod
    def process_bot_message(cls, message: dict[str, Any]) -> dict[str, Any]:
        """Process a message received from a Rasa bot.

        Args:
        ----
            message: the message as received from Rasa

        Returns:
        -------
            a dictionary with the message that will be sent back to the user
        """
        text = message.get("text", "")
        image = message.get("image", "")
        options = [o["title"] for o in message.get("buttons", [])]
        m = {"text": text or "", "type": MessageType.TEXT}
        if image:
            m["external_file_url"] = image
            m["type"] = MessageType.IMAGE
        if options:
            m["options"] = options
        return m

    @overrides
    def on_receive_message(self, message: Message) -> None:
        if message.sent_by_human and message.type == MessageType.TEXT:
            for answer in self.generate_answer(message):
                self.enqueue_message(answer)

    @overrides
    def generate_answer(self, message: Message) -> list[OutgoingMessage]:
        if not message.text:
            return []
        return [
            OutgoingMessage(
                **self.process_bot_message(data),
                local_id=self.generate_local_id(),
                quoted_message_id=message.id or None,
            )
            for data in self.send_message_to_rasa(message.text)
        ]
