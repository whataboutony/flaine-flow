#!/usr/bin/env python3
"""Build a Flaine-area ski GeoJSON from OpenStreetMap via public Overpass APIs."""
import json, os, time, urllib.parse, urllib.request
from pathlib import Path

BBOX = (45.945, 6.58, 46.085, 6.83)  # south, west, north, east; includes neighbouring Grand Massif
QUERY = """[out:json][timeout:120];
(
 way["piste:type"="downhill"](%s,%s,%s,%s);
 way["aerialway"](%s,%s,%s,%s);
);
out geom;""" % (BBOX + BBOX)
SERVERS = ["https://overpass.kumi.systems/api/interpreter",
           "https://overpass.nchc.org.tw/api/interpreter",
           "https://overpass-api.de/api/interpreter"]
def fetch():
    errors=[]
    for server in SERVERS:
        try:
            request=urllib.request.Request(server, data=urllib.parse.urlencode({"data":QUERY}).encode(),
                headers={"User-Agent":"FlaineFlow/0.1 (independent open ski map; https://github.com/whataboutony/flaine-flow)",
                         "Accept":"application/json"})
            with urllib.request.urlopen(request, timeout=150) as response:
                obj=json.load(response)
            if not isinstance(obj.get("elements"),list): raise ValueError("No elements array")
            if len(obj["elements"])<20: raise ValueError("Unexpectedly small dataset")
            return obj
        except Exception as exc:
            errors.append(f"{server}: {exc}")
            print(errors[-1],flush=True)
            time.sleep(2)
    raise RuntimeError("No Overpass endpoint returned a valid dataset. " + " | ".join(errors))

def build(raw):
    features=[]
    for item in raw["elements"]:
        tags=item.get("tags",{})
        coords=[[p["lon"],p["lat"]] for p in item.get("geometry",[]) if "lat" in p and "lon" in p]
        if len(coords)<2: continue
        kind="lift" if tags.get("aerialway") else "piste"
        if kind=="lift" and tags.get("aerialway") in ("station","pylon"): continue
        features.append({"type":"Feature","id":f'way/{item["id"]}',
            "geometry":{"type":"LineString","coordinates":coords},
            "properties":{"name":tags.get("piste:name") or tags.get("name") or "Unnamed",
              "kind":kind,"difficulty":tags.get("piste:difficulty","unknown"),
              "lift_type":tags.get("aerialway",""),"osm_id":item["id"]}})
    if sum(f["properties"]["kind"]=="piste" for f in features)<15:
        raise RuntimeError("Too few pistes; refusing to publish an incomplete extract")
    return {"type":"FeatureCollection","features":features}

if __name__=="__main__":
    result=build(fetch())
    output=Path("pistes.geojson")
    tmp=output.with_suffix(".geojson.tmp")
    tmp.write_text(json.dumps(result,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    os.replace(tmp,output)
    print(f"Wrote {len(result['features'])} features to {output}")
