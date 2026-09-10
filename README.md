# resort_plan

Planning analysis of Revelstoke Mountain Resort and the City of Revelstoke.
See [CLAUDE.md](CLAUDE.md) for the project rules and layout.

## Setup

Python 3.13, Windows, Git Bash.

```
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
nbstripout --install
```

`requirements.txt` is a pinned `pip freeze` of a plain venv. geopandas and
rasterio both ship PyPI wheels with GDAL bundled, which is enough for this
project (single machine, standard raster/vector formats, no exotic GDAL
drivers). geopandas's own docs recommend conda-forge for the broadest
dependency coverage, but that means installing conda first, which this
machine does not have, so a venv is the lighter path here.

`nbstripout` clears notebook outputs on commit so `notebooks/*.ipynb` never
carries executed output into git. `nbstripout --install` writes the git
filter to `.git/info/attributes`, which is local to this clone and is not
itself versioned, so re-run it after any fresh clone or venv rebuild.
