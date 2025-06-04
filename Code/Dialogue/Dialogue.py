import pygame # type: ignore

class Dialogue(pygame.sprite.Sprite):
    def __init__(self, agent, text='', outline_color=(0,0,0), width=0, height=0):
        super().__init__()
        self.position = (agent.position[0], agent.position[1] - height)
        self.outline_color = outline_color
        text_list = []
        if width == 0:
            width = len(text) * 10
        if height == 0:
            height = 50
        if width > 200:
            height = (width // 200) * 10 + 50
            width = 200
            for t in text.strip().split('\n'):
                for i in range(0, len(t), 30):
                    text_list.append(t[i:i+30])
        if text_list == []:
            text_list.append(text)
        self.width = width
        self.height = height
        self.text_list = text_list

    def draw(self, surface):
        pygame.draw.rect(surface, (255,255,255), (self.position[0], self.position[1], self.width, self.height))
        pygame.draw.rect(surface, self.outline_color, (self.position[0], self.position[1], self.width, self.height), 3)
        font = pygame.font.Font('freesansbold.ttf', 12)
        for i in range(len(self.text_list)):
            text = self.text_list[i]
            displayed_text = font.render(text, True, (0,0,0))
            textRect = displayed_text.get_rect()
            textRect.center = (self.position[0] + self.width//2, self.position[1] + 30 + (i * 15))
            surface.blit(displayed_text, textRect)