import websocket
import rel
from threading import Thread
import sys


class Socket:
    def __init__(self, animemusicapi) -> None:
        self.animemusicapi = animemusicapi
        self.ws = None
        self.connect()

    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.animemusicapi.get_websocket_url(),
            on_open=self.ws_ready,
            on_message=self.ws_receive_message,
            on_error=self.ws_error,
            on_close=self.ws_close,
            cookie=self.animemusicapi.session.cookies.get_dict()["io"],
            subprotocols=["websocket"],
            header={
                "Origin": "https://animemusicquiz.com",
                "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                "Sec-WebSocket-Version": "13",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
            },
        )
        
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.start()

    def ws_ready(self, ws):
        ws.send("2probe")
        ws.send("5")

    @staticmethod
    def ws_error(ws, error):
        print(error)

    @staticmethod
    def ws_close(ws, close_status_code, close_msg):
        sys.exit(0)

    def ws_receive_message(self, ws, message):
        ws.send("2")

        if message != "3":
            print(message)


    def test(self):
        self.ws.send('42["command",{"type":"roombrowser","command":"host solo room","data":{"roomName":"Solo","privateRoom":false,"password":"","roomSize":8,"numberOfSongs":100,"teamSize":1,"modifiers":{"skipGuessing":true,"skipReplay":true,"duplicates":true,"queueing":true,"lootDropping":true,"rebroadcastSongs":true,"dubSongs":false},"songSelection":{"standardValue":1,"advancedValue":{"watched":0,"unwatched":0,"random":100}},"watchedDistribution":1,"songType":{"standardValue":{"openings":true,"endings":true,"inserts":false},"advancedValue":{"openings":0,"endings":0,"inserts":0,"random":100}},"openingCategories":{"instrumental":true,"chanting":true,"character":true,"standard":true},"endingCategories":{"instrumental":true,"chanting":true,"character":true,"standard":true},"insertCategories":{"instrumental":true,"chanting":true,"character":true,"standard":true},"guessTime":{"randomOn":false,"standardValue":5,"randomValue":[5,60]},"scoreType":1,"showSelection":1,"inventorySize":{"randomOn":false,"standardValue":20,"randomValue":[1,99]},"lootingTime":{"randomOn":false,"standardValue":90,"randomValue":[10,150]},"lives":5,"samplePoint":{"randomOn":true,"standardValue":1,"randomValue":[0,100]},"playbackSpeed":{"randomOn":false,"standardValue":1,"randomValue":[true,true,true,true]},"songDifficulity":{"advancedOn":false,"standardValue":{"easy":false,"medium":false,"hard":true},"advancedValue":[0,100]},"songPopularity":{"advancedOn":false,"standardValue":{"disliked":true,"mixed":true,"liked":true},"advancedValue":[0,100]},"playerScore":{"advancedOn":false,"standardValue":[1,10],"advancedValue":[true,true,true,true,true,true,true,true,true,true]},"animeScore":{"advancedOn":false,"standardValue":[2,10],"advancedValue":[true,true,true,true,true,true,true,true,true]},"vintage":{"standardValue":{"years":[1944,2022],"seasons":[0,3]},"advancedValueList":[]},"type":{"tv":true,"movie":true,"ova":true,"ona":true,"special":true},"genre":[],"tags":[],"gameMode":"Solo"}}]')
