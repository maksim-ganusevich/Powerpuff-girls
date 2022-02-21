import pygame
import sys
from pygame.color import THECOLORS
from math import fabs, sin, pi, sqrt, cos
from work.config import base, obstacles, global_state

map_size = 11

COLORS = [(255, 153, 0), (204, 51, 204), (102, 153, 255)]
ICONS_PATH = {
    "at_spg": "work\\Visualisation\\icons\\at_spg.png",
    "heavy_tank": "work\\Visualisation\\icons\\heavy_tank.png",
    "light_tank": "work\\Visualisation\\icons\\light_tank.png",
    "medium_tank": "work\\Visualisation\\icons\\medium_tank.png",
    "spg": "work\\Visualisation\\icons\\spg.png",
}


class Graphics:

    def __init__(self):
        self.__screen_width = 1280
        self.__screen_height = 720
        self.__hex_radius = self.__screen_height / map_size / 3.5
        self.__obstacles = obstacles
        self.__base = base
        self.__map_size = map_size
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        self.__hex_cords = self.__get_hexes_coord()
        self.__tank_colors = None
        self.__font_size = int(self.__hex_radius * 2)

    @staticmethod
    def get_colors():
        color_dict = dict()
        for color_id, player in enumerate(global_state["players"]):
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

        map_indexes_arr = self.get_all_map_indexes(map_size)
        hex_cords = dict()
        for index in map_indexes_arr:
            hex_cords[index] = self.__hex_to_pixel(index, self.__hex_radius, center)
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
        for pl in global_state["players"]:
            if player_id == pl["idx"]:
                return pl["name"]

    def __draw_empty_map(self):
        r = pygame.Rect(self.__screen_width * 0.57, 0, self.__screen_width * 0.43, self.__screen_height)
        pygame.draw.rect(self.__screen, (37, 37, 36), r)
        pygame.draw.line(self.__screen, THECOLORS['black'],
                         (self.__screen_width * 0.57, 0),
                         (self.__screen_width * 0.57, self.__screen_height),
                         int(self.__hex_radius))
        for value in self.__hex_cords.values():
            hex_r = self.__screen_height / map_size / 3.5
            self.__draw_hex((255, 253, 83), 0, hex_r, value)
            self.__draw_hex(THECOLORS['black'], 3, hex_r, value)

    def __draw_obstacles(self):
        for obstacle in self.__obstacles:
            position = self.__hex_cords[(obstacle.x, obstacle.y, obstacle.z)]
            self.__draw_hex((51, 51, 51), 0, self.__hex_radius, position)
            self.__draw_hex(THECOLORS['black'], 3, self.__hex_radius, position)

    def __draw_base(self):
        for base_hex in self.__base:
            position = self.__hex_cords[(base_hex.x, base_hex.y, base_hex.z)]
            self.__draw_hex((154, 205, 50), 0, self.__hex_radius, position)
            self.__draw_hex(THECOLORS['black'], 3, self.__hex_radius, position)

    def draw_tanks(self):
        font_hp = pygame.font.SysFont("calibri", int(self.__hex_radius), True)
        for tank in global_state["vehicles"].values():
            owner_id = tank["player_id"]
            tank_type = tank["vehicle_type"]
            hp = tank["health"]
            pos_key = (tank["position"]["x"], tank["position"]["y"], tank["position"]["z"])
            position = self.__hex_cords[pos_key]
            color = self.__tank_colors[owner_id]
            self.__draw_hex(color, 0, self.__hex_radius, position)
            self.__draw_hex(THECOLORS['black'], 3, self.__hex_radius, position)
            tank_surf = pygame.image.load(ICONS_PATH[tank_type])
            scale = pygame.transform.scale(
                tank_surf, (1.5 * self.__hex_radius,
                            1.5 * self.__hex_radius))
            tank_rect = scale.get_rect(center=position)
            self.__screen.blit(scale, tank_rect)
            hp_str = font_hp.render(str(hp), False,
                                    THECOLORS["green"])
            self.__screen.blit(hp_str, (position[0] - self.__hex_radius * 0.7, position[1] - self.__hex_radius * 0.7))

    def __draw_turns(self):
        font = pygame.font.SysFont("calibri", int(self.__font_size * 1.5), True)
        turns_message = "TURN: %s/%s" % (global_state["current_turn"], global_state["num_turns"])
        text = font.render(turns_message, True, (102, 205, 170))
        position = self.__screen_width * 21 / 30, self.__screen_height / 2 - self.__hex_radius * 1.5
        self.__screen.blit(text, position)

    def __draw_players(self):
        font_b = pygame.font.SysFont("calibri", self.__font_size, True)
        font_l = pygame.font.SysFont("calibri", int(self.__font_size / 1.5), True)
        text = font_b.render("PLAYERS:", True, (102, 205, 170))
        position = self.__screen_width * 2 / 3, self.__screen_height / 15
        self.__screen.blit(text, position)
        for i, player in enumerate(global_state["players"]):
            player_message = "ID: %s   NAME: %s" % (player["idx"], player["name"])
            text = font_l.render(player_message, True, self.__tank_colors[player["idx"]])
            position = self.__screen_width * 1.9 / 3, self.__screen_height / 7.5 + self.__hex_radius * i * 1.2
            self.__screen.blit(text, position)

    def __draw_win_points(self):
        font_b = pygame.font.SysFont("calibri", self.__font_size, True)
        font_l = pygame.font.SysFont("calibri", int(self.__font_size / 1.5), True)
        text = font_b.render("WIN POINTS:", True, (102, 205, 170))
        position = self.__screen_width * 2 / 3, self.__screen_height * 3 / 4
        self.__screen.blit(text, position)
        position = self.__screen_width * 1.9 / 3, self.__screen_height * 3 / 4 + self.__hex_radius
        for id, values in global_state["win_points"].items():
            player_message = "ID: %s   capture: %s   kill: %s" % (id, values["capture"], values["kill"])
            text = font_l.render(player_message, True, self.__tank_colors[int(id)])
            position = self.__screen_width * 1.9 / 3, position[1] + self.__hex_radius * 1.2
            self.__screen.blit(text, position)

    def draw_info(self):
        self.__draw_turns()
        self.__draw_players()
        self.__draw_win_points()

    def __draw_winner(self):
        if global_state["finished"]:
            winner_id = global_state["winner"]
            rect = pygame.Rect(
                (self.__screen_width * 0.2, self.__screen_height * 0.3, self.__screen_width * 0.6, self.__screen_height * 0.4))
            pygame.draw.rect(self.__screen, self.__tank_colors[winner_id], rect, 0)
            pygame.draw.rect(self.__screen, THECOLORS['black'], rect, 5)
            font = pygame.font.SysFont("calibri", self.__font_size * 2, True)
            win_message = "%s win!" % self.__get_name(winner_id)
            text = font.render(win_message, True, THECOLORS['black'])
            text_rect = text.get_rect(center=(self.__screen_width / 2, self.__screen_height / 2))
            self.__screen.blit(text, text_rect)

    def __draw_all(self):
        self.__screen.fill((47, 79, 79))
        self.__draw_empty_map()
        self.__draw_base()
        self.__draw_obstacles()
        if global_state:
            if not self.__tank_colors:
                self.__tank_colors = self.get_colors()
            self.draw_tanks()
            self.draw_info()
            self.__draw_winner()

    def render(self):
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.__draw_all()
            pygame.display.update()



