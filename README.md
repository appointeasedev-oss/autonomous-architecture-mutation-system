# Autonomous Architecture Mutation System

Autonomous Architecture Mutation System (AAMS) is an open-source system that evolves neural network architectures by mutating structured specs, generating model code, training micro-models, and evaluating results under strict safety rules.

## What this repository provides (initial skeleton)
- A repo layout for domain-specific architecture specs (language, vision, hybrid).
- A GitHub-first control loop for mutation, evaluation, and decision making.
- A Kaggle execution lane for GPU training jobs, separated from decision logic.
- A minimal runnable evolution cycle to prove the end-to-end loop locally.

## Execution model (GitHub + Kaggle)
**GitHub = brain (control + evolution)**
- Mutates architecture specs.
- Generates model code from specs.
- Applies safety rules and evaluates results.
- Accepts/rejects mutations and logs experiment history.

**Kaggle = muscle (training + compute)**
- Pulls the experiment bundle from GitHub.
- Trains micro/medium models.
- Uploads results back to GitHub for evaluation.

This separation keeps self-modification safe and auditable.

## Repository structure
```
.github/workflows/    # GitHub Actions (evolution + evaluation)
meta_controller/       # LLM-driven mutation planner (future)
domains/               # Domain-specific schemas and baselines
  language/
  vision/
  hybrid/
specs/                 # Active and historical architecture specs
aams/                  # Core loop (mutate → train → evaluate → log)
compiler/              # Spec → model code generation
trainer/               # Micro-training pipelines
evaluator/             # Fitness scoring and regression checks
evolution/             # Mutation engine and selection logic
docs_store/            # Curated docs + retrieval index
safety/                # Mutation limits + rollback rules
logs/                  # Experiment history and failure records
kaggle/                # Kaggle notebook + scripts for training
docs/                  # GitHub Pages metrics dashboard
```

> Note: Directories are scaffolded now. Implementation will be added iteratively.

## GitHub Actions (available)
- `evolve.yml`: orchestrates mutation and code generation (creates a pending spec + bundle).
- `dispatch_kaggle.yml`: uploads the experiment bundle and (optionally) sends it to Kaggle.
- `receive_results.yml`: stores Kaggle outputs into the repo for evaluation.
- `evaluate.yml`: accepts or rejects mutations and updates specs.

## Kaggle integration (ready for wiring)
Kaggle will be used only for training jobs. The notebook in `kaggle/` will:
1. Pull the experiment bundle.
2. Train the model.
3. Output metrics as `results.json`.
4. Push results back to GitHub.

## Run the local loop (minimal end-to-end)
1. Ensure you have Python 3.11+.
2. Run one evolution cycle:
   ```bash
   python -m aams.run_cycle --seed 7
   ```
3. View the latest metrics snapshot in `docs/metrics.json` (generated on each run).

## Auto-improve on GitHub
The `AAMS evolution loop` workflow runs every 5 minutes (GitHub's minimum schedule)
and on manual dispatch. Each run:
- Mutates the current spec.
- Writes a pending spec + experiment bundle.
- Commits and pushes changes back to the repo.

To complete the Kaggle loop:
1. Run `dispatch_kaggle.yml` to upload the latest bundle.
2. Execute the Kaggle notebook to train and generate `results.json`.
3. Commit `experiments/results/results.json` (or upload it via workflow).
4. Run `evaluate.yml` to accept/reject the mutation.

## GitHub Pages dashboard
The metrics dashboard lives in `docs/` and reads `docs/metrics.json`.
If you want a starter payload before running cycles, copy `docs/metrics.sample.json`
to `docs/metrics.json`.

To enable it:
1. Push the repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Save, then open the provided Pages URL.

## What you need to do next
1. **Decide the first domain to evolve** (language/vision/hybrid).
2. **Run local cycles** to populate logs and metrics.
3. **Enable GitHub Pages** so the dashboard is live.
4. **Add Kaggle credentials** and run `dispatch_kaggle.yml` once you're ready for GPU runs.

## Next steps
- Add initial domain schemas and baseline specs.
- Implement mutation grammar and safety rules.
- Create minimal training + evaluation loop.
- Wire up GitHub Actions + Kaggle notebook.
