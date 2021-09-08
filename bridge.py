from enum import IntEnum
from websocket import create_connection, ABNF
import socket

TCP_IP = 'localhost'
TCP_PORT = 1337
BUFFER_SIZE = 1024


class CMDOpcodes(IntEnum):
    ERROR = 0x00
    GET_ENTIRE_IMAGE = 0x01
    ENTIRE_IMAGE = 0x02
    UPDATE_PIXEL = 0x03
    UNMINED_TRANSACTION = 0x04
    MINED_TRANSACTION = 0x05
    GET_PIXEL_DATA = 0x06
    PIXEL_DATA = 0x07
    GET_STORE_ITEMS = 0x08
    STORE_ITEMS = 0x9
    BUY_STORE_ITEM = 0x0a
    GET_USER_DATA = 0x0b
    USER_DATA = 0x0c


colorMap = [
    "000000",
    "FF0000",
    "00FF00",
    "0000FF",
    "FFFF00",
    "FF00FF",
    "00FFFF",
    "FFFFFF"]

ws = create_connection('wss://api.celestium.hutli.org')
ws.send([int(CMDOpcodes.GET_ENTIRE_IMAGE)], ABNF.OPCODE_BINARY)
entire_image = list(map(lambda i: colorMap[i], ws.recv()))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
to_send = ""
for x in range(1000):
    for y in range(1000):
        to_send += f"PX {x} {y} {entire_image[x * y]}\n"
s.send(to_send.encode())
