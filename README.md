# Flaine Flow 🏂

Independent experimental piste map of Flaine / Grand Massif.

## Current status
The basemap app and extraction workflow are committed. **Pistes will not appear until the dataset workflow successfully generates `pistes.geojson`.** We have not verified a successful run yet.

## Build piste data
Open **Actions → Build Flaine piste dataset → Run workflow**. The workflow extracts OSM downhill piste ways and aerialway ways through public Overpass APIs, validates that a meaningful number of pistes exist, and commits `pistes.geojson`. On failure, it does not create fake geometry. For workflow commits, repository Actions workflow permissions must allow read/write.

## Publish
In **Settings → Pages**, choose **Deploy from branch → main → /(root)**. This is a public prototype.

## Licence, attribution and safety
Piste geometry is © OpenStreetMap contributors, licensed under ODbL: https://www.openstreetmap.org/copyright . Retain attribution and comply with applicable ODbL database redistribution/share-alike obligations. Basemap by OpenFreeMap / OpenMapTiles, mapping library MapLibre GL JS (BSD-3-Clause). Do not copy official Grand Massif map artwork. Not affiliated with the resort.

Community-maintained piste geometry may be incomplete, out of date, or inaccurate. This app has no verified real-time closures or conditions and is **not** a certified navigation or safety system. Follow resort signs and official operational information.
