import json
import socket
from time import sleep
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

    def __init__(self):
        self.__TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.__TCPSocket.connect(self.__serverAddressPort)

    def __del__(self):
        self.__TCPSocket.close()

    def send_request(self, action: int, data: dict = None, send_req=True, wait_res=True) -> dict:
        # формат запроса: {action (4 bytes)} + {data length (4 bytes)} +
        # + {bytes of UTF-8 string with data in JSON format}
        if send_req:
            bytes_to_send = action.to_bytes(4, byteorder='little')
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
        if wait_res:
            buffer = b''
            data_length = None
            while True:
                msg_from_server = self.__TCPSocket.recv(self.__bufferSize)
                buffer += msg_from_server

                if len(buffer) >= 8:  # получаем гарантированные первые 8 байт (result + data length)
                    if not data_length:
                        data_length = int.from_bytes(buffer[4:8], "little")
                    if len(buffer) >= data_length + 8:  # получаем доп. данные размера data_length
                        break

            code_result = int.from_bytes(buffer[:4], "little")
            print("Result: " + str(Result(code_result)))
            print("Data length: " + str(data_length))
            print("Full response: " + str(buffer))

            if Result(code_result) != Result.OKEY:
                return None

            if data_length > 0:
                data = json.loads(buffer[8:].decode('utf-8'))
                return data

    def send_login(self, name: str, password="", game: str = None, num_turns: int = None, num_players=1,
                   is_observer=False) -> int:
        """Возвращает id текущего игрока"""

        data = {"name": name, "password": password, "game": game, "num_turns": num_turns, "num_players": num_players,
                "is_observer": is_observer}
        login = self.send_request(1, data)

        print("-----LOGIN1: " + str(login))
        print()

        return login["idx"]

    def send_shoot(self, id: int, shoot_pos: dict):
        data = {"vehicle_id": id, "target": shoot_pos}
        self.send_request(102, data)
