import pygame # type: ignore
from ollama import chat # type: ignore
from ollama import ChatResponse # type: ignore
from Dialogue.Dialogue import Dialogue
import random

class Base_Agent(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x=0, velocity_y=0, color=(0,0,255), role_prompt=""):
        super().__init__()
        self.position = (x, y)
        self.velocity = (velocity_x, velocity_y)
        self.color = color
        self.role_prompt = role_prompt
        self.conversing = -1
        self.conversation = []
        self.response = None
        self.dialogue = Dialogue(self)
        self.movement_bound = 30

    def prompt(self, p):
        response: ChatResponse = chat(model='llama3.2', messages=[
        {'role': 'system', 'content': self.role_prompt},
        {'role': 'system', 'content': f"Conversation thus far: \n {self.conversation[-1]}"},
        {'role': 'user', 'content': p}
        ])
        print(self.conversing)
        print("Prompt:", p)
        print("Response:", response.message.content)
        print()
        return response.message.content

    def update(self):
        newx=self.position[0] + self.velocity[0]
        newy=self.position[1] + self.velocity[1]
        if newx<1 or newx>1280:
            newx=self.position[0]
            self.velocity=(0, self.velocity[1])
        if newy<1 or newy>720:
            newy=self.position[1]
            self.velocity=(self.velocity[0], 0)
        self.position=(newx,newy)
        self.stop_moving()
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, 10)

    def move_left(self):
        self.velocity = (-random.randint(1, self.movement_bound), self.velocity[1])
    
    def move_right(self):
        self.velocity = (random.randint(1, self.movement_bound), self.velocity[1])
    
    def move_up(self):
        self.velocity = (self.velocity[0], -random.randint(1, self.movement_bound))

    def move_down(self):
        self.velocity = (self.velocity[0], random.randint(1, self.movement_bound))

    def stop_moving(self):
        self.velocity = (0,0)