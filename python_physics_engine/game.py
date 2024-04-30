import pygame
#import math
import engine
import random as rnd

#import tkinter as tk
from tkinter import *
#import os


class Rect:
    def __init__(self, left, top, right, bottom):
        self.left, self.top, self.right, self.bottom =\
            left, top, right, bottom

        self.momentum = engine.Vector2D(0,0)

    def get_momentum(self):
        return self.momentum

class Frame:
    def __init__(self, pressed, dt):
        self.pressed = pressed
        self.dt = dt

"""pos and val - Vector2D class"""
class Arrow:
    def __init__(self, pos, val, color):
        self.pos, self.val = pos, val
        self.color = color
        self.tip = 10
        self.factor = 3
        self.list_of_points = []
        if abs(self.val) != 0:
            self.dir = self.val/abs(self.val)
            self.list_of_points = [list(self.pos.intpair()),
                               list((self.pos + self.val / self.factor).intpair()),
                               list((self.pos + self.val / self.factor - self.tip * self.dir + self.tip / self.factor * self.dir.cross()).intpair()),
                               list((self.pos + self.val / self.factor - self.tip * self.dir - self.tip / self.factor * self.dir.cross()).intpair()),
                               list((self.pos + self.val / self.factor).intpair()),
                               ]
        #else:
            #self.list_of_points = [list(self.pos.intpair())]

    def __call__(self, pos, val):
        if (type(pos) is tuple):
            self.pos = engine.Vector2D(*pos)
        else:
            self.pos = pos

        if (type(val) is tuple):
            self.val = engine.Vector2D(*val)
        else:
            self.val = val

        if abs(self.val) != 0:
            self.dir = self.val / abs(self.val)
            self.list_of_points = [list(self.pos.intpair()),
                                   list((self.pos + self.val / self.factor).intpair()),
                                   list((self.pos + self.val / self.factor - self.tip * self.dir + self.tip/self.factor * self.dir.cross()).intpair()),
                                   list((self.pos + self.val / self.factor - self.tip * self.dir - self.tip/self.factor * self.dir.cross()).intpair()),
                                   list((self.pos + self.val / self.factor).intpair()),
                                   ]

