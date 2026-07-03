from model import ForestModel, Herbivore

# Create the model: 20x20 grid, 30 herbivores, 50% forestry intensity
model = ForestModel(width=20, height=20, n_herbivores=30, forestry_intensity=0.5, seed=42)

# Place herbivores at random positions on the grid
for i in range(model.n_herbivores):
    herbivore = Herbivore(model)
    x = model.random.randrange(model.width)
    y = model.random.randrange(model.height)
    model.grid.place_agent(herbivore, (x, y))

# Run for 10 steps using the model's own step() method
for i in range(10):
    model.step()

# Pull the collected data out as a pandas DataFrame
results = model.datacollector.get_model_vars_dataframe()
print(results)