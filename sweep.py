import pandas as pd
from model import ForestModel, Herbivore

intensities = [0.2, 0.5, 0.8]
n_replicates = 10
n_steps = 150

all_results = []
trajectories = []

for intensity in intensities:
    for rep in range(n_replicates):
        seed = int(intensity * 1000) + rep

        model = ForestModel(
            width=20, height=20, n_herbivores=30,
            forestry_intensity=intensity, seed=seed
        )

        for i in range(model.n_herbivores):
            herbivore = Herbivore(model)
            x = model.random.randrange(model.width)
            y = model.random.randrange(model.height)
            model.grid.place_agent(herbivore, (x, y))

        for step in range(n_steps):
            model.step()

        df = model.datacollector.get_model_vars_dataframe()
        settled = df.iloc[-10:]  # average over final 10 steps once behaviour stabilises

        all_results.append({
            "forestry_intensity": intensity,
            "replicate": rep,
            "final_reserve_dependency": settled["reserve_dependency"].mean(),
            "final_mean_forage": settled["mean_forage"].mean(),
        })

        traj = df[["reserve_dependency"]].copy()
        traj["forestry_intensity"] = intensity
        traj["replicate"] = rep
        traj["step"] = traj.index
        trajectories.append(traj)

        print(f"intensity={intensity}, rep={rep}: "
              f"final_reserve_dependency={settled['reserve_dependency'].mean():.3f}")

results_df = pd.DataFrame(all_results)
results_df.to_csv("sweep_results.csv", index=False)

trajectories_df = pd.concat(trajectories, ignore_index=True)
trajectories_df.to_csv("sweep_trajectories.csv", index=False)

print("\nSaved sweep_results.csv and sweep_trajectories.csv")
print("\nMean final reserve-dependency by forestry intensity:")
print(results_df.groupby("forestry_intensity")["final_reserve_dependency"].mean())