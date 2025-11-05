# Southwest Verification Project (SWVP)
**Testing Cross-Domain APC Formation in a Multi-Sensor Corridor**  
Built on the Unified Archetypal Bayesian Theory (UABT) and the Adaptive APC Forecast Engine (AAFE).

**Author:** Zachariah Paul Laing  
**License:** CC-BY-SA 4.0  
**Status:** Phase I public release

## Overview
SWVP implements a corridor-scale, multi-sensor pipeline (Tucson→White Sands→Las Vegas) to quantify and forecast
Anomalus Phenomena Clusters (APCs). It couples UABT domain likelihoods (S₁–S₉) with AAFE’s adaptive posterior drift:

Posterior_Odds(t+Δt) = Posterior_Odds(t) × Π(LR_i,t) × Π(ω_j,t) × M_F5(t) × [1 + α(dΔ/dt)]
P_posterior = Posterior_Odds / (1 + Posterior_Odds)


## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run a corridor simulation + fusion + forecast
python src/swvp_demo.py --steps 2000 --seed 42
