import pygame # type: ignore
from Agents import base_agent

class Rishabh(base_agent.Base_Agent):
    def __init__(self, x, y, role_prompt, velocity_x=0, velocity_y=0, color=(255,0,0)):
        super().__init__(x, y, velocity_x, velocity_y, color, role_prompt)