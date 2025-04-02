import pygame # type: ignore
from ollama import chat # type: ignore
from ollama import ChatResponse # type: ignore
from Dialogue.Dialogue import Dialogue
import random

instructions='''You are given prompts consisting of conversations between you and other people. Repond to these prompts with your own response. When you wish to end the conversation, end the response with "end conv".
Remember to converse like a human. Your responses should flow from the previous ones.
Keep the responses under 30 words.'''

class Base_Agent(pygame.sprite.Sprite):
    def __init__(self, name, x, y, velocity_x=0, velocity_y=0, color=(0,0,255), role_prompt=""):
        super().__init__()
        self.name = name
        self.position = (x, y)
        self.velocity = (velocity_x, velocity_y)
        self.color = color
        self.role_prompt = role_prompt
        self.conversing = -1
        self.conversation = []
        self.dialogue = Dialogue(self)
        self.movement_bound = 30
        self.tasks = self.prompt("Give a list of tasks for me to do throughout the day")

    def prompt(self):
        a=[{'role': 'system', 'content': self.role_prompt+instructions}]
        prompt=f"{self.conversation[-1]}"
        a.append({'role': 'user', 'content': prompt})
        response = chat(model='llama3.2', messages=a)

        print("Name:", self.name)
        print("Conversing Status:", self.conversing)
        print("Prompt:", prompt)
        print("Response:", response.message.content)
        print()
        self.conversation[-1]+="Me: "+response.message.content+"\n"
        return response.message.content
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, 10)

    def move_left(self):
        self.position = (self.position[0]-random.randint(1, self.movement_bound), self.position[1])
    
    def move_right(self):
        self.position = (self.position[0]+random.randint(1, self.movement_bound), self.position[1])
    
    def move_up(self):
        self.position = (self.position[0], self.position[0]-random.randint(1, self.movement_bound))

    def move_down(self):
        self.position = (self.position[0], self.position[0]+random.randint(1, self.movement_bound))