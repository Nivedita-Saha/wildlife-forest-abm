from model import ForestModel

for intensity in [0.2, 0.5, 0.8]:
    model = ForestModel(width=20, height=20, n_herbivores=30, forestry_intensity=intensity, seed=1)
    counts = {"forest": 0, "logged": 0, "reserve": 0}
    for cell in model.cell_type.values():
        counts[cell] += 1
    total = sum(counts.values())
    print(f"intensity={intensity}: forest={counts['forest']/total:.2f}, "
          f"logged={counts['logged']/total:.2f}, reserve={counts['reserve']/total:.2f}")