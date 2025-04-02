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

names=["Cashier", "Teacher", "Student", "Worker"]
role_prompts=[open("Prompts/"+name+".txt").read().strip() for name in names]
agents=[Base_Agent(name, random.randint(1, 1280), random.randint(1, 720), role_prompt=role_prompts[i]) for i, name in enumerate(names)]

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
                if not agent.conversation[-1]:
                    agent.conversation="You notice a new person in front of you\n"
                    agents[agent.conversing].conversing=i
                    agents[agent.conversing].conversation.append("")
                if "end conv" in agent.conversation[-1].lower():
                    agents[agent.conversing].conversing=-1
                    agent.conversing=-1
                    agent.dialogue=Dialogue(agent)
                else:
                    response = agent.prompt()
                    agents[agent.conversing].conversation[-1]+=f"{agent.name}: "+response
                    agent.dialogue = Dialogue(agent, response)
                    if "end conv" in response.lower():
                        agents[agent.conversing].conversing=-1
                        agent.conversing=-1
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
                        if agent.should_converse(j):
                            agent.conversing=j
                            agent.conversation.append("")

    for i, agent in enumerate(agents):
        agent.update()
        agent.draw(screen)
        if not agent.dialogue.text_list or not agent.dialogue.text_list[0]:
            agent.dialogue = Dialogue(agent, agent.tasks)
        agent.dialogue.draw(screen)

    pygame.display.flip()
    dt = clock.tick(30) / 1000

pygame.quit()