"""
Derived class from Scene
It has function for rendering
"""
class GScene(engine.Scene):
    def __init__(self, width, height):
        super(GScene, self).__init__()
        self.sphere_color = {}
        #self.vel_vector = {}
        self.number_vel_arrow = 0
        self.number_acc_arrow = 0
        self.border_active = True

        self.vel_arrow_enable  = False
        self.acc_arrow_enable  = False
        self.forse_arrow_enable = False
        self.group_forse_arrow_enable = False

        self.vel_arrow = {}
        self.acc_arrow = {}

        self.forse_arrow = Arrow(engine.Vector2D(0, 1),
                                 engine.Vector2D(1, 0),
                                 (255, 255, 255)
                                 )

        self.rect = Rect(0, 0, width, height)
        print('Create')

    def delete_arrow(self, i):
        self.vel_arrow.pop(i)
        self.acc_arrow.pop(i)

        self.number_vel_arrow -= 1
        self.number_acc_arrow -= 1

    def update_arrow_vel(self, i):
        if self.vel_arrow_enable is True:
            self.vel_arrow[i](self.sphere[i].pos, self.sphere[i].vel)

    def update_arrow_acc(self, i):
        if self.acc_arrow_enable is True:
            self.acc_arrow[i](self.sphere[i].pos, self.sphere[i].acc)

    def update_arrow_forse(self, tip, i):
        if self.forse_arrow_enable is True:
            self.forse_arrow(self.sphere[i].pos, tip)

    def update_arrow_all(self):
        if self.vel_arrow_enable is True:
            for i in self.sphere:
                self.update_arrow_vel(i)

        if self.acc_arrow_enable is True:
            for i in self.sphere:
                self.update_arrow_acc(i)

    def handle_border(self):
        self.rect.momentum = engine.Vector2D(0, 0)
        for i in self.sphere:
            """left"""
            if self.sphere[i].pos.x - self.sphere[i].radius < self.rect.left:
                if self.sphere[i].vel.x < 0:
                    depth = abs(self.rect.left - (self.sphere[i].pos.x - self.sphere[i].radius))
                    self.sphere[i].pos.x += depth
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.x = -self.sphere[i].vel.x
                    self.rect.momentum += ( p_prev-self.sphere[i].get_momentum())
                    self.sphere[i].pos.x = self.rect.left + self.sphere[i].radius

            """top"""
            if self.sphere[i].pos.y - self.sphere[i].radius < self.rect.top:
                if self.sphere[i].vel.y < 0:
                    depth = abs(self.rect.top - (self.sphere[i].pos.y - self.sphere[i].radius))
                    self.sphere[i].pos.y += depth
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.y = -self.sphere[i].vel.y
                    self.rect.momentum += ( p_prev - self.sphere[i].get_momentum())
                    self.sphere[i].pos.y = self.rect.top + self.sphere[i].radius

            """right"""
            if self.sphere[i].pos.x + self.sphere[i].radius > self.rect.right:
                if self.sphere[i].vel.x > 0:
                    depth = abs(self.sphere[i].pos.x + self.sphere[i].radius - self.rect.right)
                    self.sphere[i].pos.x -= depth
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.x = -self.sphere[i].vel.x
                    self.rect.momentum += ( p_prev - self.sphere[i].get_momentum())
                    self.sphere[i].pos.x = self.rect.right - self.sphere[i].radius

            """bottom"""
            if self.sphere[i].pos.y + self.sphere[i].radius > self.rect.bottom:
                if self.sphere[i].vel.y > 0:
                    depth = abs(self.sphere[i].pos.y + self.sphere[i].radius - self.rect.bottom)
                    self.sphere[i].pos.y -= depth
                    p_prev = self.sphere[i].get_momentum()
                    self.sphere[i].vel.y = -self.sphere[i].vel.y
                    self.rect.momentum += ( p_prev - self.sphere[i].get_momentum())
                    self.sphere[i].pos.y = self.rect.bottom - self.sphere[i].radius

    """Update scene state"""
    def update_graphick_scene(self, frame):
        #f = Vec2()
        #f.x = frame.pressed[pygame.K_RIGHT] - frame.pressed[pygame.K_LEFT];
        #f.y = frame.pressed[pygame.K_DOWN] - frame.pressed[pygame.K_UP];
        #f *= self.a
        if self.border_active is True:
            self.handle_border()

        self.update(frame.dt)

        self.update_arrow_all()

        self.collision_response_spheres(self.collision_detection_spheres(frame.dt), frame.dt)



    def render(self, canvas):
        """Draw Player on the Game window"""
        for i in self.sphere:
            canvas.circle(self.sphere_color[i],
                          self.sphere[i].pos.intpair(),
                          self.sphere[i].radius)

        if self.vel_arrow_enable is True:
            for i in self.vel_arrow:
                if self.sphere[i].vel != engine.Vector2D(0, 0):
                    canvas.arrow(self.vel_arrow[i].color,
                                 self.vel_arrow[i].list_of_points, 1
                             )

        if self.acc_arrow_enable is True:
            for i in self.acc_arrow:
                if self.sphere[i].acc != engine.Vector2D(0, 0):
                    canvas.arrow(self.acc_arrow[i].color,
                                 self.acc_arrow[i].list_of_points, 3
                         )
        if self.forse_arrow_enable is True:
            canvas.arrow(self.forse_arrow.color,
                         self.forse_arrow.list_of_points, 4
                         )


    def add_arrow(self, pos, vel, acc, color):
        self.vel_arrow[self.number_vel_arrow] = Arrow(pos, vel, color)
        self.number_vel_arrow += 1

        self.acc_arrow[self.number_acc_arrow] = Arrow(pos, acc, color)
        self.number_acc_arrow += 1

    def in_sphere(self, pos):
        for i in self.sphere:
            if abs(self.sphere[i].pos - engine.Vector2D(*pos)) <= self.sphere[i].radius:
                return i

        return -1
    #def generate_scene_none_intersects(self):

     #   for i in range (0, self.n_spheres):



class Canvas:
    def __init__(self, screen):
        self.screen = screen

    def clear(self):
        self.screen.fill((0, 0, 0))

    def circle(self, color, pos, radius):
        pygame.draw.circle(self.screen, color, pos, radius)

    def arrow(self, color, list_of_points, width):
        pygame.draw.lines(self.screen, color, False, list_of_points, width)


