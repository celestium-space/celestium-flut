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


TCP_IP = 'localhost'
TCP_PORT = 1337
BUFFER_SIZE = 1024

def on_message(ws, message):
    cmd = int(message[0])
    data = message[1:]
    if cmd == CMDOpcodes.ENTIRE_IMAGE:
        print("Got entire image")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        to_send = ""
        for y in range(1000):
            for x in range(1000):
                to_send += f"PX {x} {y} {colorMap[data[x + (y * 1000)]]}\n"
        s.send(to_send.encode())
        s.close()
    elif cmd == CMDOpcodes.UPDATE_PIXEL:
        x = (int(data[0]) << 8) + int(data[1])
        y = (int(data[2]) << 8) + int(data[3])
        c = colorMap[int(data[4])]
        print(f"Got new pixel {x, y} -> {c}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(f"PX {x} {y} {c}\n".encode())
        s.close()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    ws.send(bytearray([int(CMDOpcodes.GET_ENTIRE_IMAGE)]), websocket.ABNF.OPCODE_BINARY)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://api.celestium.hutli.org',
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    ws.run_forever()
