"""A module that defines the expected format of the configuration file.

See the file `settings_rasa_TEMPLATE.py` for a template.
"""

from typing import Protocol, TypedDict, runtime_checkable

from blab_chatbot_bot_client.settings_format import BlabWebSocketBotClientSettings


class RasaSettings(TypedDict):
    """Contains parameters related to the Rasa bot."""

    ADDRESS: str
    """Rasa bot address. The port should be specified after a colon.
       Example: `http://localhost:5005/webhooks/rest/webhook`.
    """


@runtime_checkable
class BlabRasaClientSettings(BlabWebSocketBotClientSettings, Protocol):
    """A protocol that should be implemented by the configuration file.

    It extends the parent protocol (`BlabBotClientSettings`)
    with the inclusion of the `RASA_SETTINGS` field.
    """

    RASA_SETTINGS: RasaSettings

    DEV_ENVIRONMENT: bool