class World:
    def __init__(self):
        self.units = []

    def update(self, frame):
        for u in self.units:
            u.update_graphick_scene(frame)

    def render(self, canvas):
        canvas.clear()
        for u in self.units:
            u.render(canvas)

    def addUnit(self, u):
        self.units.append(u)

class Game:
    #self.world.addUnit(Player(pos=(50, 50), rect=Rect(0, 0, self.width, self.height)))
    def __init__(self):
        self._running = True
        self._pause = False
        self.key_r_pressed = False
        self.key_v_pressed = False
        self.key_a_pressed = False
        self.key_m_pressed = False
        self.key_f_pressed = False
        self.current_forse_i = -1


        # self.show_vel_vector = False
        self.size = self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.font = pygame.font.init()
        self.font = pygame.font.SysFont('mono', self.height // 30, bold=True)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.fps = 50
        self.playtime = 0.0

        pygame.display.set_caption('Game')

        self.clock = pygame.time.Clock()

        self.canvas = Canvas(self.screen)

        self.world = World()

        rnd.seed()
        self.number_speres = 5  # default

        self.scene = GScene(self.width, self.height)

        # TODO: перегрузить вызов Scene

        for i in range(0, self.number_speres):
            self.scene.add_sphere(engine.Vector2D(rnd.randint(10, self.width - 10),
                                                  rnd.randint(10, self.height - 10)),
                                  engine.Vector2D(rnd.randint(-500, 500),
                                                  rnd.randint(-500, 500)),
                                  engine.Vector2D(rnd.randint(-50, 50),
                                                  rnd.randint(-50, 50)),
                                  rnd.randint(1, 10),
                                  rnd.randint(10, 70))
            self.scene.sphere_color[i] = (rnd.randint(0, 255),
                                          rnd.randint(0, 255),
                                          rnd.randint(0, 255))

        for i in range (0, self.number_speres):
            self.scene.add_arrow(self.scene.sphere[i].pos,
                                 self.scene.sphere[i].vel,
                                 self.scene.sphere[i].acc,
                                 (255 - self.scene.sphere_color[i][0],
                                  255 - self.scene.sphere_color[i][1],
                                  255 - self.scene.sphere_color[i][2])
                                 )
        self.world.addUnit(self.scene)



    def exit(self):
        """Exit the game"""
        self._running = False

    def handle_event(self, event):
        """Handling one pygame event"""
        #print(pygame.event.eveSnt_name(event.type))

        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        if event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

            if event.key == pygame.K_SPACE:
                if self._pause is True:
                    self._pause = False
                else:
                    self._pause = True



            if event.key == pygame.K_DELETE:
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                if i != -1:
                    self.scene.delete_sphere(i)
                    self.scene.delete_arrow(i)
                    i = -1

            """Border"""
            if event.key == pygame.K_b:
                if self.scene.border_active is True:
                    self.scene.border_active = False
                else:
                    self.scene.border_active = True
            """show vel_arrow"""
            if event.key == pygame.K_LCTRL:
                for i in self.scene.sphere:
                    self.scene.vel_arrow[i](self.scene.sphere[i].pos, self.scene.sphere[i].vel)

                if self.scene.vel_arrow_enable is True:
                    self.scene.vel_arrow_enable = False
                else:
                    self.scene.vel_arrow_enable = True

            """show acc_arrow"""
            if event.key == pygame.K_LSHIFT:

                if self.scene.acc_arrow_enable is True:
                    self.scene.acc_arrow_enable = False
                else:
                    self.scene.acc_arrow_enable = True

                for i in self.scene.sphere:
                        self.scene.acc_arrow[i](self.scene.sphere[i].pos, self.scene.sphere[i].acc)


            if event.key == pygame.K_r:
                #print("key r pressed")
                self.key_r_pressed = True

            if event.key == pygame.KMOD_LCTRL:
                self.key_lctrl_pressed = True

            if event.key == pygame.K_v:
                self.key_v_pressed = True

            if event.key == pygame.K_f:
                self.key_f_pressed = True

            if event.key == pygame.K_a:
                self.key_a_pressed = True

            if event.key == pygame.K_m:
                self.key_m_pressed = True


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                self.key_r_pressed = False

            if event.key == pygame.K_a:
                self.key_a_pressed = False

            if event.key == pygame.K_v:
                self.key_v_pressed = False

            if event.key == pygame.K_f:
                self.key_f_pressed = False
                if (pygame.mouse.get_pressed() == (1, 0, 0)):
                    self.scene.forse_arrow_enable = False

            if event.key == pygame.K_m:
                self.key_m_pressed = False

        if event.type == pygame.MOUSEMOTION:
            """motion sphere"""
            #print (pygame.mouse.get_pressed())
            if (pygame.mouse.get_pressed() == (1,0,0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)

                #print (self.current_forse_i, i, self.scene.forse_arrow_enable is True)
                """apply single forse"""
                if self.key_f_pressed is True:
                    if  self.scene.forse_arrow_enable is True:
                        #self.pos = pygame.mouse.get_pos()
                        self.r_pos = engine.Vector2D(self.pos[0] - self.scene.sphere[self.current_forse_i].pos.x,
                                                     self.pos[1] - self.scene.sphere[self.current_forse_i].pos.y)
                        self.scene.forse_arrow_enable = True

                        self.scene.update_arrow_forse( self.r_pos, self.current_forse_i)

                        self.scene.sphere[self.current_forse_i].acc += self.r_pos - self.scene.sphere[self.current_forse_i].acc
                        self.scene.update_arrow_acc(self.current_forse_i)
                        #print (self.scene.forse_arrow.val, "   ", self.scene.sphere[self.current_forse_i].acc)

                    if self.scene.group_forse_arrow_enable is True:
                        pass

                    else:
                        pass
                    """apply forse for all spheres"""


                """motion sphere"""
                if self.key_f_pressed is False:

                    if i != -1:
                        #self.r_pos = engine.Vector2D(self.pos[0] - self.scene.sphere[i].pos.x,
                         #                            self.pos[1] - self.scene.sphere[i].pos.y)
                        prev_pos = self.scene.sphere[i].pos
                        self.scene.sphere[i].set_pos(self.pos)

                        self.scene.update_arrow_acc(i)
                        self.scene.update_arrow_vel(i)
                        #self.scene.update_arrow_forse( self.r_pos + (self.scene.sphere[i].pos - prev_pos), i)

                        i = -1

        if event.type == pygame.MOUSEBUTTONDOWN:
            """Right mouse button down - create new sphere"""

            if (pygame.mouse.get_pressed() == (1, 0, 0)):
                self.pos = pygame.mouse.get_pos()
                i = self.scene.in_sphere(self.pos)
                if i!=-1:
                    print (i)
                    print(self.scene.sphere[i])
                    if self.scene.forse_arrow_enable is False and self.key_f_pressed is True:
                        self.current_forse_i = i
                        self.scene.forse_arrow_enable = True
                else:
                    if self.scene.group_forse_arrow_enable is False and self.key_f_pressed is True:
                        self.scene.group_forse_arrow_enable = True
                i = -1

            if (pygame.mouse.get_pressed() == (0, 0, 1)):
                self.pos = pygame.mouse.get_pos()
                self.scene.add_sphere(engine.Vector2D(*self.pos),
                                      engine.Vector2D(rnd.randint(-500, 500),
                                                          rnd.randint(-500, 500)),
                                      engine.Vector2D(rnd.randint(-50, 50),
                                                      rnd.randint(-50, 50)),
                                      rnd.randint(1, 20),
                                      rnd.randint(10, 50))
                self.scene.sphere_color[self.scene.n_spheres-1] = (rnd.randint(0, 255),
                                              rnd.randint(0, 255),
                                              rnd.randint(0, 255))

                self.scene.add_arrow(self.scene.sphere[self.scene.n_spheres-1].pos,
                                     self.scene.sphere[self.scene.n_spheres-1].vel,
                                     self.scene.sphere[self.scene.n_spheres - 1].acc,
                                     (255 - self.scene.sphere_color[self.scene.n_spheres-1][0],
                                      255 - self.scene.sphere_color[self.scene.n_spheres-1][1],
                                      255 - self.scene.sphere_color[self.scene.n_spheres-1][2])
                                     )
            """wheel mouse"""
            if (pygame.mouse.get_pressed() == (0, 0, 0)):
                """radius"""
                if (self.key_r_pressed is True):
                    self.pos = pygame.mouse.get_pos()
                    i = self.scene.in_sphere(self.pos)
                    if i != -1:
                        """up"""
                        if (event.button == 4):
                            self.scene.sphere[i].set_radius(self.scene.sphere[i].radius + 2)
                        """down"""
                        if (event.button == 5):
                            self.scene.sphere[i].set_radius(self.scene.sphere[i].radius - 2)

                        i = -1

                """mass"""
                if (self.key_m_pressed is True):
                    self.pos = pygame.mouse.get_pos()
                    i = self.scene.in_sphere(self.pos)
                    if i != -1:
                        """up"""
                        if (event.button == 4):
                            self.scene.sphere[i].set_mass(self.scene.sphere[i].mass + 2)
                        """down"""
                        if (event.button == 5):
                            self.scene.sphere[i].set_mass(self.scene.sphere[i].mass - 2)
                        i = -1

                """velocity"""
                if (self.key_v_pressed is True):
                    self.pos = pygame.mouse.get_pos()
                    i = self.scene.in_sphere(self.pos)
                    if i != -1:
                        """up"""
                        if (event.button == 4):
                            self.scene.sphere[i].set_vel_abs(abs(self.scene.sphere[i].vel) + 5)
                            self.scene.update_arrow_vel(i)
                        """down"""
                        if (event.button == 5):
                            self.scene.sphere[i].set_vel_abs(abs(self.scene.sphere[i].vel) - 5)
                            self.scene.update_arrow_vel(i)
                        i = -1

                """acc"""
                if (self.key_a_pressed is True):
                    self.pos = pygame.mouse.get_pos()
                    i = self.scene.in_sphere(self.pos)
                    if i != -1:
                        """up"""
                        if (event.button == 4):
                            self.scene.sphere[i].set_acc_abs(abs(self.scene.sphere[i].acc) + 2)
                            self.scene.update_arrow_acc(i)
                        """down"""
                        if (event.button == 5):
                            self.scene.sphere[i].set_acc_abs(abs(self.scene.sphere[i].acc) - 2)
                            self.scene.update_arrow_acc(i)
                        i = -1

        if event.type == pygame.MOUSEBUTTONUP:
            if self.key_f_pressed is True:
                #self.key_f_pressed = False
                self.scene.forse_arrow_enable = False




    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def flip(self):

        pygame.display.flip()
        #self.clock.tick(self.fps)
        self.screen.blit(self.background, (0, 0))

    def draw_text(self, text, coord):
        """Center text in window.
        """
        fw, fh = self.font.size(text)
        surface = self.font.render(text, True, (0, 255, 0))
        #self.screen.blit(surface, ((self.width - fw) // 2, (self.height - fh) // 2))

        self.screen.blit(surface, coord)

    def execute(self):
        """Execution loop of the game"""
        while self._running:
            # get all pygame events from queue
            for event in pygame.event.get():
                self.handle_event(event)

            dt = self.clock.tick(self.fps) / 1000.0
            if self._pause is False:
                self.world.update(Frame(pygame.key.get_pressed(), dt))
                self.playtime += dt
            self.world.render(self.canvas)


            self.draw_text("FPS: %6.3f  PLAYTIME: %6.3f SECONDS" %(self.clock.get_fps(), self.playtime),
                           (self.font.get_linesize(), self.height - self.font.get_linesize()*3))
            self.draw_text("MOMENTUM: %6.3f  ENERGY: %6.3f " %(abs(self.scene.calculate_momentum()), self.scene.calculate_energy()),
                           (self.font.get_linesize(), self.height - self.font.get_linesize() *2))
            self.draw_text("NUMBER OF SPHERES: %6d " % (self.scene.n_spheres),
                           (self.font.get_linesize(), self.height - self.font.get_linesize() * 1))

            #self.scene.momentum = engine.Vector2D(0, 0)
            #self.scene.energy = 0

            self.flip()

        self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.execute()
