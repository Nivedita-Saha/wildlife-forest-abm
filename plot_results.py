import pandas as pd
import matplotlib.pyplot as plt

# ---------- Figure 1: reserve-dependency vs forestry intensity ----------
results = pd.read_csv("sweep_results.csv")

fig1, ax1 = plt.subplots(figsize=(7, 5))

# individual replicate points, slightly jittered for visibility
for intensity in results["forestry_intensity"].unique():
    subset = results[results["forestry_intensity"] == intensity]
    jitter = (subset["replicate"] - subset["replicate"].mean()) * 0.005
    ax1.scatter(subset["forestry_intensity"] + jitter, subset["final_reserve_dependency"],
                color="gray", alpha=0.5, zorder=2, label="Individual runs" if intensity == 0.2 else "")

# mean line across intensities
means = results.groupby("forestry_intensity")["final_reserve_dependency"].mean()
ax1.plot(means.index, means.values, marker="o", color="darkgreen", linewidth=2,
          zorder=3, label="Mean across replicates")

ax1.set_xlabel("Forestry intensity (proportion of non-reserve land actively logged)")
ax1.set_ylabel("Reserve-dependency (proportion of herbivore-time in reserve cells)")
ax1.set_title("Reserve-dependency falls as forestry intensity rises\n(habitat fragmentation limits access to reserve)")
ax1.set_xticks([0.2, 0.5, 0.8])
ax1.legend()
ax1.grid(alpha=0.3)

fig1.tight_layout()
fig1.savefig("figure1_reserve_dependency_vs_intensity.png", dpi=150)
print("Saved figure1_reserve_dependency_vs_intensity.png")

# ---------- Figure 2: agent distribution over time, one representative run ----------
trajectories = pd.read_csv("sweep_trajectories.csv")

fig2, ax2 = plt.subplots(figsize=(7, 5))

for intensity in [0.2, 0.5, 0.8]:
    # take replicate 0 as the representative run for each intensity
    run = trajectories[(trajectories["forestry_intensity"] == intensity) & (trajectories["replicate"] == 0)]
    ax2.plot(run["step"], run["reserve_dependency"], label=f"Forestry intensity = {intensity}")

ax2.set_xlabel("Step")
ax2.set_ylabel("Reserve-dependency")
ax2.set_title("Reserve-dependency over time\n(representative single run per intensity level)")
ax2.legend()
ax2.grid(alpha=0.3)

fig2.tight_layout()
fig2.savefig("figure2_reserve_dependency_over_time.png", dpi=150)
print("Saved figure2_reserve_dependency_over_time.png")