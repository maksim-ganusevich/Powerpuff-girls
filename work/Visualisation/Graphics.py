from sys import exit
import pygame
from pygame.color import THECOLORS
from math import fabs, sin, pi, sqrt, cos
from work.GameState import GameState
from work.Map import Map
from work.Singleton import Singleton

COLORS = [(46, 196, 182), (231, 29, 54), (255, 159, 28)]
ICONS_PATH = {
    "at_spg": "work\\Visualisation\\icons\\at_spg.png",
    "heavy_tank": "work\\Visualisation\\icons\\heavy_tank.png",
    "light_tank": "work\\Visualisation\\icons\\light_tank.png",
    "medium_tank": "work\\Visualisation\\icons\\medium_tank.png",
    "spg": "work\\Visualisation\\icons\\spg.png",
    "catapult": "work\\Visualisation\\icons\\catapult.png",
    "hard_repair": "work\\Visualisation\\icons\\hard_repair.png",
    "light_repair": "work\\Visualisation\\icons\\light_repair.png",
}


class Graphics(metaclass=Singleton):

    def __init__(self):
        self.__screen_width = 1280
        self.__screen_height = 720
        self.__hex_radius = self.__screen_height / Map().size / 3.5
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        self.__hex_cords = self.__get_hexes_coord()
        self.__tank_colors = None
        self.__font_size = int(self.__hex_radius * 2)

    @staticmethod
    def get_colors():
        color_dict = dict()
        for color_id, player in enumerate(GameState().players):
            color_dict[player["idx"]] = COLORS[color_id]
        return color_dict

    @staticmethod
    def get_all_map_indexes(map_size: int) -> []:
        """
        getting all hexagon indexes: [(10,0,-10),(10,-1,-9)...]
        """
        map_r = map_size - 1
        map_indexes_arr = []
        for x in range(-map_r, map_r + 1):
            for y in range(-map_r, map_r + 1):
                if fabs(x + y) <= map_r:
                    z = -(x + y)
                    map_indexes_arr.append((x, y, z))
        return map_indexes_arr

    @staticmethod
    def __hex_to_pixel(hex_index: tuple, radius: float, center):
        x = center + radius * (3 / 2 * hex_index[0])
        y = center + radius * (sqrt(3) / 2 * hex_index[0] + sqrt(3) * hex_index[1])
        return x, y

    def __get_hexes_coord(self) -> dict:
        """
        bind the hexagon indexes to the coordinates on the screen
        """
        center = self.__screen_height // 2

        map_indexes_arr = self.get_all_map_indexes(Map().size)
        hex_cords = dict()
        for index in map_indexes_arr:
            radius = self.__hex_radius
            hex_cords[index] = self.__hex_to_pixel(index, radius, center)
        return hex_cords

    def __draw_hex(self, color: tuple, width: int, radius: float, position: tuple):
        n, r = 6, radius
        x, y = position
        points = [
            (x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n))
            for i in range(n)
        ]
        pygame.draw.polygon(self.__screen, color, points, width)

    @staticmethod
    def __get_name(player_id: int) -> str:
        for pl in GameState().players:
            if player_id == pl["idx"]:
                return pl["name"]

    def __draw_empty_map(self):
        r = pygame.Rect(self.__screen_width * 0.57, 0, self.__screen_width * 0.43, self.__screen_height)
        pygame.draw.rect(self.__screen, (20, 30, 38), r)
        pygame.draw.line(self.__screen, THECOLORS['black'],
                         (self.__screen_width * 0.57, 0),
                         (self.__screen_width * 0.57, self.__screen_height),
                         int(self.__hex_radius))
        for value in self.__hex_cords.values():
            hex_r = self.__screen_height / Map().size / 3.5
            self.__draw_hex((242, 218, 145), 0, hex_r, value)
            self.__draw_hex(THECOLORS['black'], 3, hex_r, value)

    def __draw_obstacles(self):
        for obstacle in Map().obstacles:
            position = self.__hex_cords[(obstacle.x, obstacle.y, obstacle.z)]
            self.__draw_hex((20, 30, 38), 0, self.__hex_radius, position)
            self.__draw_hex(THECOLORS['black'], 3, self.__hex_radius, position)

    def __draw_base(self):
        for base_hex in Map().base:
            position = self.__hex_cords[(base_hex.x, base_hex.y, base_hex.z)]
            self.__draw_hex((154, 205, 50), 0, self.__hex_radius, position)
            self.__draw_hex(THECOLORS['black'], 3, self.__hex_radius, position)

    def __draw_catapult(self):
        for catapult in Map().catapult:
            pos_key = (catapult.x, catapult.y, catapult.z)
            position = self.__hex_cords[pos_key]
            catapult_surf = pygame.image.load(ICONS_PATH["catapult"])
            scale = pygame.transform.smoothscale(
                catapult_surf, (1.4 * self.__hex_radius,
                                1.4 * self.__hex_radius))
            catapult_rect = scale.get_rect(center=position)
            self.__screen.blit(scale, catapult_rect)

    def __draw_hard_repair(self):
        for hard_repair in Map().hard_repair:
            pos_key = (hard_repair.x, hard_repair.y, hard_repair.z)
            position = self.__hex_cords[pos_key]
            hard_repair_surf = pygame.image.load(ICONS_PATH["hard_repair"])
            scale = pygame.transform.smoothscale(
                hard_repair_surf, (1.4 * self.__hex_radius,
                                   1.4 * self.__hex_radius))
            hard_repair_rect = scale.get_rect(center=position)
            self.__screen.blit(scale, hard_repair_rect)

    def __draw_light_repair(self):
        for light_repair in Map().light_repair:
            pos_key = (light_repair.x, light_repair.y, light_repair.z)
            position = self.__hex_cords[pos_key]
            light_repair_surf = pygame.image.load(ICONS_PATH["light_repair"])
            scale = pygame.transform.smoothscale(
                light_repair_surf, (1.4 * self.__hex_radius,
                                    1.4 * self.__hex_radius))
            light_repair_rect = scale.get_rect(center=position)
            self.__screen.blit(scale, light_repair_rect)

    def __draw_tanks(self):
        font_hp = pygame.font.SysFont("calibri", int(self.__hex_radius), True)
        if GameState().current_player_idx:
            for tank in GameState().vehicles.values():
                owner_id = tank["player_id"]
                tank_type = tank["vehicle_type"]
                pos_key = (tuple(tank["position"].values()))
                position = self.__hex_cords[pos_key]
                color = self.__tank_colors[owner_id]
                self.__draw_hex(color, 0, self.__hex_radius, position)
                self.__draw_hex(THECOLORS['black'], 3, self.__hex_radius, position)
                tank_surf = pygame.image.load(ICONS_PATH[tank_type])
                scale = pygame.transform.smoothscale(
                    tank_surf, (1.5 * self.__hex_radius,
                                1.5 * self.__hex_radius))
                tank_rect = scale.get_rect(center=position)
                self.__screen.blit(scale, tank_rect)
                hp_str = font_hp.render(str(tank["health"]), True, (127, 255, 0))
                pos = (position[0] - self.__hex_radius * 0.7, position[1] - self.__hex_radius * 0.7)
                self.__screen.blit(hp_str, pos)
        else:
            for team_tanks in Map().spawn_points:
                for t_type, tank in team_tanks.items():
                    pos_key = (tuple(tank[0].values()))
                    position = self.__hex_cords[pos_key]
                    tank_surf = pygame.image.load(ICONS_PATH[t_type])
                    scale = pygame.transform.smoothscale(
                        tank_surf, (1.5 * self.__hex_radius,
                                    1.5 * self.__hex_radius))
                    tank_rect = scale.get_rect(center=position)
                    self.__screen.blit(scale, tank_rect)

    def __draw_turns(self):
        font = pygame.font.SysFont("calibri", int(self.__font_size * 1.5), False)
        turns_message = "TURN: %s/%s" % (GameState().current_turn, GameState().num_turns)
        text = font.render(turns_message, True, (242, 153, 75))
        pos = self.__screen_width * 205 / 300, self.__screen_height / 2 - self.__hex_radius * 1.5
        self.__screen.blit(text, pos)

    def __draw_players(self):
        font_b = pygame.font.SysFont("calibri", self.__font_size, False)
        font_l = pygame.font.SysFont("calibri", int(self.__font_size / 1.5), False)
        text = font_b.render("PLAYERS:", True, (242, 153, 75))
        position = self.__screen_width * 2 / 3, self.__screen_height / 15
        self.__screen.blit(text, position)
        for i, player in enumerate(GameState().players):
            player_message = "ID: %s   NAME: %s" % (player["idx"], player["name"])
            text = font_l.render(player_message, True, self.__tank_colors[player["idx"]])
            position = self.__screen_width * 1.9 / 3, self.__screen_height / 7.5 + self.__hex_radius * i * 1.2
            self.__screen.blit(text, position)

    def __draw_win_points(self):
        font_b = pygame.font.SysFont("calibri", self.__font_size, False)
        font_l = pygame.font.SysFont("calibri", int(self.__font_size / 1.5), False)
        text = font_b.render("WIN POINTS:", True, (242, 153, 75))
        position = self.__screen_width * 2 / 3, self.__screen_height * 3 / 4
        self.__screen.blit(text, position)
        position = self.__screen_width * 1.9 / 3, self.__screen_height * 3 / 4 + self.__hex_radius
        for xid, values in GameState().win_points.items():
            player_message = "ID: %s   capture: %s   kill: %s" % (xid, values["capture"], values["kill"])
            text = font_l.render(player_message, True, self.__tank_colors[int(xid)])
            position = self.__screen_width * 1.9 / 3, position[1] + self.__hex_radius * 1.2
            self.__screen.blit(text, position)

    def __draw_info(self):
        self.__draw_turns()
        self.__draw_players()
        self.__draw_win_points()

    def __draw_winner(self):
        if GameState().finished:
            winner_id = GameState().winner
            rect = pygame.Rect(
                (self.__screen_width * 0.2, self.__screen_height * 0, self.__screen_width * 0.6,
                 self.__screen_height * 0.2))
            pygame.draw.rect(self.__screen, (119, 148, 166), rect, 0)
            pygame.draw.rect(self.__screen, THECOLORS['black'], rect, 5)
            font = pygame.font.SysFont("calibri", self.__font_size * 2, True)
            win_message = "%s win!" % self.__get_name(winner_id)
            text = font.render(win_message, True, THECOLORS['black'])
            text_rect = text.get_rect(center=(self.__screen_width / 2, self.__screen_height / 10))
            self.__screen.blit(text, text_rect)

    def __draw_all(self):
        self.__screen.fill((37, 59, 89))
        self.__draw_empty_map()
        self.__draw_base()
        self.__draw_obstacles()
        self.__draw_catapult()
        self.__draw_hard_repair()
        self.__draw_light_repair()
        if GameState().current_player_idx and not self.__tank_colors:
            self.__tank_colors = self.get_colors()
        self.__draw_tanks()
        if GameState().current_player_idx:
            self.__draw_info()
            self.__draw_winner()

    def render(self):
        pygame.init()
        pygame.display.set_caption('World of Tanks: Strategy')
        pygame.display.set_icon(pygame.image.load("work\\Visualisation\\icons\\powerpuff_girls.png"))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.__draw_all()
            pygame.display.update()
