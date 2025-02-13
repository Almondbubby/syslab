import pygame # type: ignore
from ollama import chat # type: ignore
from ollama import ChatResponse # type: ignore

class Base_Agent(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_x, velocity_y, color, role_prompt):
        super().__init__()
        self.position = (x, y)
        self.velocity = (velocity_x, velocity_y)
        self.color = color
        self.role_prompt = role_prompt 

    def prompt(self, p, conversation):
        response: ChatResponse = chat(model='llama3.2', messages=[
        {'role': 'system', 'content': self.role_prompt},
        {'role': 'system', 'content': f"Here is your conversation thus far: \n {conversation}"},
        {'role': 'user', 'content': p}
        ])
        print(self)
        print(response.message.content)
        return response.message.content

    def update(self):
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, 10)

    def move_left(self):
        self.velocity = (-1, self.velocity[1])
    
    def move_right(self):
        self.velocity = (1, self.velocity[1])
    
    def move_up(self):
        self.velocity = (self.velocity[0], -1)

    def move_down(self):
        self.velocity = (self.velocity[0], 1)