# AAMS Kaggle Notebook Template

This template is designed for a Kaggle notebook that trains the bundle created by `dispatch_kaggle.yml`.

## Steps
1. Download the experiment bundle artifact from GitHub.
2. Unpack it into the notebook working directory.
3. Load `arch_spec.json` + `train_config.json`.
4. Train a micro/medium model and capture metrics.
5. Write `results.json` with the fields: `loss`, `latency`, `params`, `seed`.
6. Push `results.json` back to the GitHub repo under `experiments/results/`.

## Minimal results.json shape
```json
{
  "loss": 2.91,
  "latency": 12.3,
  "params": 18400000,
  "seed": 7
}
```
