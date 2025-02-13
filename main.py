import pygame #type: ignore
from Agents.rishabh import Rishabh
from Agents.gabriel import Gabriel
from Dialogue.Dialogue import Dialogue
import time


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

rrole_prompt = ''
with open('Prompts/rishabh_role.txt', 'r') as file:
    rrole_prompt = file.read()

rishabh = Rishabh(100, 100, role_prompt = rrole_prompt)


grole_prompt = ''
with open('Prompts/gabriel_role.txt', 'r') as file:
    grole_prompt = file.read()

gabriel = Gabriel(500, 100, role_prompt = grole_prompt)

converse = True
start = time.time()

conversation = ''
rresponse = rishabh.prompt("Env Your friend Gabriel is in front of you", conversation)
conversation += rresponse + '\n'

rdialogue = Dialogue(rishabh, '')
gdialogue = Dialogue(gabriel, '')
rdialogue = Dialogue(rishabh, rresponse)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill("white")

    gresponse = ''
    if converse and int(time.time() - start) % 10 == 0:
        gresponse = gabriel.prompt(rresponse, conversation)
        conversation += gresponse + '\n'
        gdialogue = Dialogue(gabriel, gresponse)
        if "end conv" in gresponse:
            converse = False
        rresponse = rishabh.prompt(gresponse, conversation)
        conversation += rresponse + '\n'
        rdialogue = Dialogue(rishabh, rresponse)
        if "end conv" in rresponse:
            converse = False
        print(converse)
        print('\nbang')


    rishabh.update()
    rishabh.draw(screen)
    rdialogue.draw(screen)
    rresponse = ''

    gabriel.update()
    gabriel.draw(screen)
    gdialogue.draw(screen)
    gresponse = ''




    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

