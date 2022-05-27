from utils.api import AnimeMusicAPI
from utils.socket import Socket
import sys

if __name__ == "__main__":
    animemusicapi = AnimeMusicAPI(username="", password="")
    socket = Socket(animemusicapi)
    input()
    socket.test()
    input()
    socket.ws.close()
    sys.exit(0)