import pygame
import sys


class NyanCat:
    def __init__(self):
        self.particles = []
        self.size = 12
        self.cat_size = (1185 // 7, 741 // 7)
        self.sprites = [
            pygame.transform.scale(pygame.image.load(f'sprites/cat{num}.png').convert_alpha(), self.cat_size) for num in
            ['1', '2', '3', '4']]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.jump = False

    def emit(self, speed=1):
        if self.particles:
            self.del_rainbow()
            for particle in self.particles:
                particle[0].x -= speed
                pygame.draw.rect(screen, particle[1], particle[0])

        self.draw_nyancat()

    def rainbow(self, offset, color):
        pos_x = pygame.mouse.get_pos()[0]
        pos_y = pygame.mouse.get_pos()[1] + offset
        particle_rect = pygame.Rect(int(pos_x - self.size / 2), int(pos_y - self.size / 2), self.size, self.size)
        self.particles.append((particle_rect, color))

    def del_rainbow(self):
        particle_copy = [particle for particle in self.particles if particle[0].x > 0]
        self.particles = particle_copy

    def draw_nyancat(self, speed=0.25):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
        mouse_pos = pygame.mouse.get_pos()
        if int(self.current_sprite) in range(2, 3):
            mouse_pos = (mouse_pos[0], mouse_pos[1] + 5)
            self.jump = True
        else:
            self.jump = False
        cat_rect = self.sprites[int(self.current_sprite)].get_rect(center=mouse_pos)
        screen.blit(self.sprites[int(self.current_sprite)], cat_rect)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('NyanCat Simulator')
    clock = pygame.time.Clock()
    nyan_cat = NyanCat()

    PARTICLE_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(PARTICLE_EVENT, 40)

    rainbow = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']
    offset = [-30, -18, -6, 6, 18, 30]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == PARTICLE_EVENT:
                for o, c in list(zip(offset, rainbow)):
                    if nyan_cat.jump:
                        nyan_cat.rainbow(o, pygame.Color(c))
                    else:
                        nyan_cat.rainbow(o + 1, pygame.Color(c))

        screen.fill((30, 30, 30))
        nyan_cat.emit()
        pygame.display.update()
        clock.tick(120)
