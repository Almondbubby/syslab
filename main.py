import pygame #type: ignore
from Agents.base_agent import Base_Agent
from Dialogue.Dialogue import Dialogue
import time
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
running = True
dt = 0

role_prompts=[open('Prompts/rishabh_role.txt').read(), open('Prompts/gabriel_role.txt').read(), open('Prompts/raymond_role.txt').read(), open('Prompts/deven_role.txt').read()]
agents=[Base_Agent(random.randint(1, 1280), random.randint(1, 720), role_prompt=x) for x in role_prompts]

start = time.time()
last1 = 0
last2 = 0

def distance(a, b):
    a=a.position
    b=b.position
    return (a[0]-b[0])**2+(a[1]-b[1])**2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill("white")

    if int(time.time()-start - last1) >= 2:
        last1=time.time()-start
        for i, agent in enumerate(agents):
            if agent.conversing!=-1:
                if not agent.response:
                    agent.response="Env there is a person in front of you, ask them what their name is"
                if "end conv" in agent.response.lower():
                    agents[agent.conversing].conversing=-1
                    agent.conversing=-1
                    agent.response=None
                    agent.dialogue=Dialogue(agent)
                else:
                    response = agent.prompt(agent.response.lower())
                    agent.conversation[-1] += response + '\n'
                    agents[agent.conversing].response=response
                    agent.dialogue = Dialogue(agent, response)
                    if "end conv" in response:
                        agents[agent.conversing].conversing=-1
                        agent.conversing=-1
                        agent.response=None
                        agent.dialogue=Dialogue(agent)
        
    if int(time.time() - last2) >= 2:
        last2=time.time()-start
        for i, agent in enumerate(agents):
            if agent.conversing==-1:
                r=random.randint(1, 4)
                if r==1: agent.move_left()
                elif r==2: agent.move_right()
                elif r==3: agent.move_up()
                elif r==4: agent.move_down()

                for j in range(len(agents)):
                    if i!=j and agents[j].conversing==-1:
                        if distance(agent, agents[j])<=100000 and distance(agent, agents[j])>=10000 and random.randint(1, 100)<=1:
                            agent.conversing=j
                            agent.conversation.append("")
                            agent.stop_moving()
                            agents[j].conversing=i
                            agents[j].conversation.append("")
                            agents[j].stop_moving()

    for i, agent in enumerate(agents):
        agent.update()
        agent.draw(screen)
        if not agent.dialogue.text_list or not agent.dialogue.text_list[0]:
            agent.dialogue = Dialogue(agent, agent.tasks)
        agent.dialogue.draw(screen)

    pygame.display.flip()
    dt = clock.tick(30) / 1000

pygame.quit()

