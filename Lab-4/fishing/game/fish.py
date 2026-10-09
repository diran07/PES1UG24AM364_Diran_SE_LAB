"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. The starter has one fish type; Task 2 adds more.
"""

import pygame


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10, color=(80, 180, 220)):
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )

FISH_TYPES = {
    "slow": {"speed": 2, "point_value": 10, "width": 40, "height": 20, "color": (80, 180, 220)},
    "fast": {"speed": 5, "point_value": 30, "width": 24, "height": 12, "color": (240, 200, 40)},
}


def make_fish(kind, x, y, direction=1):
    cfg = FISH_TYPES[kind]
    fish = Fish(
        x=x, y=y,
        speed=cfg["speed"] * direction,
        width=cfg["width"], height=cfg["height"],
        point_value=cfg["point_value"], color=cfg["color"],
    )
    fish.kind = kind
    return fish
