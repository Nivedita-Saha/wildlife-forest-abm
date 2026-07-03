from model import ForestModel, Herbivore

# Create the model: 20x20 grid, 30 herbivores, 50% forestry intensity
model = ForestModel(width=20, height=20, n_herbivores=30, forestry_intensity=0.5, seed=42)

# Place herbivores at random positions on the grid
for i in range(model.n_herbivores if hasattr(model, "n_herbivores") else 30):
    herbivore = Herbivore(model)
    x = model.random.randrange(model.width)
    y = model.random.randrange(model.height)
    model.grid.place_agent(herbivore, (x, y))

# Run for 10 steps and print what's happening
for step in range(10):
    # move and feed every herbivore
    for agent in list(model.agents):
        agent.step()
    # regrow forage across the grid
    model.step_forage_regrowth()

    # count how many herbivores are on each cell type
    counts = {"forest": 0, "logged": 0, "reserve": 0}
    for agent in model.agents:
        cell = model.cell_type[agent.pos]
        counts[cell] += 1

    print(f"Step {step + 1}: {counts}")

print("\nRun complete.")