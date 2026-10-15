# Flaine Flow — Project Status

**Checkpoint:** 2026-10-14  
**Purpose:** Read this file first whenever work on Flaine Flow resumes. Update it whenever the project pauses.

## Product goal
Build an independent, Google-Maps-like ski/snowboard navigation prototype for Flaine / Grand Massif. Long-term routing should understand pistes, lifts, difficulty and snowboard-specific costs such as flat traverses. **Routing is intentionally paused until piste geometry is sufficiently cleaned and validated.**

## Live prototype
GitHub Pages: https://whataboutony.github.io/flaine-flow/

The current map uses MapLibre/OpenFreeMap plus the repository's OSM-derived `pistes.geojson`. It includes named-run selection, difficulty/lift controls, location/Flaine-centre controls, and a Piste QA panel.

## Data snapshot
- `pistes.geojson`: 593 mapped features from the successful OSM extraction.
- 513 piste segments and 80 lift segments.
- 157 distinct named pistes in the extracted Grand Massif area, plus unnamed segments.
- These are mapping segments, **not official unique-piste counts**.
- Raw/community geometry must not be treated as live operational status or certified navigation.

## Validation workflow
For each piste:
1. Preserve raw OSM geometry and OSM IDs for provenance.
2. Identify centreline candidates vs boundary/area/branch artefacts.
3. Check connectivity, gaps, loops/self-crossings and measured length.
4. Compare name/difficulty with official resort material.
5. Compare bends, junctions, endpoints and downhill direction with independent/georeferenced evidence where available.
6. Keep status explicit: unreviewed → provisional/topology checked → geometry verified only when evidence supports it.
7. Never invent geometry merely to match an advertised length.

## Serpentine — current checkpoint
**Status: TOPOLOGY CHECKED / GEOMETRY NOT VERIFIED / NOT FOR ROUTING.**

Official/source attributes currently recorded:
- Name: Serpentine.
- Difficulty: blue.
- Official 2025/26 material advertises 7 km.
- OSM and independent OSM-based measurements are around 4.7–4.8 km. Treat advertised and mapped lengths as different metrics; do **not** add 2.25 km of invented geometry.

### Canonical candidate
Ordered OSM ways:
`828925195 → 718343867 → 1223500519 → 30160803 → 30791531`

QA results:
- 5 exact-connected LineStrings.
- 58 original joined vertices.
- Geographic length: ~4.746 km.
- No synthetic connector edges.
- No proper self-crossings detected.
- Candidate endpoints: `[6.7226793,45.9843396]` → `[6.6965799,46.0064917]`.
- UI currently applies 35 m Douglas–Peucker simplification **for display only**. Validation/routing must use original geometry, not the simplified preview.

### Raw Serpentine objects not in canonical display line
- `1257254973`: ~172 m, blue. Touches canonical Serpentine and Cristal in OSM; near Belzébuth. Keep as `branch_candidate_requires_independent_confirmation`.
- `1257254974`: ~99 m, blue. Touches canonical Serpentine plus Cristal/Émeraude/Belzébuth/Lucifer in OSM; Tanzanite is nearby. Keep as `branch_candidate_requires_independent_confirmation`.
- `1485662236`, `1485664434`: closed Serpentine LineStrings. Excluded from centreline candidate; likely boundary/area-like geometry but **not independently confirmed**.

Important correction from earlier work: the two short ways are not simply random isolated artefacts. Endpoint-only component analysis made them appear isolated, but later proximity/junction analysis showed they touch the main route at interior locations.

### Junction audit
The candidate intersects or closely approaches numerous mapped features including Méphisto supérieure, Amethyste, Faust, Lucifer, Démon, Cristal, Cascades, Zéolite, Jonction, Turquoise, Baudroie, Bissac and nearby lifts. These checks come from the **same OSM database**, so they establish internal topology consistency only. They do not prove a crossing is an official or physically skiable junction.

### Remaining Serpentine blockers
- Independently confirm the actual route corridor/bends.
- Confirm start and finish against identifiable/georeferenced piste/lift junctions.
- Confirm the two short branch candidates.
- Add elevation/DEM data and verify downhill direction, slope and flat/uphill sections.
- Check for 2026/27 changes.
- Only then consider `geometry_verified=true`.

Detailed audit: `reports/serpentine-geometry-qa.md`.

## Other piste reconciliation
A Flaine candidate set exists in `data/reconciliation-2025-26.json`. Serpentine is the first piste receiving detailed geometry QA. Tourmaline and Cascades have preliminary source work but should **not** be treated as fully geometry-verified. Cascades has unresolved source differences around difficulty classification.

