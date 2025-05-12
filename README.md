
# Network Dynamic Population Model

This project simulates two types of processes on a graph network: Information cascades and COVID-19 like infection spread. It provides options for visualising each day's progression and the final state of the network.

## Features

* Load graph structures from GML files.
* Simulate:
  * Information Cascades based on node thresholds.
  * COVID-19 Spread using infection probability and recovery timelines.
* Supports:
  * Sheltered nodes
  * Vaccinated nodes
* Interactive visualization of graph state over time.
* Line plot of daily new infections.
* Final network state visualization.

## Requirements
* Python 3.x
* `networkx`
* `matplotlib`

Install Dependencies:
```bash
pip install networkx matplotlib
```

## Usage

```bash
python simulation.py <graph_file> --action {cascade,covid} --initiator <node_ids> [options]
```
### Positional Arguments
`graph_file`: Path to the `.gml` file containing the graph
### Required Flags
* `--action`: Simulation Mode (`cascade` or `covid`) representing cascading behaviour or COVID-19 spread
* `--initiator`: Comma-separated list of initial infected/seed node IDs
### Optional Flags
* `--threshold`: Threshold (0-1) for cascade adoption (defalut: 0.5)
* `--probability_of_infection`: Infection probability per contact for CPVID (default: 0.1)
* `--lifespan`: Number of days before infected nodes recover (default: 10)
* `--shelter`: Proportion of nodes that are sheltered and cannot be infected (default: 0.0)
* `--vaccination`: PRoportion of ndoes that are vaccinated and immune (default: 0.0)
* `--interactive`: Show graph update after every round (interactive visualisation)
* `--plot`: Plot a line graph of daily new infections

### Example
```bash
python ./dynamic_population.py graph.gml --action covid --initiator 3,4 --probability_of_infection 0.02 --lifespan 100 --shelter 0.3 --vaccination 0.24
```

This runs a COVID simulation on `sample_graph.gml` with:
* Initial infected nodes: 0 and 1
* Infection probability: 20%
* Recovery time: 7 days
* 10% of the population sheltered
* 20% vaccinated
* Interactive daily visualization and a summary plot

## Output
* **Graph visualizations** (if `--interactive` is used): Day-by-day infection spread.
* **Line plot** (if `--plot` is used): Daily new infection counts.
* **Final network state:** Color-coded graph showing final node statuses.
