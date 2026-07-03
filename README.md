# Herbivore Space Use Under Forest Management Intensity

An agent-based model (Mesa) exploring how forestry intensity shapes herbivore access to protected reserve land — built around the research context of SLU's Grimsö Wildlife Research Station.

## Motivation

Grimsö's research explicitly studies how land-use practices — forestry, agriculture, infrastructure — affect the space use and population dynamics of wildlife such as moose and roe deer. This project models a simplified version of that relationship: how the proportion of forest under active logging affects where a herbivore population spends its time, and how easily it can reach protected reserve patches.

This is the third of three linked portfolio projects submitted for the SLU Research Engineer (AI-driven Social Simulations) application: a land-use negotiation simulator, statistical analysis of negotiation outcomes, and — here — what happens to wildlife on the ground once a land-use decision is made.

## Model design

- **Grid**: 20×20 Mesa `MultiGrid`. Cells are typed as `forest`, `logged`, or `reserve`.
- **Reserve**: a single contiguous block (~15% of the grid) in one corner, mirroring a real bounded protected area.
- **Forestry intensity**: the proportion of the remaining (non-reserve) land actively logged, tested at 20%, 50%, and 80%.
- **Herbivore agents**: each step, an agent looks at its 8 neighbouring cells and moves to whichever scores best — reserve cells are favoured, logged cells are penalised, forage level also counts. It then eats forage from its current cell.
- **Forage**: every cell has a forage value that regenerates a little each step, more slowly on logged cells.

## Key result

**Reserve-dependency falls as forestry intensity rises** — the opposite of the project's original hypothesis, and a more interesting finding.

| Forestry intensity | Mean reserve-dependency (10 replicates) |
|---|---|
| 20% | 0.92 |
| 50% | 0.65 |
| 80% | 0.51 |

This is driven by **habitat fragmentation**, not resource avoidance. Herbivores only ever assess their immediate neighbourhood, so they navigate the landscape locally, one step at a time. At low forestry intensity, forest cover stays largely connected, so herbivores can find a route to the reserve fairly easily. At high intensity, remaining forest becomes fragmented into small, disconnected pockets — herbivores can get functionally stranded, surrounded by logged land in every direction, unable to find a path to the reserve even though they are actively trying to avoid logged cells at every step.

This mirrors a well-documented real-world ecological effect: fragmentation can restrict access to refugia independently of overall habitat quality.

### Figures

- `figure1_reserve_dependency_vs_intensity.png` — final reserve-dependency vs. forestry intensity, all replicates shown, with the mean trend line.
- `figure2_reserve_dependency_over_time.png` — reserve-dependency over the full 150-step run for one representative replicate per intensity level, showing that higher intensity slows and dampens the settling process, not just its endpoint.
- `figure3_landscape_snapshot.png` — spatial snapshot of the landscape and herbivore positions after 150 steps, for all three intensity levels side by side. Makes the fragmentation mechanism directly visible.

## How to run

```bash
python3 -m venv venv
source venv/bin/activate
pip install mesa pandas matplotlib networkx

python sweep.py              # runs the full parameter sweep, saves CSVs
python plot_results.py       # produces figure1 and figure2
python landscape_snapshot.py # produces figure3
```

## What this demonstrates

- Applied agent-based modelling with Mesa: environment design, agent behaviour rules, and emergent population-level patterns.
- Translating a real research question — the effect of forestry intensity on wildlife space use — into a testable computational model.
- Parameter-sweep experimental design with replicates, and honest, iterative interpretation of simulation output (the original hypothesis was revised after the data showed a clearer, opposite pattern).
- Direct familiarity with the host department's actual research context and priorities.

## Future extension

Predator–prey dynamics (wolf/lynx interaction with herbivores) are a natural next step and are also core to Grimsö's research, but were intentionally left out of this build to keep scope realistic within a short build window. A natural extension would add a predator agent type and examine how predation risk interacts with the fragmentation effect already observed here — for example, whether herbivores in fragmented, high-logging landscapes become more vulnerable to predation due to reduced access to safe reserve areas.