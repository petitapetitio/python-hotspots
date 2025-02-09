from pathlib import Path
import json

import pandas as pd
import plotly.express as px


def read_complexity(filepath) -> pd.DataFrame:
    with open(filepath) as f:
        d = json.load(f)
        rows = []
        for filename, file_stats in d.items():
            if "error" in file_stats:
                continue
            nb_elements = len(file_stats)
            file_complexity = 0
            for component in file_stats:
                file_complexity += component['complexity'] / nb_elements
            rows.append((filename, file_complexity))

    return pd.DataFrame(rows, columns=["filename", "cyclomatic_complexity"])


churns = pd.read_csv("churn.csv")[["filename", "churn"]]

locs = pd.read_csv("loc.csv")[["filename", "code"]].rename(columns={"code": "loc"}).dropna()
locs["filename"] = locs["filename"].apply(lambda path: Path(path).as_posix())
hotspots = pd.merge(churns, locs, on="filename")
fig = px.scatter(hotspots, "churn", "loc", hover_data="filename")
fig.write_html("hotspots_with_loc.html")

ccs = read_complexity("complexity.json")
hotspots = pd.merge(churns, ccs, on="filename")
fig = px.scatter(hotspots, "churn", "cyclomatic_complexity", hover_data="filename")
fig.write_html("hotspots_with_cyclomatic_complexity.html")
