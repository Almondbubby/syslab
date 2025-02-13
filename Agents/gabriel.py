import pygame # type: ignore
from Agents import base_agent

class Gabriel(base_agent.Base_Agent):
    def __init__(self, x, y, role_prompt, velocity_x=0, velocity_y=0, color=(0,0,255)):
        super().__init__(x, y, velocity_x, velocity_y, color, role_prompt)