# Serpentine geometry QA — 2026-10-14

**Result: topology checks PASS; official alignment NOT YET VERIFIED. Do not enable routing.**

## Sources
- OSM-derived `pistes.geojson` in this repository (community-maintained data).
- Flaine 2025/26 official piste map: https://www.flaine.com/wp-content/uploads/2025/11/GM_PlanPistes_25_26_HD.pdf
- Flaine 2025/26 press pack identifies Serpentine as the blue piste on Grandes Platières and advertises 7 km: https://www.flaine.com/wp-content/uploads/2025/09/FLAINE-DOSSIER-DE-PRESSE_26_FR.pdf

## Measured canonical candidate
Ordered OSM way IDs, **not** independently surveyed:
`828925195 → 718343867 → 1223500519 → 30160803 → 30791531`

- 5 connected LineStrings; 58 joined coordinate vertices.
- Consecutive endpoints agree exactly (no synthetic connecting edges).
- Sum of geographic segment lengths: **4.746 km**.
- No proper self-crossings among nonadjacent line segments (planar intersection check).
- First coordinate: `[6.7226793, 45.9843396]`.
- Last coordinate: `[6.6965799, 46.0064917]`.
- Raw Serpentine also includes 2 disconnected short ways and 2 closed boundary-like ways; these were omitted from the candidate. Omission does not prove they are irrelevant to the official route.
- UI uses 35 m Douglas–Peucker simplification **for display only**. The original joined vertices, not the simplified preview, must be used for subsequent QA/routing calculations.

## Independent assessment
The candidate runs broadly from the Grandes Platières side towards Flaine, consistent with the official sector description. The official piste map is a schematic illustration, **not a georeferenced surveyed centreline**. It cannot certify metre-level spatial alignment. The advertised 7 km and OSM-measured 4.746 km remain distinct metrics; we have not established why they differ.

## Unresolved blockers to a VERIFIED label
1. Match the start and finish to identifiable lift terminals or piste junctions on a georeferenced reference.
2. Check the route corridor and each bend against independent GPS track / authoritative geospatial data.
3. Confirm downhill direction with elevation data and test for uphill/flat sections.
4. Review omitted OSM objects and ensure no real branch is missing.
5. Confirm any changes for the 2026/27 season.

**Decision:** `topology_checked_geometry_unverified`. Do not claim safe or certified navigation.

## Short Serpentine object review — pause point (2026-10-14)

Reviewed OSM ways `1257254973` and `1257254974` rather than deleting them as artefacts.

- `1257254973`: a two-point ~172 m blue Serpentine line. It touches the selected Serpentine way `30791531` and Cristal `30791529`. It is also within ~19 m of Belzébuth.
- `1257254974`: a two-point ~99 m blue Serpentine line. It touches selected Serpentine `30791531`, Cristal, Émeraude, Belzébuth and Lucifer in the OSM geometry; Tanzanite is within ~3 m.

These objects sit in a dense piste-junction area. Their topology is therefore consistent with **connector/branch geometry**, rather than random detached artefacts. But because this conclusion is derived from the same OSM database, it is not independent evidence that each mapped crossing is physically skiable or officially part of Serpentine.

**Decision at pause:** keep both raw objects and their provenance; exclude them from the single canonical display centreline for now; mark them `branch_candidate_requires_independent_confirmation`. Do not delete, merge, or use them for routing until independently checked.
