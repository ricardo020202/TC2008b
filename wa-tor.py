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
# Definicion del agente Animal
# =============================================================================
class Animal_Agent():
    def __init__(self, id, x, y, energy, fertility_thresh):
        self.id = id
        self.x, self.y = x, y
        self.energy = energy
        self.fertility_thresh = fertility_thresh
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
    # Funcion para llenar el modelo con agentes
    # Entrada: numero de peces, numero de tiburones
    # Salida: Ninguna
    # =============================================================================
    def place_agents(self, numFish=120, numSharks=40):
        self.numFish, self.numSharks = numFish, numSharks

        for _ in range(self.numFish):
            x, y = random.randrange(self.width), random.randrange(self.height)
            if not self.grid[y][x]:
                animal = Animal_Agent(FISH, x, y, energies[FISH], fertility_thresh[FISH])
                self.animals.append(animal)
                self.grid[y][x] = animal

        for _ in range(self.numSharks):
            x, y = random.randrange(self.width), random.randrange(self.height)
            if not self.grid[y][x]:
                animal = Animal_Agent(SHARK, x, y, energies[SHARK], fertility_thresh[SHARK])
                self.animals.append(animal)
                self.grid[y][x] = animal

    # =============================================================================
    # Funcion para obtener la matriz del modelo
    # Entrada: Ninguna
    # Salida: Matriz del modelo
    # =============================================================================
    def get_grid(self):
        return [[self.grid[y][x].id if self.grid[y][x] else 0
                 for x in range(self.width)] for y in range(self.height)]

    # =============================================================================
    # Funcion para mover un agente
    # Entrada: agente
    # Salida: Ninguna
    # =============================================================================
    def move(self, animal, x, y):
        neighbours = {}
        animal.fertility += 1
        moved = False

        dx_dy_pairs = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for dx, dy in dx_dy_pairs:
            xp, yp = (x + dx) % self.width, (y + dy) % self.height
            neighbours[xp, yp] = self.grid[yp][xp]
        
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
            if animal.fertility >= animal.fertility_thresh:
                animal.fertility = 0
                animal = Animal_Agent(animal.id, x, y, energies[animal.id], fertility_thresh[animal.id])
                self.animals.append(animal)
                self.grid[y][x] = animal
            else:
                self.grid[y][x] = WATER

    # =============================================================================
    # Funcion para avanzar un paso en el modelo
    # Entrada: Ninguna
    # Salida: Ninguna
    # =============================================================================
    def step(self):
        random.shuffle(self.animals)
        numAnimals = len(self.animals)
        for i in range(numAnimals):
            animal = self.animals[i]
            if animal.dead:
                continue
            self.move(animal, animal.x, animal.y)

        self.animals = [animal for animal in self.animals if not animal.dead]

CHRONONS = 400
WATER, FISH, SHARK = 0, 1, 2
energies = {FISH: 20, SHARK: 3}
fertility_thresh = {FISH: 4, SHARK: 12}

colors = ['#FFFFFF', '#FFD700', '#FF0000']
cm = LinearSegmentedColormap.from_list('wator_cmap', colors, N=3)

random.seed(10)

aquarium = Aquarium_Model()
aquarium.place_agents()

fig, ax = plt.subplots()
im = ax.imshow(aquarium.get_grid(), cmap=cm, interpolation='none')

for _ in range(CHRONONS):
    aquarium.step()
    im.set_array(aquarium.get_grid())
    ax.set_title(str(_ + 1) + ' ' + 'chronons')
    plt.pause(0.1) 

plt.show()
