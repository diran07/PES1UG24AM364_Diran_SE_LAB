"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic, including the 30-second round timer.
"""

import math
import random

import pygame

from game.hook import Hook, IDLE
from game.fish import make_fish
from game.catch import check_catch
from game import renderer
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_SECONDS = 30


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            make_fish("slow", x=100, y=180),
            make_fish("fast", x=550, y=230, direction=-1),
            make_fish("slow", x=400, y=280, direction=-1),
            make_fish("fast", x=250, y=340),
            make_fish("slow", x=250, y=400),
        ]
        self.hooked_fish = None
        self.score = 0
        self.round_start = pygame.time.get_ticks()
        self.game_over = False

    def restart(self):
        if self.game_over:
            self.reset()

    def time_left(self):
        elapsed = (pygame.time.get_ticks() - self.round_start) / 1000
        return max(0.0, ROUND_SECONDS - elapsed)

    def cast(self):
        if not self.game_over:
            self.hook.start_cast()

    def update(self):
        if self.game_over:
            return
        if self.time_left() <= 0:
            self.game_over = True
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                kind = self.hooked_fish.kind
                self.hooked_fish = None
                self.fish_list.append(make_fish(kind, x=-40, y=random.randint(150, 420)))
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {math.ceil(self.time_left())}", (WIDTH - 110, 10))

        if self.game_over:
            renderer.draw_banner(surface, font, f"Time's up! Final score: {self.score}")
            msg = "Press R to play again"
            w = font.size(msg)[0]
            renderer.draw_text(surface, font, msg, ((WIDTH - w) // 2, HEIGHT // 2 + 30))