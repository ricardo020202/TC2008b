# =============================================================================
# Created By  : Jose Ricardo Rosales Castaneda
# Created Date: 24/08/2023
# Description : Wa-Tor Model
# =============================================================================

import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# =============================================================================
# Definicion de constantes
# =============================================================================
WATER = 0
FISH = 1
SHARK = 2

energies = {FISH: 20, SHARK: 3}
fertility_thresh = {FISH: 4, SHARK: 12}

colors = ['#FFFFFF', '#FFD700', '#FF0000']
cm = LinearSegmentedColormap.from_list('wator_cmap', colors, N=3)

random.seed(10)

# =============================================================================
# Definicion del agente
# =============================================================================
class Animal_Agent():
    def __init__(self, id, x, y, energy, fertility_threshold):
        self.id = id
        self.x, self.y = x, y
        self.energy = energy
        self.fertility_threshold = fertility_threshold
        self.fertility = 0
        self.dead = False

# =============================================================================
# Definicion del modelo
# =============================================================================
class Aquarium_Model():
    def __init__(self, width=75, height=50):
        self.width, self.height = width, height
        self.cells = width * height
        self.grid = [[WATER]*width for y in range(height)]
        self.animals = []

    # =============================================================================
    # Funcion para colocar un agente en el modelo
    # Entrada: id del agente, posicion x, posicion y
    # Salida: Ninguna
    # =============================================================================
    def place_agent(self, animal_id, x, y):
        animal = Animal_Agent(animal_id, x, y,
                            energies[animal_id],
                            fertility_thresh[animal_id])
        self.animals.append(animal)
        self.grid[y][x] = animal

    # =============================================================================
    # Funcion para llenar el modelo con agentes
    # Entrada: numero de peces, numero de tiburones
    # Salida: Ninguna
    # =============================================================================
    def fill(self, nfish=120, nsharks=40):
        self.nfish, self.nsharks = nfish, nsharks

        for _ in range(self.nfish):
            x, y = random.randrange(self.width), random.randrange(self.height)
            if not self.grid[y][x]:
                self.place_agent(FISH, x, y)

        for _ in range(self.nsharks):
            x, y = random.randrange(self.width), random.randrange(self.height)
            if not self.grid[y][x]:
                self.place_agent(SHARK, x, y)

    # =============================================================================
    # Funcion para obtener la matriz del modelo
    # Entrada: Ninguna
    # Salida: Matriz del modelo
    # =============================================================================
    def get_grid(self):
        return [[self.grid[y][x].id if self.grid[y][x] else 0
                 for x in range(self.width)] for y in range(self.height)]

    # =============================================================================
    # Funcion para obtener los vecinos de un agente
    # Entrada: posicion x, posicion y
    # Salida: Diccionario de vecinos
    # =============================================================================
    def get_neighbours(self, x, y):
        neighbours = {}
        for dx, dy in ((0,-1), (1,0), (0,1), (-1,0)):
            xp, yp = (x+dx) % self.width, (y+dy) % self.height
            neighbours[xp, yp] = self.grid[yp][xp]
        return neighbours

    # =============================================================================
    # Funcion para realizar un paso en el modelo
    # Entrada: agente
    # Salida: Ninguna
    # =============================================================================
    def move(self, animal):
        neighbours = self.get_neighbours(animal.x, animal.y)
        animal.fertility += 1
        moved = False
        
        if animal.id == SHARK:
            fish_neighbours = [pos for pos in neighbours if neighbours[pos] != WATER and neighbours[pos].id == FISH]
            if fish_neighbours:
                xp, yp = random.choice(fish_neighbours)
                animal.energy += 2
                self.grid[yp][xp].dead = True
                self.grid[yp][xp] = WATER
                moved = True

        if not moved:
            water_neighbours = [pos for pos in neighbours if neighbours[pos] == WATER]
            if water_neighbours:
                xp, yp = random.choice(water_neighbours)
                if animal.id != FISH:
                    animal.energy -= 1
                moved = True
            elif animal.id == SHARK:
                xp, yp = animal.x, animal.y

        if animal.energy < 0:
            animal.dead = True
            self.grid[animal.y][animal.x] = WATER
        elif moved:
            x, y = animal.x, animal.y
            animal.x, animal.y = xp, yp
            self.grid[yp][xp] = animal
            if animal.fertility >= animal.fertility_threshold:
                animal.fertility = 0
                self.place_agent(animal.id, x, y)
            else:
                self.grid[y][x] = WATER

    # =============================================================================
    # Funcion para avanzar un paso en el modelo
    # Entrada: Ninguna
    # Salida: Ninguna
    # =============================================================================
    def step(self):
        random.shuffle(self.animals)
        nanimals = len(self.animals)
        for i in range(nanimals):
            animal = self.animals[i]
            if animal.dead:
                continue
            self.move(animal)

        self.animals = [animal for animal in self.animals if not animal.dead]

aquarium = Aquarium_Model()
aquarium.fill()

fig, ax = plt.subplots()
im = ax.imshow(aquarium.get_grid(), cmap=cm, interpolation='none')

CHRONONS = 400

for _ in range(CHRONONS):
    aquarium.step()
    im.set_array(aquarium.get_grid())
    ax.set_title(str(_ + 1) + ' ' + 'chronons')
    plt.pause(0.1) 

plt.show()
