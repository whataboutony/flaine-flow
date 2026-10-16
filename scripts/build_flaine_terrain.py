#!/usr/bin/env python3
"""Build a compact real-terrain grid around Flaine from Copernicus GLO-30."""
import json, tempfile, urllib.request
from pathlib import Path
import rasterio
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"flaine-terrain-cop30.json"
# Flaine bowl + Grandes Platières / Grand Vans context. Keep v1 compact for browser rendering.
WEST,EAST,SOUTH,NORTH=6.64,6.76,45.965,46.035
COLS,ROWS=121,101
URLS={
45:"https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N45_00_E006_00_DEM/Copernicus_DSM_COG_10_N45_00_E006_00_DEM.tif",
46:"https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N46_00_E006_00_DEM/Copernicus_DSM_COG_10_N46_00_E006_00_DEM.tif"}
files={}; ds={}
try:
 for k,u in URLS.items():
  t=tempfile.NamedTemporaryFile(suffix=".tif",delete=False);t.close();urllib.request.urlretrieve(u,t.name);files[k]=t.name;ds[k]=rasterio.open(t.name)
 vals=[]
 for r in range(ROWS):
  lat=NORTH-(NORTH-SOUTH)*r/(ROWS-1); row=[]
  for c in range(COLS):
   lon=WEST+(EAST-WEST)*c/(COLS-1)
   candidates=[]
   for k,d in ds.items():
    b=d.bounds
    if b.left<=lon<=b.right and b.bottom<=lat<=b.top:
     v=float(next(d.sample([(lon,lat)],masked=True))[0])
     if v>0: candidates.append(v)
   if not candidates:
    for delta in (-5e-5,5e-5):
     for k,d in ds.items():
      b=d.bounds
      if b.left<=lon<=b.right and b.bottom<=lat+delta<=b.top:
       v=float(next(d.sample([(lon,lat+delta)],masked=True))[0])
       if v>0:candidates.append(v)
   if not candidates: raise RuntimeError(f"No DEM value {lon},{lat}")
   row.append(round(min(candidates),1))
  vals.append(row)
finally:
 for d in ds.values():d.close()
 for p in files.values():
  try:Path(p).unlink()
  except:pass
flat=[v for row in vals for v in row]
payload={"source":"Copernicus DEM GLO-30 Public (AWS Open Data, 2021 release)","model":"DSM","resolution_m":30,
"bounds":{"west":WEST,"east":EAST,"south":SOUTH,"north":NORTH},"cols":COLS,"rows":ROWS,
"min_elevation_m":min(flat),"max_elevation_m":max(flat),"elevations_m":vals}
OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(payload,separators=(",",":"))+"\n")
print(f"Wrote {OUT} {COLS}x{ROWS} {min(flat):.1f}-{max(flat):.1f}m")
