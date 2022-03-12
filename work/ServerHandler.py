import json
import socket
import logging
from typing import Optional, Dict
from work.ServerCommands import Action, Result
from work.ServerConfig import ADDRESS, PORT, ACTION_LENGTH, RESULT_LENGTH, DATA_LENGTH

logging.basicConfig(level=logging.DEBUG,
                    format='\n%(levelname)s - %(asctime)s - %(message)s',
                    datefmt='%H:%M:%S')

logging.basicConfig(level=logging.DEBUG, format='\n%(levelname)s - %(asctime)s - %(message)s', datefmt='%H:%M:%S')


class ServerHandler:
    __serverAddressPort = (ADDRESS, PORT)
    __bufferSize = 4096

    def __init__(self):
        self.__TCPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.__TCPSocket.connect(self.__serverAddressPort)

    def __del__(self):
        self.__TCPSocket.close()

    def send_request(self, action, data=None, send_req=True, wait_res=True) -> Optional[Dict]:
        # request format: {action (4 bytes)} + {data length (4 bytes)} +
        # + {bytes of UTF-8 string with data in JSON format}
        if send_req:
            bytes_to_send = action.value.to_bytes(ACTION_LENGTH, byteorder='little')
            data_length = 0
            if data:
                json_value = json.dumps(data, separators=(',', ':'))
                data_length = len(json_value)
                bytes_to_send += \
                    data_length.to_bytes(DATA_LENGTH, byteorder='little') + bytes(json_value.encode('utf-8'))
            else:
                bytes_to_send += data_length.to_bytes(DATA_LENGTH, byteorder='little')
            self.__TCPSocket.sendall(bytes_to_send)

        # receiving answer
        if wait_res:
            buffer = b''
            data_length = None
            while True:
                msg_from_server = self.__TCPSocket.recv(self.__bufferSize)
                buffer += msg_from_server

                if len(buffer) >= RESULT_LENGTH + DATA_LENGTH:  # getting first bytes (result + data_length)
                    if not data_length:
                        data_length = int.from_bytes(buffer[RESULT_LENGTH:RESULT_LENGTH + DATA_LENGTH], "little")
                    # extra data with the size of data_length
                    if len(buffer) >= RESULT_LENGTH + DATA_LENGTH + data_length:
                        break

            code_result = int.from_bytes(buffer[:RESULT_LENGTH], "little")
            print_log = logging.info
            if Result(code_result) != Result.OKEY:
                print_log = logging.error
                print_log('\n---' + str(Action(action)) + '---' +
                          "\nResult: " + str(Result(code_result)) +
                          "\nData length: " + str(data_length) +
                          "\nFull response: " + str(buffer))
                return None

            if data_length > 0:
                data = json.loads(buffer[RESULT_LENGTH + DATA_LENGTH:].decode('utf-8'))
                return data

    # returns id of the current player
    def send_login(self, name: str, password: str, game: str,
                   num_turns: int, num_players: int,
                   is_observer: bool) -> int:
        data = {"name": name, "password": password, "game": game,
                "num_turns": num_turns, "num_players": num_players,
                "is_observer": is_observer}
        login = self.send_request(Action.LOGIN, data)
        return login["idx"]

    def send_shoot(self, id: int, shoot_pos: dict) -> None:
        data = {"vehicle_id": id, "target": shoot_pos}
        self.send_request(Action.SHOOT, data)
