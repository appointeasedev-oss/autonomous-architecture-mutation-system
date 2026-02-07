# Kaggle execution lane

This folder contains the Kaggle notebook template used to run training jobs.

Workflow:
1. GitHub prepares an experiment bundle (spec + generated model + config).
2. Kaggle pulls the bundle, trains, and writes `results.json`.
3. GitHub ingests results and decides whether to accept the mutation.
