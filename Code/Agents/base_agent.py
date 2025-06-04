import pygame # type: ignore
from ollama import chat # type: ignore
from ollama import ChatResponse # type: ignore
from Dialogue.Dialogue import Dialogue
import random

instructions='''You are given prompts consisting of conversations between you and other people. Repond to these prompts with your own response. When you wish to end the conversation, end the response with "end conv".
Remember to converse like a human. Your responses should flow from the previous ones.
Keep the responses under 30 words.'''

class Base_Agent(pygame.sprite.Sprite):
    def __init__(self, name, x, y, color=(0,0,255), role_prompt=""):
        super().__init__()
        self.name = name
        self.position = (x, y)
        self.color = color
        self.role_prompt = role_prompt
        self.conversing = -1
        self.conversation = []
        self.dialogue = Dialogue(self)
        self.movement_bound = 5
        self.history = []
        self.tasks = [(8, "Wake up"), (9, "Eat breakfast"), (10, "Go to school/work"), (5, "Go home"), (11, "Go to sleep")]
        self.tasks = ', '.join(':'.join(map(str, x)) for x in self.tasks)

    def prompt(self, prompt=""):
        print("Name:", self.name)
        print("Conversing Status:", self.conversing)
        a=[{'role': 'system', 'content': (prompt if prompt else self.role_prompt)+instructions}]
        if self.conversation:
            prompt=f"{self.conversation[-1]}"
            a.append({'role': 'user', 'content': prompt})
        print("Prompt:", prompt)
        response = chat(model='llama3.2', messages=a)
        print("Response:", response.message.content)
        print()
        self.conversation[-1]+="Me: "+response.message.content+"\n"
        return response.message.content
    
    def end_convo(self, time):
        self.history.append((time, self.conversing))
        self.conversing=-1

    def should_converse(self, j):
        if self.conversing!=-1: return False
        if self.history.count(j)<1: return True
        return False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, 10)

    def move_random(self):
        r=random.randint(1, 4)
        if r==1: self.move_left()
        elif r==2: self.move_right()
        elif r==3: self.move_up()
        elif r==4: self.move_down()

    def move_left(self):
        self.position = (self.position[0]-random.randint(1, self.movement_bound), self.position[1])
    
    def move_right(self):
        self.position = (self.position[0]+random.randint(1, self.movement_bound), self.position[1])
    
    def move_up(self):
        self.position = (self.position[0], self.position[0]-random.randint(1, self.movement_bound))

    def move_down(self):
        self.position = (self.position[0], self.position[0]+random.randint(1, self.movement_bound))