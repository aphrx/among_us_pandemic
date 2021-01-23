import pygame
import numpy as np
import random
import cv2
import sys
import argparse

from PIL import Image

class Agent:
    def __init__(self, map, image, status, lifespan, sporatic, quarantine):
        self.white_map = map
        self.image = image
        self.coords = [None, None]
        self.status = status
        self.last_dir = None
        self.duration = 0
        self.in_quarantine = False

        # Args
        self.virus_lifespan = int(lifespan)
        self.sporatic = float(sporatic)
        self.quarantine = quarantine

    def find_rand_location(self):    
        self.coords = self.white_map[random.randint(0, len(self.white_map))]

    def counter(self):
        self.duration += 1
        if self.duration % self.virus_lifespan == 0 and self.status == 1:
            self.status = 2
            self.in_quarantine = False
            self.find_rand_location()

        if self.duration % self.quarantine == 0 and self.status == 1 and not self.in_quarantine:
            self.coords = [400,750]
            self.in_quarantine = True


    def explore(self):
        
        up = [self.coords[1]-3,self.coords[0]]
        down = [self.coords[1]+3,self.coords[0]]
        left = [self.coords[1],self.coords[0]-3]
        right = [self.coords[1],self.coords[0]+3]
        directions = [up, down, left, right]
        valid = []

        im = Image.fromarray(self.image)

        if self.in_quarantine:
            for d in directions:
                if (d[0] > 710 and d[0] < 790) and (d[1] > 360 and d[1] < 440):
                    valid.append(d)
        else:
            for d in directions:
                color = im.getpixel((int(d[0]),int(d[1])))
                if color == (255,255,255):
                    valid.append(d)

        if self.last_dir is not None and  directions[self.last_dir] in valid and random.random() > self.sporatic:
            move = directions[self.last_dir]
        else:
            move = random.choice(valid)
            self.last_dir = directions.index(move)
        move[1], move[0] = move
        self.coords = move

        if self.status == 1:
            self.counter()

    def get_coords(self):
        return self.coords

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status
    


class Simulation:
    def __init__(self, origin, infection_rate, radius, agents, lifespan, sporatic, quarantine):
        pygame.init()
        WIDTH = 823
        HEIGHT = 482
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

        self.bg = pygame.image.load("assets/overlay.png")
        self.image = cv2.imread('assets/overlay.png')
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        thres = 50
        mask = gray > thres
        self.image[mask] = (255, 255, 255)
        self.white_map = np.column_stack(np.where(mask == True))

        #INSIDE OF THE GAME LOOP
        self.color = (255, 0, 0)

        # arguments
        self.infected_origin = int(origin)
        self.infection_rate = float(infection_rate)
        self.radius = int(radius)
        self.agent_quantity = int(agents)
        self.lifespan = int(lifespan)
        self.sporatic = float(sporatic)
        self.quarantine = int(quarantine)

    def add_agents(self, n):
        agents = []
        for i in range(n):
            infected = 0
            if i < self.infected_origin:
                infected = 1
            a = Agent(self.white_map, self.image, infected, self.lifespan, self.sporatic, self.quarantine)
            a.find_rand_location()
            agents.append(a)
        return agents

    def draw(self, coords, status):
        if status is 0:
            char = pygame.image.load("assets/rsz_white.png")
        elif status is 1:
            char = pygame.image.load("assets/rsz_red.png")
        elif status is 2:
            char = pygame.image.load("assets/rsz_black.png")
        self.screen.blit(char, (coords[1]-10, coords[0]-15))
        #pygame.draw.circle(self.screen, self.color, (coords[1],coords[0]), 5)

    def infection_radius(self, agents):
        for a in agents:
            for b in agents:
                if a is not b and a.get_status() == 1 and random.random() < self.infection_rate:
                    a_coords = a.get_coords()
                    b_coords = b.get_coords()
                    if abs(a_coords[0]-b_coords[0]) < self.radius and abs(a_coords[1]-b_coords[1]) < self.radius and b.get_status() == 0:
                        b.set_status(1)

    def quarantine_room(self):
        pygame.draw.rect(self.screen, (100,0,0), (700, 350, 100, 100), 0)
        pygame.draw.rect(self.screen, (255,0,0), (700, 350, 100, 100), 3)

    def loop(self):        
        agents = self.add_agents(self.agent_quantity)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.pygame.quit()
                    sys.exit()

            self.screen.blit(self.bg, (0, 0))

            if self.quarantine != -1:
                self.quarantine_room()

            for a in agents:
                a.explore()
                self.draw(a.get_coords(), a.get_status())

            self.infection_radius(agents)
            

            pygame.display.update()
            self.clock.tick(60)

def main():
    argparser = argparse.ArgumentParser(
        description='Among Us Pandemic Simulator')
    argparser.add_argument(
        '-o', '--origin',
        metavar='ORIGIN',
        default=1,
        help='Assigns number of people who start off with virus')
    argparser.add_argument(
        '-ir', '--infection-rate',
        metavar='INFECTION_RATE',
        default=0.03,
        help='Assigns infection rate from 0 to 1')
    argparser.add_argument(
        '-r', '--radius',
        metavar='RADIUS',
        default=20,
        help='Assigns infection radius')
    argparser.add_argument(
        '-a', '--amount',
        metavar='AMOUNT',
        default=20,
        help='Assigns number of agents')
    argparser.add_argument(
        '-l', '--lifespan',
        metavar='LIFESPAN',
        default=1000,
        help='Assigns virus lifespan in frames')
    argparser.add_argument(
        '-s', '--sporatic',
        metavar='SPORATIC',
        default=0.1,
        help='Assigns likelihood of agent changing direction when on a fixed path')
    argparser.add_argument(
        '-q', '--quarantine',
        metavar='QUARANTINE',
        default=-1,
        help='Assigns quarantine counter delay')
    
    args = argparser.parse_args()

    s = Simulation(args.origin, args.infection_rate, args.radius, args.amount, args.lifespan, args.sporatic, args.quarantine)
    s.loop()

if __name__ == '__main__':
    main()