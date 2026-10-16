#!/usr/bin/env python3
"""Build a static 30 m Copernicus GLO-30 elevation profile for Serpentine."""
import json, math, tempfile, urllib.request
from pathlib import Path
import rasterio

ROOT=Path(__file__).resolve().parents[1]
PISTES=ROOT/"pistes.geojson"
OUT=ROOT/"data"/"serpentine-elevation-cop30.json"
ORDER=[828925195,718343867,1223500519,30160803,30791531]
SPACING_M=25.0
TILE_URL="https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N45_00_E006_00_DEM/Copernicus_DSM_COG_10_N45_00_E006_00_DEM.tif"

def hav(a,b):
 r=6371000.; p1,p2=map(math.radians,[a[1],b[1]]); dp=math.radians(b[1]-a[1]); dl=math.radians(b[0]-a[0])
 h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
 return 2*r*math.asin(math.sqrt(h))

def join(data):
 fs={int(f["properties"]["osm_id"]):f for f in data["features"] if f["properties"].get("osm_id")}
 out=[]
 for oid in ORDER:
  c=fs[oid]["geometry"]["coordinates"]
  if out:
   if hav(out[-1],c[-1])<hav(out[-1],c[0]): c=list(reversed(c))
   if hav(out[-1],c[0])>5: raise RuntimeError("Serpentine chain gap >5 m")
   out.extend(c[1:])
  else: out.extend(c)
 return out

def densify(line,spacing):
 out=[line[0]]; carry=0.
 for a,b in zip(line,line[1:]):
  seg=hav(a,b)
  if seg==0: continue
  pos=spacing-carry if carry else spacing
  while pos<seg:
   t=pos/seg; out.append([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]); pos+=spacing
  carry=(carry+seg)%spacing
  if carry<1e-6: carry=0.
 out.append(line[-1]); return out

data=json.loads(PISTES.read_text())
line=join(data); pts=densify(line,SPACING_M)
with tempfile.NamedTemporaryFile(suffix=".tif") as tmp:
 urllib.request.urlretrieve(TILE_URL,tmp.name)
 with rasterio.open(tmp.name) as ds:
  elev=[float(v[0]) for v in ds.sample([(p[0],p[1]) for p in pts])]
dist=[0.]
for a,b in zip(pts,pts[1:]): dist.append(dist[-1]+hav(a,b))
samples=[{"distance_m":round(d,1),"lon":round(p[0],7),"lat":round(p[1],7),"elevation_m":round(z,1)} for d,p,z in zip(dist,pts,elev)]
payload={"piste":"Serpentine","source":"Copernicus DEM GLO-30 Public (AWS Open Data, 2021 release)","model":"DSM","resolution_m":30,"sample_spacing_m":SPACING_M,"raw_geometry_vertices":len(line),"sample_count":len(samples),"mapped_distance_m":round(dist[-1],1),"samples":samples}
OUT.parent.mkdir(exist_ok=True); OUT.write_text(json.dumps(payload,indent=2)+"\n")
print(f"Wrote {OUT}: {len(samples)} samples over {dist[-1]/1000:.3f} km")
