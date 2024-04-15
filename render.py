import pygame
from math import sqrt, pow
from buttons import Button
from bodies import CelestialBody
from physics import Physics
import config
import random
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
        self.bodies = []
        self.buttons = []
        self.state = 1  # SimulationState.CREATION
        self.is_active = False
        self.create_mode = False
        self.delete_mode = False
        self.drag_body = None
        self.selected_body = None
        self.zoom = 1
        self.pan = [0, 0]
        self.elapsed_time = 0
        self.create_buttons()
        self.img_create = pygame.image.load('create.png')
        self.img_edit = pygame.image.load('edit.png')
        self.font = pygame.font.SysFont('Arial', 25)
        self.font2 = pygame.font.Font(None, 74)

    def create_buttons(self):
        self.create_button = Button(0, 0, 100, 40, "Create")
        self.delete_button = Button(100, 0, 100, 40, "Delete")
        self.demo_button = Button(200, 0, 100, 40, "Demo")
        self.edit_button = Button(300, 0, 100, 40, "Edit")
        self.run_button = Button(400, 0, 100, 40, "Run")
        self.start_stop_button = Button(0, 0, 150, 40, "Start/Stop")
        self.reset_button = Button(150, 0, 100, 40, "Reset")
        self.back_button = Button(250, 0, 100, 40, "Back")
        self.buttons = [
            self.create_button,
            self.delete_button,
            self.demo_button,
            self.edit_button,
            self.run_button,
            self.start_stop_button,
            self.reset_button,
            self.back_button,
        ]
        self.create_buttons =[self.create_button, self.delete_button, self.demo_button, self.edit_button, self.back_button]

    def create_body(self, pos):
        mass = 2.5
        color = WHITE
        name = f"User{len(self.bodies)}"
        size = mass * 10
        body = CelestialBody(name, pos[0], pos[1], mass, size, color)
        self.bodies.append(body)

    def delete_body(self, pos):
        for body in self.bodies:
            if body.is_over(pos):
                self.bodies.remove(body)
                break

    def load_demo(self):
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

    def update(self):
        for body in self.bodies:
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

    def reset(self):
        self.is_active = False
        self.elapsed_time = 0
        for body in self.bodies:
            body.reset()

    def adjust_zoom(self, amount):
        self.zoom *= 1.1 if amount > 0 else 0.9

    def pan_view(self, rel):
        self.pan[0] += rel[0]
        self.pan[1] += rel[1]

    def draw_text(surface, text, color, pos=(0, 0)):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)
    
    def handle_creation_events(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.create_button.is_over(pos):
                self.create_body(pos)
            elif self.delete_button.is_over(pos):
                self.delete_mode = True
            elif self.demo_button.is_over(pos):
                self.load_demo()
            elif self.edit_button.is_over(pos):
                self.state = 2  # SimulationState.EDIT
            elif self.run_button.is_over(pos):
                self.state = 3  # SimulationState.RUNNING
            else:
                for body in self.bodies:
                    if body.is_over(pos):
                        self.drag_body = body
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag_body = None
            self.delete_mode = False
        elif event.type == pygame.MOUSEMOTION:
            if self.drag_body:
                self.drag_body.move_to(event.pos)

    def render_creation_menu(self, screen):
        for button in self.create_buttons:
            button.draw(screen)
        for body in self.bodies:
            body.draw(screen)
        screen.blit(self.img_create, (0, HEIGHT - 100))
        if self.create_mode:
            self.draw_text(screen, "Click where you want to create a body", WHITE)
        elif self.delete_mode:
            self.draw_text(screen, "Click on the body to delete", WHITE)

    def handle_edit_events(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.run_button.is_over(pos):
                self.state = 3  # SimulationState.RUNNING
            elif self.back_button.is_over(pos):
                self.state = 1  # SimulationState.CREATION
            else:
                for body in self.bodies:
                    if body.is_over(pos):
                        self.selected_body = body
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_body = None
        elif event.type == pygame.MOUSEMOTION:
            if self.selected_body:
                self.selected_body.set_velocity(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            if self.selected_body:
                self.selected_body.adjust_mass(event.y)

    def render_edit_menu(self, screen):
        for button in self.buttons:
            button.draw(screen)
        for body in self.bodies:
            body.draw(screen, show_velocity=True)
        screen.blit(self.img_edit, (50, HEIGHT - 100))
        if self.selected_body:
            self.draw_text(screen, f"Editing: {self.selected_body.name}", WHITE)

    def handle_simulation_events(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_stop_button.is_over(pos):
                self.is_active = not self.is_active
            elif self.reset_button.is_over(pos):
                self.reset()
            elif self.back_button.is_over(pos):
                self.state = 1  # SimulationState.CREATION
        elif event.type == pygame.MOUSEWHEEL:
            self.adjust_zoom(event.y)
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button is pressed
                self.pan_view(event.rel)

    def render_simulation(self, screen):
        for button in self.buttons:
            button.draw(screen)
        for body in self.bodies:
            body.draw(screen, zoom=self.zoom, pan=self.pan)
        counter_surf = self.font2.render(f"{int(self.elapsed_time)}:{int((self.elapsed_time*10) % 10)}", True, RED)
        screen.blit(counter_surf, (WIDTH - 150, 10))