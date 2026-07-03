import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from model import ForestModel, Herbivore

intensities = [0.2, 0.5, 0.8]
n_steps = 150

# Colors for each cell type
cell_colors = {
    "forest": "#2d6a4f",    # dark green
    "logged": "#8d6e63",    # brown
    "reserve": "#4a90d9",   # blue
}

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for ax, intensity in zip(axes, intensities):
    seed = int(intensity * 1000)
    model = ForestModel(width=20, height=20, n_herbivores=30,
                         forestry_intensity=intensity, seed=seed)

    for i in range(model.n_herbivores):
        herbivore = Herbivore(model)
        x = model.random.randrange(model.width)
        y = model.random.randrange(model.height)
        model.grid.place_agent(herbivore, (x, y))

    for step in range(n_steps):
        model.step()

    # Build a colour grid from cell_type
    grid_img = np.zeros((model.height, model.width, 3))
    color_map = {
        "forest": (0.176, 0.416, 0.310),
        "logged": (0.553, 0.431, 0.388),
        "reserve": (0.290, 0.565, 0.851),
    }
    for (x, y), cell in model.cell_type.items():
        grid_img[y, x] = color_map[cell]

    ax.imshow(grid_img, origin="lower")

    # Plot herbivore positions
    xs = [a.pos[0] for a in model.agents]
    ys = [a.pos[1] for a in model.agents]
    ax.scatter(xs, ys, c="yellow", edgecolors="black", s=60, linewidths=0.8, zorder=3)

    reserve_dep = sum(1 for a in model.agents if model.cell_type[a.pos] == "reserve") / len(model.agents)
    ax.set_title(f"Forestry intensity = {intensity}\nReserve-dependency = {reserve_dep:.2f}", fontsize=12)
    ax.set_xticks([])
    ax.set_yticks([])

# Shared legend
legend_patches = [
    mpatches.Patch(color=cell_colors["forest"], label="Forest"),
    mpatches.Patch(color=cell_colors["logged"], label="Logged"),
    mpatches.Patch(color=cell_colors["reserve"], label="Reserve"),
    mpatches.Patch(facecolor="yellow", edgecolor="black", label="Herbivore"),
]
fig.legend(handles=legend_patches, loc="lower center", ncol=4, fontsize=11, bbox_to_anchor=(0.5, -0.02))

fig.suptitle("Landscape and herbivore positions after 150 steps, by forestry intensity", fontsize=14)
fig.tight_layout(rect=[0, 0.05, 1, 0.95])
fig.savefig("figure3_landscape_snapshot.png", dpi=150, bbox_inches="tight")
print("Saved figure3_landscape_snapshot.png")