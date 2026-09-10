"""Run notebooks/NN_*.ipynb through papermill, in numeric order, into runs/.

Each notebook gets its own papermill.execute_notebook() call, so each one
gets a fresh kernel process. Stops at the first failing notebook and
reports which cell failed.

Usage:
    python tools/run_pipeline.py                    # run every notebook
    python tools/run_pipeline.py --only 03           # run just step 03
    python tools/run_pipeline.py --from 05            # run step 05 onward
    python tools/run_pipeline.py -p threshold 0.8     # override a parameter
    python tools/run_pipeline.py --scenario scenarios/climate.yaml
    python tools/run_pipeline.py --scenario scenarios/climate.yaml --only 04

--scenario FILE points to a YAML or JSON mapping of scenario name to a
dict of parameter overrides, for example:

    baseline: {climate_scenario: ssp245, staffing_ratio: mid}
    high_growth: {climate_scenario: ssp585, staffing_ratio: high}

The selected notebooks (all of them, or whatever --only/--from narrows
it to) run once per scenario, with that scenario's parameters merged
over any -p overrides, into runs/<scenario_name>/ instead of runs/.
"""

import argparse
import glob
import json
import os
import sys

import papermill as pm
from papermill.exceptions import PapermillExecutionError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOKS = os.path.join(ROOT, "notebooks")
RUNS = os.path.join(ROOT, "runs")


def discover_notebooks():
    paths = sorted(glob.glob(os.path.join(NOTEBOOKS, "[0-9][0-9]_*.ipynb")))
    return [(os.path.basename(p)[:2], p) for p in paths]


def select_notebooks(only, from_step):
    notebooks = discover_notebooks()
    if only:
        notebooks = [(n, p) for n, p in notebooks if n == only]
    elif from_step:
        notebooks = [(n, p) for n, p in notebooks if n >= from_step]
    return notebooks


def run_one(path, parameters, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(path))
    print(f"--- running {os.path.basename(path)} ---")
    try:
        pm.execute_notebook(
            path,
            output_path,
            parameters=parameters or None,
            progress_bar=False,
            cwd=ROOT,
        )
    except PapermillExecutionError as e:
        print(
            f"FAILED: {os.path.basename(path)} cell {e.cell_index} "
            f"(execution count {e.exec_count}): {e.ename}: {e.evalue}",
            file=sys.stderr,
        )
        return False
    print(f"ok -> {os.path.relpath(output_path, ROOT)}")
    return True


def coerce(value):
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            pass
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    return value


def parse_parameters(pairs):
    return {name: coerce(value) for name, value in pairs}


def load_scenario_file(path):
    with open(path, encoding="utf-8") as f:
        if path.endswith((".yaml", ".yml")):
            import yaml

            return yaml.safe_load(f)
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="run only this step number, e.g. 03")
    parser.add_argument("--from", dest="from_step", help="run this step number onward")
    parser.add_argument(
        "-p", "--parameter", nargs=2, action="append", default=[],
        metavar=("NAME", "VALUE"), help="override a notebook parameter",
    )
    parser.add_argument("--scenario", help="YAML or JSON file of named parameter sets")
    args = parser.parse_args()

    if args.only and args.from_step:
        parser.error("--only and --from are mutually exclusive")

    base_parameters = parse_parameters(args.parameter)
    notebooks = select_notebooks(args.only, args.from_step)
    if not notebooks:
        print("No matching notebooks found.", file=sys.stderr)
        sys.exit(1)

    if args.scenario:
        scenario_sets = load_scenario_file(args.scenario)
        for set_name, set_parameters in scenario_sets.items():
            merged = {**base_parameters, **set_parameters}
            output_dir = os.path.join(RUNS, set_name)
            print(f"=== scenario: {set_name} ===")
            for _, path in notebooks:
                if not run_one(path, merged, output_dir):
                    sys.exit(1)
        return

    for _, path in notebooks:
        if not run_one(path, base_parameters, RUNS):
            sys.exit(1)


if __name__ == "__main__":
    main()
