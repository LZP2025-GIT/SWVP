import os, yaml
from src.swvp_pipeline import SWVPPipeline

def test_pipeline_runs():
    here = os.path.dirname(__file__)
    aafe_cfg = os.path.join(here, "..", "src", "aafe", "aafe_config.yaml")
    params = os.path.join(here, "..", "src", "config", "model_params.yaml")
    p = SWVPPipeline(aafe_cfg, params)
    out = p.step({"S1_optical":1.1, "S2_em":1.05}, f5_verified_fraction=0.2)
    assert 0 <= out["posterior"] <= 1
