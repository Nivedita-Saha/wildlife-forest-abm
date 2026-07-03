import mesa
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np


class ForestModel(mesa.Model):
    """
    A model of herbivore space use under varying forestry intensity.
    Grid cells are typed as 'forest', 'logged', or 'reserve'.
    """

    def __init__(self, width=20, height=20, n_herbivores=30, forestry_intensity=0.5, seed=None):
        super().__init__(seed=seed)

        self.width = width
        self.height = height
        self.forestry_intensity = forestry_intensity
        self.n_herbivores = n_herbivores

        self.grid = MultiGrid(width, height, torus=False)

        self.cell_type = {}
        self.forage = {}

        self._init_landscape()

        self.datacollector = DataCollector(
            model_reporters={
                "mean_forage": lambda m: np.mean(list(m.forage.values())),
                "reserve_dependency": lambda m: (
                    sum(1 for a in m.agents if m.cell_type[a.pos] == "reserve") / len(m.agents)
                    if len(m.agents) > 0 else 0
                ),
                "forest_count": lambda m: sum(1 for a in m.agents if m.cell_type[a.pos] == "forest"),
                "logged_count": lambda m: sum(1 for a in m.agents if m.cell_type[a.pos] == "logged"),
                "reserve_count": lambda m: sum(1 for a in m.agents if m.cell_type[a.pos] == "reserve"),
            }
        )

    def _init_landscape(self):
        """
        Assigns each grid cell a type: 'forest', 'logged', or 'reserve'.
        Roughly matches Grimsö: ~85% of forest area under conventional
        management, ~15% protected reserve. Within the managed portion,
        forestry_intensity controls what fraction is actively logged
        at any given time.
        """
        reserve_fraction = 0.15
        for x in range(self.width):
            for y in range(self.height):
                r = self.random.random()
                if r < reserve_fraction:
                    cell = "reserve"
                elif r < reserve_fraction + (1 - reserve_fraction) * self.forestry_intensity:
                    cell = "logged"
                else:
                    cell = "forest"

                self.cell_type[(x, y)] = cell
                self.forage[(x, y)] = 0.2 if cell == "logged" else 1.0

    def step_forage_regrowth(self):
        """
        Called once per model step. Forage regenerates a little each step,
        capped at 1.0, and regenerates slower on logged cells.
        """
        for pos, cell in self.cell_type.items():
            growth_rate = 0.02 if cell == "logged" else 0.05
            self.forage[pos] = min(1.0, self.forage[pos] + growth_rate)

    def step(self):
        self.agents.shuffle_do("step")
        self.step_forage_regrowth()
        self.datacollector.collect(self)


class Herbivore(mesa.Agent):
    """
    A herbivore that moves each step toward nearby cells with better
    forage or reserve status, avoiding logged cells where possible,
    and eats forage from its current cell.
    """

    def __init__(self, model):
        super().__init__(model)

    def step(self):
        self._move()
        self._eat()

    def _move(self):
        x, y = self.pos
        neighbors = self.model.grid.get_neighborhood(
            (x, y), moore=True, include_center=True
        )

        def score(pos):
            cell = self.model.cell_type[pos]
            forage_val = self.model.forage[pos]
            if cell == "reserve":
                bonus = 0.5
            elif cell == "logged":
                bonus = -0.5
            else:
                bonus = 0.0
            return forage_val + bonus

        best_pos = max(neighbors, key=score)
        self.model.grid.move_agent(self, best_pos)

    def _eat(self):
        pos = self.pos
        current_forage = self.model.forage[pos]
        eaten = min(0.1, current_forage)
        self.model.forage[pos] -= eaten