## Architecture / important files
- `index.html` — current prototype UI and Serpentine provisional display-centreline logic.
- `pistes.geojson` — raw OSM-derived piste/lift features.
- `scripts/build_pistes.py` — Overpass extraction/build script.
- `.github/workflows/build-pistes.yml` — dataset workflow.
- `data/reconciliation-2025-26.json` — piste reconciliation/QA metadata.
- `reports/piste-inventory-audit.md` — inventory audit.
- `reports/serpentine-geometry-qa.md` — detailed Serpentine audit.
- `PROJECT_STATUS.md` — this handover/checkpoint.

## Known technical debt
- Serpentine cleaned geometry is currently generated inside `index.html`; future cleaned pistes should move to a dedicated canonical/validated GeoJSON layer rather than accumulating hard-coded UI logic.
- Build script currently preserves limited OSM properties. Preserve useful raw tags (area/grooming/ref/oneway etc.) before large-scale centreline extraction.
- No routing graph currently exists in the repo.
- No DEM/elevation pipeline exists yet.
- Official piste map is schematic and should be used as a reference, not copied as map artwork.
- GitHub Pages may show cancelled checks on superseded commits when newer deployments replace them; do not confuse that with piste-QA failure.

## Elevation experiment — 2026-10-16

`index.html` now contains an experimental Serpentine terrain-elevation profile. When Serpentine is selected, the browser batches its 58 original canonical vertices to the Open-Meteo elevation endpoint (Copernicus GLO-90 terrain model), plots elevation against cumulative geodesic distance, reports start/end/net elevation, and flags vertex-to-vertex model intervals above +2% as uphill and −3% to +2% as flat-ish. This is a first routing experiment only: 90 m DEM resolution is too coarse for metre-level piste features, and the current flags are not yet snowboard-routing truth. The map remains usable if the elevation service fails. A future production build should precompute elevation server/build-side, preferably from a finer DEM, rather than depend on a browser API call.

## Exact next action when resuming
**Do not start Tourmaline immediately.** First finish Serpentine's independent geometry evidence:
1. Find a trustworthy independent/georeferenced trace or authoritative spatial reference for Serpentine's bends/endpoints.
2. If unavailable, add DEM/elevation validation and explicitly leave bend alignment unverified rather than guessing.
3. Resolve the two short branch candidates.
4. If evidence is sufficient, create a dedicated canonical piste GeoJSON feature with provenance and verification metadata.
5. Only after Serpentine's process is stable, apply the same QA workflow to Tourmaline.

## Safety / licensing
Retain © OpenStreetMap contributors (ODbL), OpenFreeMap/OpenMapTiles attribution and the independent-project disclaimer. Never present static OSM data as live piste status. The prototype is not certified navigation; resort signs, closures, weather and official operational information take precedence.


## Product differentiation checkpoint — 2026-10-14

Competitor review changed the positioning. Existing ski-navigation products already advertise combinations of digital piste maps, turn-by-turn navigation, offline maps, ability-based routing, group tracking and, in some cases, snowboard/flat-aware routing. **Flaine Flow should not assume that basic piste navigation or flat avoidance alone is a moat.**

Current product hypothesis: **“Navigation that understands how you ride.”**

Promising differentiation hypotheses to test:
- **Riding-style routing:** optimise not just difficulty/time but the experience — e.g. carving-friendly consistent gradients, relaxed cruising, progression, exploration, snowboard-friendly terrain, fewer awkward traverses/junctions.
- **Explainable routing:** show why one route is recommended over another (e.g. +5 minutes but avoids a long flat and has more continuous downhill terrain). Routing should expose meaningful costs rather than behave as a black box.
- **Time-aware “Get Me Home”:** eventually account for location, ability, estimated travel time, critical lift connections and trustworthy lift closing/operational data. Never make live/safety claims without reliable operational feeds.
- **Mixed-ability group routing:** find a route suitable for everyone or allow riders to take different suitable pistes and reconverge at a shared lift/meeting point.
- **Personalised piste recommendations:** eventually learn rider preferences from explicit feedback such as too flat, great for carving, narrow, crowded, beginner-friendly, etc. Start with transparent rules; do not pretend to have a trained recommendation model without data.

Potential long-term structure:
1. **Reliable mountain-routing engine** — canonical piste geometry, junctions, lifts, elevation/direction, constraints and provenance.
2. **Personalised navigation layer** — rider style/preferences, route explanations, group needs and eventually contextual recommendations.

Key strategic test before major expansion: **Does an existing competitor already solve the user's real Flaine navigation problem well enough?** Test competitor apps in/for Flaine and document exactly where they succeed or fail, especially for snowboard-specific routing and route explainability. Use the observed gaps — not assumptions — to decide Flaine Flow's differentiation.

Scaling hypothesis: Flaine is the proving ground, not the final market. If the canonical-data + routing pipeline becomes repeatable, additional French resorts should become an onboarding/data-QA problem rather than a rewrite. Do not scale resort coverage until the Flaine validation/routing workflow is robust.
