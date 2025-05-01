import pygame #type: ignore
from Agents.base_agent import Base_Agent
from Dialogue.Dialogue import Dialogue
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1400, 800))
clock = pygame.time.Clock()
running = True

names=["Cashier", "Teacher", "Student", "Worker"]
role_prompts=[open("Prompts/"+name+".txt").read().strip() for name in names]
agents=[Base_Agent(name, random.randint(400, 1000), random.randint(200, 600), tuple(random.randint(0, 255) for i in range(3)), role_prompt=role_prompts[i]) for i, name in enumerate(names)]

buildings=[tuple(random.randint(300, 700) for i in range(2)) for j in range(5)]
for x in agents:
    buildings.append(x.position)

counter=0
counter2=0
time=8*60

def draw_building(screen, x, y, size=100):
    wall_color = (120, 120, 120)
    wall_thickness = 4
    pygame.draw.rect(screen, wall_color, (x - size//2, y - size//2, size, size), wall_thickness)
    
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

    counter+=1
    if counter>=30:
        counter=0
        for i, agent in enumerate(agents):
            if agent.conversing!=-1:
                if not agent.conversation[-1]:
                    agent.conversation=["You notice a new person in front of you\n"]
                    agents[agent.conversing].conversing=i
                    agents[agent.conversing].conversation.append("")
                if "end conv" in agent.conversation[-1].lower():
                    agents[agent.conversing].end_convo(time)
                    agent.end_convo(time)
                    agent.dialogue=Dialogue(agent)
                else:
                    response = agent.prompt()
                    agents[agent.conversing].conversation[-1]+=f"{agent.name}: "+response
                    agent.dialogue = Dialogue(agent, response)
                    if "end conv" in response.lower():
                        agents[agent.conversing].end_convo(time)
                        agent.end_convo(time)
                        agent.dialogue=Dialogue(agent)
        
    counter2+=1
    if counter2>=20:
        counter2=0
        for i, agent in enumerate(agents):
            if agent.conversing==-1:
                agent.move_random()

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
    
    for x in buildings:
        start_x, start_y = x
        draw_building(screen, start_x, start_y)

    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Time: {time//60} hours and {time%60} minutes", True, (0, 0, 0))
    screen.blit(text_surface, (20, 20))
    pygame.display.flip()
    clock.tick(10)
    time+=1
    if time>=24*60:
        time=0

pygame.quit()

