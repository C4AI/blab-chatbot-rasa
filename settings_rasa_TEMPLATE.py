"""A module that contains settings for Watson bot client."""

from blab_chatbot_bot_client.settings_format import BlabWebSocketConnectionSettings

from blab_chatbot_rasa.rasa_settings_format import RasaSettings

# fmt: off

BLAB_CONNECTION_SETTINGS: BlabWebSocketConnectionSettings = {

    # Address of the (usually local) HTTP server that the controller will connect to:
    "BOT_HTTP_SERVER_HOSTNAME": "localhost",

    # Port of the aforementioned server:
    "BOT_HTTP_SERVER_PORT": 25225,

    # BLAB Controller address for WebSocket connections:
    "BLAB_CONTROLLER_WS_URL": "ws://localhost:8000",

}

RASA_SETTINGS: RasaSettings = {

    # Rasa bot address (the port should be specified after a colon):
    "ADDRESS": "http://localhost:5005/webhooks/rest/webhook",

}
