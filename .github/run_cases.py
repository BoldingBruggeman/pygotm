import argparse
from pathlib import Path

import numpy as np

import pygotm._pygotm

parser = argparse.ArgumentParser()
parser.add_argument("cases_dir", type=str, help="Path to the directory containing GOTM cases")
args = parser.parse_args()


cases_path = Path(args.cases_dir)
for case_dir in cases_path.iterdir():
    if case_dir.is_dir() and (case_dir / "gotm.yaml").exists():
        nlev = np.random.randint(10, 100)
        print(f"Running case {case_dir.name} with nlev {nlev}")
        pygotm._pygotm.Mixing(nlev, yaml_path=str(case_dir / "gotm.yaml").encode("ascii"))