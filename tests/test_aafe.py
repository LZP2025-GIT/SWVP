import os
from src.aafe.aafe_engine import AAFEEngine

def test_engine_load():
    here = os.path.dirname(__file__)
    cfg = os.path.join(here, "..", "src", "aafe", "aafe_config.yaml")
    eng = AAFEEngine.from_yaml(cfg)
    assert 0.0 < eng.prev_posterior < 1.0
