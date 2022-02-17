import asyncio
import socket
from enum import IntEnum
from time import sleep

import websockets


class CMDOpcodes(IntEnum):
    GET_PIXEL_COLOR = 0x00
    PIXEL_COLOR = 0x01
    GET_CANVAS = 0x02
    CANVAS = 0x03
    UPDATED_PIXEL_EVENT = 0x04
    UNMINED_TRANSACTION = 0x05
    MINED_TRANSACTION = 0x06
    GET_PIXEL_MINING_DATA = 0x07
    PIXEL_MINING_DATA = 0x08
    GET_STORE_ITEM = 0x09
    STORE_ITEM = 0x0A
    BUY_STORE_ITEM = 0x0B
    GET_USER_DATA = 0x0C
    USER_DATA = 0x0D
    GET_USER_MIGRATION_TRANSACTION = 0x0E


colorMap = [
    "000000",
    "E50000",
    "02BE01",
    "0000EA",
    "F8F208",
    "FD5EF8",
    "00D3DD",
    "FFFFFF",
    "7415CD",
    "F3C99D",
    "999999",
    "E59500",
    "0083C7",
    "347115",
    "43270A",
    "865A48",
]

TCP_IP = "localhost"
TCP_PORT = 1337
BUFFER_SIZE = 1024
INSTANCE_URL = "wss://api.celestium.space"


async def main(instance):
    while True:
        try:
            async with websockets.connect(instance, ping_interval=None) as ws:
                await ws.send(bytes([int(CMDOpcodes.GET_CANVAS)]))
                while True:
                    message = await ws.recv()
                    cmd = int(message[0])
                    data = message[1:]
                    if cmd == CMDOpcodes.CANVAS:
                        print("Got entire image")
                        to_send = ""
                        for y in range(1000):
                            for x in range(1000):
                                color = colorMap[data[x + (y * 1000)]]
                                tmp = f"PX {x} {y} {color}\n"
                                to_send += tmp
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((TCP_IP, TCP_PORT))
                        s.send(to_send.encode())
                        s.close()
                    elif cmd == CMDOpcodes.UPDATED_PIXEL_EVENT:
                        x = (int(data[0]) << 8) + int(data[1])
                        y = (int(data[2]) << 8) + int(data[3])
                        try:
                            c = colorMap[int(data[4])]
                        except IndexError:
                            c = colorMap[0]
                        print(f"Got new pixel {x, y} -> {c}")
                        to_send = f"PX {x} {y} {c}\n"

                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((TCP_IP, TCP_PORT))
                        s.send(to_send.encode())
                        s.close()
        except Exception as e:
            print(f'Could not connect to "{instance}", retrying in 5min: "{e}"')
        sleep(60 * 5)


if __name__ == "__main__":
    asyncio.run(main(INSTANCE_URL))
