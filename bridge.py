from enum import IntEnum
import websocket
import socket


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
    BUY_STORE_ITEM = 0x0A
    GET_USER_DATA = 0x0B
    USER_DATA = 0x0C


colorMap = [
    "000000",
    "e50000",
    "02be01",
    "0000ea",
    "f8f208",
    "fd5ef8",
    "00d3dd",
    "ffffff",
    "7415cd",
    "f3c99d",
    "999999",
    "e59500",
    "0083c7",
    "347115",
    "43270a",
    "865a48",
]

TCP_IP = "localhost"
TCP_PORT = 1337

BUFFER_SIZE = 1024


def on_message(ws, message):
    cmd = int(message[0])
    data = message[1:]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    if cmd == CMDOpcodes.ENTIRE_IMAGE:
        print("Got entire image")
        to_send = ""
        for y in range(1000):
            for x in range(1000):
                color = colorMap[data[x + (y * 1000)]]
                tmp = f"PX {x} {y} {color}\n"
                to_send += tmp

        s.send(to_send.encode())
    elif cmd == CMDOpcodes.UPDATE_PIXEL:
        x = (int(data[0]) << 8) + int(data[1])
        y = (int(data[2]) << 8) + int(data[3])
        c = colorMap[int(data[4])]
        print(f"Got new pixel {x, y} -> {c}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        to_send = f"PX {x} {y} {c}\n"
        s.send(to_send.encode())

    s.close()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):

    print("### closed ###")


def on_open(ws):
    ws.send(bytearray([int(CMDOpcodes.GET_ENTIRE_IMAGE)]), websocket.ABNF.OPCODE_BINARY)


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://api.celestium.space",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()
