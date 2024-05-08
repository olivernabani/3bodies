# Render class definition
# This class is responsible for rendering the simulation and handling the events
# by Oliver Nabani, 2024

import pygame
from buttons import Button
from bodies import CelestialBody
from physics import Physics
import copy

# Constantes de la pantalla
WIDTH, HEIGHT = 1920, 1080

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 155)
RED = (255, 50, 50)

class Render:
    def __init__(self):
        # Pygame initialization
        self.clock = pygame.time.Clock()
        self.bodies = [] # List of CelestialBody objects
        self.backup = [] # List of CelestialBody objects
        
        #Flags
        self.state = 1  # SimulationState.CREATION, initial state
        self.is_active = False # Flag to start/stop the simulation
        self.create_mode = False # Flag to create a body
        self.delete_mode = False # Flag to delete a body        
        self.dragging = False # Flag to indicate if a body is being dragged
        self.vector = False # Flag to indicate if the velocity vector edition is being displayed
        self.start_timer = False # Flag to start the timer
        self.give_color = False # Flag to give color to the bodies
        
        # Slected objects
        self.selected_body = None # Reference to the body being edited
        self.drag_body = None # Reference to the body being dragged
        
        # Simulation parameters
        self.zoom = 1 # Zoom level
        self.pan = [0, 0] # Pan position
        self.counter = 0 # Counter for the elapsed time
        self.temporal_pos = [0, 0]
        self.elapsed_time = 0 # Elapsed time in seconds, when the simulation is running
        
        # Create the buttons
        self.create_buttons() # Create the buttons
        
        # Screen additional elements
        self.img_create = pygame.image.load('assets/create.png')
        self.img_edit = pygame.image.load('assets/edit.png')        
        self.font = pygame.font.SysFont('Arial', 25)
        self.font2 = pygame.font.Font(None, 74)

    def create_buttons(self): # Definition of the buttons
        # Control buttons
        self.create_button = Button(0, 0, 100, 40, "Create")
        self.delete_button = Button(100, 0, 100, 40, "Delete")
        self.demo_button = Button(200, 0, 100, 40, "Demo")
        self.edit_button = Button(300, 0, 100, 40, "Edit")
        self.run_button = Button(400, 0, 100, 40, "Run")
        self.run_button2 = Button(0, 0, 100, 40, "Run")
        self.start_stop_button = Button(0, 0, 100, 40, "Start/Stop")
        self.reset_button = Button(150, 0, 100, 40, "Reset")
        self.back_button = Button(0, 40, 100, 40, "<-Back")
        
        # Arrays of menu buttons
        self.creation_buttons =[self.create_button, self.delete_button, self.demo_button, self.edit_button, self.run_button]
        self.edition_buttons = [self.run_button2, self.back_button]
        self.simulation_buttons = [self.start_stop_button, self.reset_button, self.back_button] 
        
        # Color buttons
        self.rojo = Button(0, 0, 30, 30, "")
        self.rojo.color = RED
        self.azul = Button(0, 30, 30, 30, "")
        self.azul.color = BLUE
        self.amarillo = Button(0, 60, 30, 30, "")
        self.amarillo.color = YELLOW
        self.blanco = Button(0, 90, 30, 30, "")
        self.blanco.color = WHITE
        self.color_buttons = [self.rojo, self.azul, self.amarillo, self.blanco]
        
    def color_selector(self,pos): # Position the color buttons, when a body is selected
        self.rojo.x = pos[0]
        self.rojo.y = pos[1]
        self.azul.x = pos[0]
        self.azul.y = pos[1] + 30
        self.amarillo.x = pos[0]
        self.amarillo.y = pos[1] + 60
        self.blanco.x = pos[0]
        self.blanco.y = pos[1] + 90
        
    def create_body(self, pos): # Create a body with default parameters
        mass = 2.5
        color = WHITE
        name = f"User{len(self.bodies)}"
        size = mass * 10
        body = CelestialBody(name, pos[0], pos[1], mass, size, color)
        self.bodies.append(body)

    def delete_body(self, pos): # Delete a body
        for body in self.bodies:
            if body.is_over(pos):
                self.bodies.remove(body)
                break

    def load_demo(self): # Demo with some configured bodies that provides a interesting simulation
        self.bodies.clear()
        sun1 = CelestialBody("Sun1", WIDTH // 3.2, HEIGHT // 2, 3.2, 30, YELLOW)
        sun2 = CelestialBody("Sun2", WIDTH // 2, HEIGHT // 4, 2.75, 30, YELLOW)
        sun3 = CelestialBody("Sun3", WIDTH * 3 // 4, HEIGHT // 2, 3, 30, YELLOW)
        earth = CelestialBody("Earth", WIDTH // 3.2 - 150, HEIGHT // 2, 0.01, 10, WHITE)
        sun1.vy = 0.4
        sun1.vx = 0.4
        sun3.vx = -0.6
        sun2.vy = -0.3
        earth.vy = 3
        self.bodies.extend([sun1, sun2, sun3, earth])

    def update(self): # Apply the physics to the bodies
        for body in self.bodies: #Clear the forces
            body.force_x, body.force_y = 0, 0
        for i, body1 in enumerate(self.bodies):
            for body2 in self.bodies[i + 1 :]:
                force_x, force_y = Physics.calculate_gravitational_force(body1, body2)
                body1.vx += force_x / body1.mass
                body1.vy += force_y / body1.mass
                body2.vx -= force_x / body2.mass
                body2.vy -= force_y / body2.mass
        for body in self.bodies:
            body.update_position()
        self.elapsed_time += 1 / 60  # Assuming 60 FPS

    def reset(self): # Reset the simulation
        self.is_active = False # Stop the simulation
        self.elapsed_time = 0 # Reset the elapsed time
        
        # Restore the initial state of the bodies
        self.bodies.clear()
        self.bodies = copy.deepcopy(self.backup)

    def adjust_zoom(self, amount): # Adjust the zoom level
        self.zoom *= 1.1 if amount > 0 else 0.9

    def pan_view(self, rel): # Pan the view
        self.pan[0] += rel[0]
        self.pan[1] += rel[1]

    def draw_text(self,surface, text, color, pos=(0, 0)):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)
    
    
    # The following methods handle the events and render the different states of the simulation
    
    # ====================================================================================
    #
    #   Creation Menu
    #
    # ====================================================================================
    
    def handle_creation_events(self, event):
        pos = pygame.mouse.get_pos()
       
        # Left mouse button pressed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            # Check if the buttons are pressed
            if self.create_button.is_over(pos):
                self.create_mode = True
            elif self.delete_button.is_over(pos):
                self.delete_mode = True
            elif self.demo_button.is_over(pos):
                self.load_demo()
            elif self.edit_button.is_over(pos):
                self.state = 2  # SimulationState.EDIT
            elif self.run_button.is_over(pos):
                self.state = 3
            else:
                # Check if a body is clicked
                if self.create_body and self.create_mode:
                    self.create_body(pos)
                    self.create_mode = False
                elif self.delete_mode:
                    self.delete_body(pos)
                    self.delete_mode = False
                for body in self.bodies:
                    if body.is_over(pos):
                        self.drag_body = body
                        print(body.name)
                        self.dragging = True
                        
        # Mouse button released
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag_body = None
            self.dragging = False
            self.give_color = False
            for button in self.color_buttons: #Change the color of the body
                if button.is_over(pos):
                    print(self.selected_body)
                    self.selected_body.color = button.color  
                    
        # Right mouse button pressed     
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            for body in self.bodies:
                if body.is_over(pos):
                    self.selected_body = body                    
                    self.color_selector(pos)
                    self.give_color = True
        # Mouse movement          
        elif event.type == pygame.MOUSEMOTION:
            if self.drag_body and self.dragging:
                self.drag_body.x = pos[0]
                self.drag_body.y = pos[1]        
    
    # Render the creation menu
    def render_creation_menu(self, screen):        
        for button in self.creation_buttons:
            button.draw(screen)
        
        
        for body in self.bodies:
            body.draw(screen,1,0,0,0,False)
        if self.give_color:
            for button in self.color_buttons:
                button.draw(screen)
        screen.blit(self.img_create, (0, HEIGHT - 100))
        if self.create_mode:    
            self.draw_text(screen, "Click where you want to create a body", WHITE, (40, 920))
        elif self.delete_mode:
            self.draw_text(screen, "Click on the body to delete", WHITE, (40, 920))

    # ====================================================================================
    #
    #   Edit Menu
    #
    # ====================================================================================

    def handle_edit_events(self, event):
        pos = pygame.mouse.get_pos()
        self.temporal_pos = pos
        if event.type == pygame.MOUSEBUTTONDOWN:            
            if self.run_button2.is_over(pos):
                self.state = 3  # SimulationState.RUNNING
                self.backup = copy.deepcopy(self.bodies)
            elif self.back_button.is_over(pos):
                self.state = 1  # SimulationState.CREATION
            else:
                for body in self.bodies:
                    if body.is_over(pos):
                        self.selected_body = body
                        self.vector = True
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_body = None
            self.vector = False
        elif event.type == pygame.MOUSEWHEEL:
            for body in self.bodies:
                if body.is_over(pos):
                    body.mass += 0.05 if event.y > 0 else -0.05
                    body.radius = max(body.mass * 10,10)

    def render_edit_menu(self, screen):
        for button in self.edition_buttons:
            button.draw(screen)
        for body in self.bodies:
            if self.vector: # Draw the velocity vector
                if body.name == self.selected_body.name:
                    pos = (body.x, body.y)
                    deltax = self.temporal_pos[0] - pos[0]
                    deltay = self.temporal_pos[1] - pos[1]
                    self.selected_body.vx = deltax / 200
                    self.selected_body.vy = deltay / 200
            body.draw(screen, 1,0,0,5,True)
        screen.blit(self.img_edit, (50, HEIGHT - 100))
    
    # ====================================================================================
    #
    #   Simulation
    #
    # ====================================================================================
        

    def handle_simulation_events(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_stop_button.is_over(pos):
                self.is_active = not self.is_active
            elif self.reset_button.is_over(pos):
                self.reset()
            elif self.back_button.is_over(pos):
                self.reset()
                self.state = 1  # SimulationState.CREATION
        elif event.type == pygame.MOUSEWHEEL:
            self.adjust_zoom(event.y)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button is pressed
                self.pan_view(event.rel)

    def render_simulation(self, screen):
        for button in self.simulation_buttons:
            button.draw(screen)
        for body in self.bodies:
            body.draw(screen, self.zoom, self.pan[0], self.pan[1], 0, False)
        if self.is_active:
            self.update()                
            
        counter_surf = self.font2.render(f"{int(self.elapsed_time)}:{int((self.elapsed_time*10) % 10)}", True, RED)
        screen.blit(counter_surf, (WIDTH - 150, 10))