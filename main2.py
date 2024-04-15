import pygame
import sys
from render import Render
from enum import Enum

# Initialize Pygame
pygame.init()

# Screen settings and colors
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 155)
RED = (255, 50, 50)

class SimulationState(Enum): # Enum for the simulation state
    CREATION = 1
    EDIT = 2
    RUNNING = 3

def main():
    clock = pygame.time.Clock()
    simulation = Render()
    print('Hemos llegado a main()')
    while True:
        for event in pygame.event.get(): # Event loop
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle events depending on the simulation state    
            if simulation.state == SimulationState.CREATION.value:
                simulation.handle_creation_events(event)
            elif simulation.state == SimulationState.EDIT.value:            
                simulation.handle_edit_events(event)
            elif simulation.state == SimulationState.RUNNING.value:           
                simulation.handle_simulation_events(event)

        screen.fill(BLACK)       

        if simulation.state == SimulationState.CREATION.value:           
            simulation.render_creation_menu(screen)
        elif simulation.state == SimulationState.EDIT.value:
            simulation.render_edit_menu(screen)
        elif simulation.state == SimulationState.RUNNING.value:
            if simulation.is_active:
                simulation.update()
            simulation.render_simulation(screen)

        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    main()