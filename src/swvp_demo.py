import argparse, os, random
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from fusion import combine_posteriors, tier_from_probs
from swvp_pipeline import SWVPPipeline

def synth_tick(domain_names, rng, simcfg):
    # baseline or spike?
    spike = (rng.random() < simcfg["spike_probability"])

    def pick_range(name):
        lo, hi = (simcfg["spike_LR_range"] if spike else simcfg["base_LR_range"])
        return rng.uniform(lo, hi)

    LRs = {d: pick_range(d) for d in domain_names}
    f5_lo, f5_hi = (simcfg["f5_range_spike"] if spike else simcfg["f5_range_baseline"])
    f5 = rng.uniform(f5_lo, f5_hi)
    return LRs, f5, spike

def main(steps, seed):
    here = os.path.dirname(__file__)
    aafe_cfg = os.path.join(here, "aafe", "aafe_config.yaml")
    params_path = os.path.join(here, "config", "model_params.yaml")
    with open(params_path, "r") as f:
        model_params = yaml.safe_load(f)

    pipeline = SWVPPipeline(aafe_cfg, params_path)

    # domain names from aafe_config
    import yaml as _yaml
    with open(aafe_cfg, "r") as f:
        raw = _yaml.safe_load(f)
    domain_names = list(raw["likelihoods"].keys())

    rng = random.Random(seed)
    rows = []
    for t in range(steps):
        LRs, f5, spike = synth_tick(domain_names, rng, model_params["simulation"])
        # fold nominal config multipliers:
        for k, v in raw["likelihoods"].items():
            LRs[k] *= float(v)
        out = pipeline.step(LRs, f5)

        # simple multi-domain combine heuristic (illustrative)
        p_list = [out["posterior"] * 0.9, out["posterior"] * 1.05, out["posterior"] * 1.1]
        p_combined = combine_posteriors(p_list)
        tier = tier_from_probs(
            p_single=out["posterior"],
            p_combined=p_combined,
            dual_threshold=model_params["fusion"]["dual_domain_threshold"],
            tri_threshold=model_params["fusion"]["tri_domain_threshold"],
        )
        rows.append({
            "t": out["t"], "posterior": out["posterior"], "drift": out["drift"],
            "M_F5": out["M_F5"], "flagged": out["flagged"], "p_combined": p_combined,
            "tier": tier, "spike_synthetic": int(spike), **{f"LR_{k}": v for k, v in LRs.items()}, "F5": f5
        })

    os.makedirs("outputs", exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv("outputs/swvp_stream.csv", index=False)
    df[df["tier"].isin(["Tier I","Tier II"])].to_csv("outputs/events_flagged.csv", index=False)

    # quick plot
    plt.figure(figsize=(10,4))
    plt.plot(df["t"], df["posterior"], label="Posterior")
    plt.plot(df["t"], df["p_combined"], label="P_combined", alpha=0.7)
    plt.axhline(model_params["fusion"]["dual_domain_threshold"], ls="--", label="Dual threshold")
    plt.axhline(model_params["fusion"]["tri_domain_threshold"], ls="--", label="Tri threshold")
    plt.xlabel("t"); plt.ylabel("Probability"); plt.title("SWVP Rolling Posterior")
    plt.legend(); plt.tight_layout()
    plt.savefig("outputs/posterior_map.png", dpi=160)
    print("Wrote outputs/swvp_stream.csv, outputs/events_flagged.csv, outputs/posterior_map.png")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    main(args.steps, args.seed)
