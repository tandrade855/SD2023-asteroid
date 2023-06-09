from threading import Thread
from game_mechanics import GameMechanics
from constantes import *
import json
import logging
import socket


class ClientSession(Thread):
    """Maintains a session with the client"""

    def __init__(self, socket_client: socket,  game_mech: GameMechanics):
        """
        Constructs a thread to hold a session with the client
        """
        Thread.__init__(self)
        self.socket_client = socket_client
        self.gm = game_mech

    def send_counter(self):
        counter = self.gm.counter
        self.socket_client.send(counter.to_bytes(N_BYTES, byteorder="big", signed=True))

    def send_player(self):
        player = self.gm.player
        msg = json.dumps(player)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def send_asteroids(self):
        asteroids = self.gm.asteroids
        msg = json.dumps(asteroids)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def send_lasers(self):
        lasers = self.gm.lasers
        msg = json.dumps(lasers)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def all_players(self):
        players = self.gm.players
        msg = json.dumps(players)
        dim = len(msg)
        self.socket_client.send(dim.to_bytes(N_BYTES, byteorder="big", signed=True))
        self.socket_client.send(msg.encode(STR_COD))

    def remove_player1(self):
        self.gm.players.pop(0)

    def remove_player2(self):
        self.gm.players.pop(1)

    def update_positions(self, msg, player: int):
        if msg == LEFT1 or msg == LEFT2:
            msg = LEFT
        if msg == RIGHT1 or msg == RIGHT2:
            msg = RIGHT
        if msg == UP1 or msg == UP2:
            msg = UP

        self.gm.update_positions(msg, player)

    def msg_dispatcher(self, socket_client) -> bool:
        end = False
        self.gm.clock.tick(self.gm.FPS)

        if len(self.gm.asteroids) == 0:
            self.gm.create_asteroids()

        self.gm.check_collisions()

        self.gm.move_laser()

        data_recv: bytes = self.socket_client.recv(MSG_SIZE)
        msg = data_recv.decode(STR_COD)
        if msg == GET_COUNTER:
            self.send_counter()
        if msg == GET_PLAYERS:
            self.send_player()
        if msg == ALL_PLAYERS:
            self.all_players()
        if msg == REM_PLAYER1:
            self.remove_player1()
        if msg == REM_PLAYER2:
            self.remove_player2()
        if msg == GET_AST:
            self.send_asteroids()
        if msg == GET_LASERS:
            self.send_lasers()
        if msg == LEFT1 or msg == RIGHT1 or msg == UP1:
            self.update_positions(msg, 0)
        if msg == LEFT2 or msg == RIGHT2 or msg == UP2:
            self.update_positions(msg, 1)
        if msg == END:
            socket_client.send(END.encode(STR_COD))
            end = True
        return end

    def run(self):
        last_request = False
        while not last_request:
            last_request = self.msg_dispatcher(self.socket_client)
        logging.debug("Client " + str(self.socket_client.peer_addr) + " disconnected")