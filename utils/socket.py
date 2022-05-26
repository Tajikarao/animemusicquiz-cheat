import websocket
import rel
import sys


class Socket:
    def __init__(self, animemusicapi) -> None:
        self.animemusicapi = animemusicapi
        self.connect()

    def connect(self):
        ws = websocket.WebSocketApp(
            self.animemusicapi.get_websocket_url(),
            on_open=self.ws_ready,
            on_message=self.ws_receive_message,
            on_error=self.ws_error,
            on_close=self.ws_close,
            cookie=self.animemusicapi.session.cookies.get_dict()["io"],
            subprotocols=["websocket"],
            header={
                "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                "Sec-WebSocket-Version": "13",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            },
        )

        ws.run_forever(origin="https://animemusicquiz.com", dispatcher=rel)
        rel.signal(2, rel.abort)
        rel.dispatch()

    @staticmethod
    def ws_ready(ws):
        ws.send("2probe")
        ws.send("5")

    @staticmethod
    def ws_error(ws, error):
        print(error)

    @staticmethod
    def ws_close(ws, close_status_code, close_msg):
        sys.exit(0)

    @staticmethod
    def ws_receive_message(ws, message):
        ws.send("2")

        if message != "3":
            print(message)
