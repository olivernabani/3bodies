import pygame
import config

# Clase para representar los cuerpos celestes
class CelestialBody:
    def __init__(self, name, x, y, mass, radius, color):
        self.name = name
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.vx = 0
        self.vy = 0
        self.trail = []
    
    def is_over(self, pos):        
        if self.x - self.radius < pos[0] < self.x + self.radius and self.y - self.radius < pos[1] < self.y + self.radius:
            print('true')
            return True
        else:
            return False

    def draw(self, screen, zoom, diffx, diffy, width, tag):
        myx = int(self.x * zoom + (config.WIDTH/2)*(1-zoom) + diffx)
        myy = int(self.y * zoom + (config.HEIGHT/2)*(1-zoom) + diffy)
        myradius = int(self.radius * zoom)
        
        pygame.draw.circle(screen, self.color, (myx, myy), myradius, width)
        for point in self.trail:
            puntox = int(point[0]* zoom + (config.WIDTH/2)*(1-zoom) + diffx)
            puntoy = int(point[1]* zoom + (config.HEIGHT/2)*(1-zoom) + diffy)
            pygame.draw.circle(screen, self.color, (puntox, puntoy), 1)
            
        pygame.draw.aaline(screen, config.WHITE, (myx,myy),(myx+(self.vx*200),myy +(self.vy*200)))

        if tag:
            font = pygame.font.SysFont('Arial', 15)
            formatted_mass = "{:.2f}".format(self.mass)
            text = font.render(formatted_mass,True, config.WHITE)
            screen.blit(text,(self.x -50, self.y -50))
        
    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        if len(self.trail) > 8000:
            self.trail.pop(0)
        self.trail.append((self.x, self.y))