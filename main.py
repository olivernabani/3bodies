import pygame
import sys
from math import sqrt, pow
from buttons import Button
from bodies import CelestialBody
from physics import Physics
import config
import random
import copy

# Inicializar Pygame
pygame.init()

# Constantes de la pantalla
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0,0,155)
RED = (255, 50, 50)

bodies = []
indice_user = 0


def add_body(pos,mass,color): #Add a new body to the simulation
    global bodies, indice_user
    name = 'User' + str(indice_user)
    indice_user += 1
    size = mass * 10
    body = CelestialBody(name,pos[0],pos[1],mass,size,color)
    bodies.append(body)
    return body

def demo():
    global bodies
    # Cuerpos celestes: posiciones iniciales, masas, etc.
    sun1 = CelestialBody('sun1',WIDTH // 3.2, HEIGHT // 2, 3.2, 30, YELLOW)
    sun2 = CelestialBody('sun2',WIDTH // 2, HEIGHT // 4 , 2.75, 30, YELLOW)
    sun3 = CelestialBody('sun3',WIDTH * 3 // 4, HEIGHT // 2, 3, 30, YELLOW)    
    earth = CelestialBody('earth',WIDTH // 3.2 - 150, HEIGHT // 2, 0.01, 10, WHITE)
    
    sun1.vy = 0.4
    sun1.vx = 0.4
    sun3.vx = -0.6
    sun2.vy =-0.3
    earth.vy = 3
    
    # Añadir más cuerpos según sea necesario
    bodies.append(sun1)
    bodies.append(sun2)
    bodies.append(sun3)
    bodies.append(earth)
    
    for body in bodies:
        body.draw(screen, 1, 0, 0,0,False)
        

    

# Main program
def main():
    # Variables de control
    global bodies    
    clock = pygame.time.Clock()   

    working, creation = True, True #First Menu
    edition, running, simulation_active = False, False, False #Menu States
    drag, create, vector, delete, instruction, start_timer = False, False, False, False, False, False #Action States
    diffx, diffy, deltax, deltay = 0,0,0,0 #On screen modifiers
    zoom = 1    
    move_body=''
    indication=''
    oldpos = pygame.mouse.get_pos()
    
    img_create = pygame.image.load('create.png')
    img_edit = pygame.image.load('edit.png')
    font = pygame.font.SysFont('Arial', 25)
    font2 = pygame.font.Font(None, 74)
    
    
    
    while working: #Main Loop
        working = False # By default on loop
        #Button Generation
        buttons = []
        for i in range(4):
            wid = 100
            xbut = 0 + wid * i
            buttons.append(Button(xbut, 0, wid, 40, 'Sim'))
            print(f'Creado botón [{i}] con x en {xbut}')
        
        #Buttons for Creation Menu
        tags = config.tags
        for i, button in enumerate(buttons):
            if i < len(tags):
                button.text = tags[i]    
        
        
        while creation: #Menu to create bodies
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Exit
                    creation = False
                    edition = False
                    running = False
                if event.type == pygame.KEYDOWN: # 
                    if event.key == pygame.K_DELETE: # Delete a body
                        delete = True
                        instruction = True
                        indication = 'Click over the body to delete'
                    if event.key == pygame.K_a: # Add a new body
                        create = True
                        instruction = True
                        indication = 'Click where you want to create a body'
                if event.type == pygame.MOUSEBUTTONDOWN: # Mouse Click
                    if create: #Add a new body
                        new = add_body(pos,2.5,WHITE)
                        new.draw(screen,1,0,0,0,False)                    
                        create = not create
                        instruction = False
                    if delete: # Delete a body
                        for body in bodies:
                            if body.is_over(pos):
                                bodies.remove(body)
                                delete = False
                                instruction = False
                    if buttons[2].is_over(pos): # Allow add a new body
                        create = True 
                        print("Añáde un Cuerpo")
                    if buttons[0].is_over(pos): # GO to Simulation Screen
                        creation = False
                        running = True
                    if buttons[3].is_over(pos): # GO to edition Screen
                        creation = False
                        edition = True
                    if buttons[1].is_over(pos): # Add demo bodies
                        demo()
                    for body in bodies: # Allow body movement
                        if body.is_over(pos):
                            drag = True
                            move_body = body.name
                if event.type == pygame.MOUSEBUTTONUP: # Stop body movement
                    drag = False
                    move_body = ''          
            
            # Draw Creation Menu Screen
            screen.fill(BLACK)
            for i in range(4):
                buttons[i].draw(screen, (0, 0, 0))
                    
            # Draw Bodies
            for body in bodies:
                if drag:
                    if body.name == move_body:
                        body.x = pos[0]
                        body.y = pos[1]
                        
                body.draw(screen,1,0,0,0,False)
                
            # Draw Instructions
            screen.blit(img_create,(0,HEIGHT-100))
            if instruction:            
                inst = font.render(indication,True, WHITE)
                screen.blit(inst,(50, HEIGHT -150))
            # Present on screen
            pygame.display.flip()
            clock.tick(60)
        
        # Menu for Edition
        # Description: Allow to modify the bodies properties and initial conditions
        
        # Buttons for edit menu
        tags = ['Sim','Back','None','None']
        for i, button in enumerate(buttons):
            if i < len(tags):
                button.text = tags[i]
        
        while edition: # Edit Menu for bodies
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Exit
                    edition = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN: # Mouse Click
                    print(pos)
                    for body in bodies: # Allow body movement
                        if body.is_over(pos):
                            move_body = body.name
                            vector = True
                    if buttons[0].is_over(pos): # GO to Simulation Screen
                        edition = False
                        running = True
                    if buttons[1].is_over(pos): # GO to Creation Screen
                        edition = False
                        running = False
                        working = True
                        creation = True
                if event.type == pygame.MOUSEBUTTONUP: # Stop body movement
                    vector = False
                    move_body=''
                if event.type == pygame.MOUSEWHEEL: # Modify body mass
                    for body in bodies:
                        if body.is_over(pos):
                            move_body = body.name
                            if event.y > 0:
                                body.mass += 0.05
                            elif event.y < 0:
                                body.mass -= 0.05        
                
            screen.fill(BLACK)
            
            for i in range(2): # Draw Buttons
                buttons[i].draw(screen, (0, 0, 0))
            # Dibujar los cuerpos celestes
            for body in bodies: # Draw Bodies
                if vector:
                    if body.name == move_body:
                        deltax = pos[0]-body.x
                        deltay = pos[1]-body.y
                        body.vx = deltax/50
                        body.vy = deltay/50
                        
                body.draw(screen, 1, 0 , 0,5,True)
            screen.blit(img_edit,(50,HEIGHT-100))
            pygame.display.flip()
            clock.tick(60)
        
        # Simulation Screen        
        # Buttons for sim menu
        tags = ['Start/Stop','Reset','Back','None']
        for i, button in enumerate(buttons):# Draw Buttons
            if i < len(tags):
                button.text = tags[i]
        
        backup = copy.deepcopy(bodies)
        back_visible = True
        counter = 0
        print(backup)
        while running:
            pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pygame.image.save(screen, "captura_de_pantalla.png")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0].is_over(pos):
                        simulation_active = not simulation_active
                        back_visible = False
                        start_timer = not start_timer
                    if buttons[1].is_over(pos):
                        simulation_active = False
                        bodies.clear()
                        bodies = copy.deepcopy(backup)
                        print(bodies)
                        back_visible = True
                        start_timer = False
                        counter = 0
                        zoom = 1
                    if buttons[2].is_over(pos) and back_visible:
                        edition = False
                        running = False
                        working = True
                        creation = True
                    drag = True                            
                if event.type == pygame.MOUSEBUTTONUP:
                    drag = False
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        zoom = zoom * 1.1
                    elif event.y < 0:
                        zoom = zoom * 0.9
            if drag:
                diffx += pos[0] - oldpos[0]
                diffy += pos[1] - oldpos[1]            
                
            oldpos = pos    
            
            screen.fill(BLACK)
            
            buttons[0].draw(screen, (0, 0, 0))
            buttons[1].draw(screen, (0, 0, 0))
            if back_visible:
                buttons[2].draw(screen, (0, 0, 0))
            
            for body in bodies:
                body.draw(screen, zoom, diffx, diffy,0,False)
                
            counter_surf = font2.render(f"{int(counter)}:{int((counter*10) % 10)}", True, RED)
            screen.blit(counter_surf, (WIDTH - 150, 10))           
                        
            if simulation_active:
            # Limpiar las fuerzas actuales (si las hubiera)
                for body in bodies:
                    body.force_x, body.force_y = 0, 0
                
                # Calcular la fuerza gravitacional entre todos los pares de cuerpos
                for i, body1 in enumerate(bodies):
                    for j, body2 in enumerate(bodies[i+1:], i+1):
                        print(body1)
                        print(body2)
                        force_x, force_y = Physics.calculate_gravitational_force(body1, body2)
                        body1.vx += force_x / body1.mass
                        body1.vy += force_y / body1.mass
                        body2.vx -= force_x / body2.mass  # La fuerza en la dirección opuesta para el otro cuerpo
                        body2.vy -= force_y / body2.mass

                # Actualizar las posiciones de los cuerpos celestes
                for body in bodies:
                    body.update_position()

                if start_timer:
                    counter += clock.get_time() / 1000.0
                
                screen.fill(BLACK)
                buttons[0].draw(screen, (0, 0, 0))
                buttons[1].draw(screen, (0, 0, 0))
                if back_visible:
                    buttons[2].draw(screen, (0, 0, 0))
            
                # Dibujar los cuerpos celestes
                for body in bodies:
                    body.draw(screen, zoom, diffx , diffy, 0, False)
                
                counter_surf = font2.render(f"{int(counter)}:{int((counter*10) % 10)}", True, RED)
                screen.blit(counter_surf, (WIDTH - 150, 10))
                
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
