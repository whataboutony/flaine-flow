#!/usr/bin/env python3
"""Build a static 30 m Copernicus GLO-30 elevation profile for Serpentine.\nSamples the canonical centreline at approximately 25 m spacing.\n"""
import json, math, tempfile, urllib.request
from pathlib import Path
import rasterio

ROOT=Path(__file__).resolve().parents[1]
PISTES=ROOT/"pistes.geojson"
OUT=ROOT/"data"/"serpentine-elevation-cop30.json"
ORDER=[828925195,718343867,1223500519,30160803,30791531]
SPACING_M=25.0
TILE_URLS={
 45:"https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N45_00_E006_00_DEM/Copernicus_DSM_COG_10_N45_00_E006_00_DEM.tif",
 46:"https://copernicus-dem-30m.s3.eu-central-1.amazonaws.com/Copernicus_DSM_COG_10_N46_00_E006_00_DEM/Copernicus_DSM_COG_10_N46_00_E006_00_DEM.tif",
}

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
# Serpentine crosses the 46°N tile boundary. Load every required latitude tile
# and sample each point from its containing one-degree COP30 raster.
tile_files={}
datasets={}
try:
 for lat_deg,url in TILE_URLS.items():
  tmp=tempfile.NamedTemporaryFile(suffix=f"-N{lat_deg}.tif",delete=False)
  tmp.close(); urllib.request.urlretrieve(url,tmp.name); tile_files[lat_deg]=tmp.name
  datasets[lat_deg]=rasterio.open(tmp.name)
 elev=[]
 for lon,lat in pts:
  lat_deg=math.floor(lat)
  ds=datasets.get(lat_deg)
  if ds is None: raise RuntimeError(f"No COP30 tile loaded for latitude {lat}")
  val=float(next(ds.sample([(lon,lat)]))[0])
  if not math.isfinite(val) or val<=0:
   raise RuntimeError(f"Invalid COP30 elevation {val} at {lon},{lat} from N{lat_deg} tile")
  elev.append(val)
finally:
 for ds in datasets.values(): ds.close()
 for path in tile_files.values():
  try: Path(path).unlink()
  except FileNotFoundError: pass
dist=[0.]
for a,b in zip(pts,pts[1:]): dist.append(dist[-1]+hav(a,b))
samples=[{"distance_m":round(d,1),"lon":round(p[0],7),"lat":round(p[1],7),"elevation_m":round(z,1)} for d,p,z in zip(dist,pts,elev)]
payload={"piste":"Serpentine","source":"Copernicus DEM GLO-30 Public (AWS Open Data, 2021 release)","model":"DSM","resolution_m":30,"sample_spacing_m":SPACING_M,"raw_geometry_vertices":len(line),"sample_count":len(samples),"mapped_distance_m":round(dist[-1],1),"tiles":["N45E006","N46E006"],"validation":{"min_elevation_m":round(min(elev),1),"max_elevation_m":round(max(elev),1),"zero_or_invalid_samples":sum(1 for z in elev if not math.isfinite(z) or z<=0)},"samples":samples}
OUT.parent.mkdir(exist_ok=True); OUT.write_text(json.dumps(payload,indent=2)+"\n")
print(f"Wrote {OUT}: {len(samples)} samples over {dist[-1]/1000:.3f} km")
