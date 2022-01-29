import json
import socket
from enum import Enum


class Result(Enum):
    OKEY = 0
    BAD_COMMAND = 1
    ACCESS_DENIED = 2
    INAPPROPRIATE_GAME_STATE = 3
    TIMEOUT = 4
    INTERNAL_SERVER_ERROR = 500


class ServerHandler:
    __serverAddressPort = ("wgforge-srv.wargaming.net", 443)
    __bufferSize = 4096

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ServerHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.__TCPSocket.connect(self.__serverAddressPort)

    def __del__(self):
        self.__TCPSocket.close()

    def send_request(self, action, data=None):
        # формат запроса: {action (4 bytes)} + {data length (4 bytes)} + {bytes of UTF-8 string with data in JSON format}
        bytes_to_send = action.value.to_bytes(4, byteorder='little')
        data_length = 0
        if data:
            json_value = json.dumps(data, separators=(',', ':'))
            data_length = len(json_value)
            bytes_to_send += data_length.to_bytes(4, byteorder='little') + bytes(json_value.encode('utf-8'))
        else:
            bytes_to_send += data_length.to_bytes(4, byteorder='little')
        print('\n---' + str(action) + '---')
        print('Sending: ' + repr(bytes_to_send))
        self.__TCPSocket.sendall(bytes_to_send)

        # получение ответа
        buffer = b''
        data_length = None
        while True:
            msgFromServer = self.__TCPSocket.recv(self.__bufferSize)
            buffer += msgFromServer

            if len(buffer) >= 8:  # получаем гарантированные первые 8 байт (result + data length)
                if not data_length:
                    data_length = int.from_bytes(buffer[4:8], "little")
                if len(buffer) >= data_length + 8:  # получаем доп. данные размера data_length
                    break

        code_result = int.from_bytes(buffer[:4], "little")
        print("Result: " + str(Result(code_result)))
        print("Data length: " + str(data_length))
        print("Full responce: " + str(buffer))

        if Result(code_result) != Result.OKEY:
            return None

        if data_length > 0:
            data = json.loads(buffer[8:].decode('utf-8'))
            return data
