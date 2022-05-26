import json
import re
import time
from math import ceil

import requests


class AnimeMusicAPI:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

        self.base_domaine = "animemusicquiz.com"

        self.session = requests.Session()
        self.endpoints = {
            "login": f"https://{self.base_domaine}/signIn",
            "signout": f"https://{self.base_domaine}/signout",
            "socketToken": f"https://{self.base_domaine}/socketToken",
        }

        self.login = self.login()
        self.token, self.port = self.socketToken()
        self.sid = self.get_socket_sid()

    def get_websocket_url(self):
        return f"wss://socket.animemusicquiz.com:{self.port}/socket.io/?token={self.token}&EIO=3&transport=websocket&sid={self.sid}"

    def socketToken(self):
        socketToken = self.session.get(self.endpoints["socketToken"]).json()
        return socketToken["token"], socketToken["port"]

    def get_socket_sid(self) -> str:
        polling = self.session.get(
            f"https://socket.animemusicquiz.com:{self.port}/socket.io/?token={self.token}&EIO=3&transport=polling&t="
        ).text

        return json.loads(re.search("\{(.*?)\}", polling).group())["sid"]

    def login(self) -> str:
        data = {"username": self.username, "password": self.password}

        login = self.session.post(self.endpoints["login"], json=data)

        if login.status_code == 429 and login.text.startswith("Too many requests"):
            retry_in = float(login.text.split("please wait ")[1].split(" ")[0])
            print(f'"Too many requests" detected, retry in {retry_in} seconds')
            time.sleep(ceil(retry_in))
            self.login()

        return login

    def logout(self) -> json:
        return self.session.get(self.endpoints["signout"])
