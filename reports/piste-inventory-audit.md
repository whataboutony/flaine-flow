# Flaine Flow — preliminary piste inventory audit

Generated 2026-10-14 from the checked-in `pistes.geojson`. **This is an OSM inventory audit, not an official piste match.** No changes to routing or piste geometry were made.

## Source data

- Total geographic features: **593**
- Piste line segments: **513**
- Lift line segments: **80**
- Distinct non-empty piste names (exact spelling): **157**
- Unnamed piste segments: **148**
- Names with multiple OSM difficulty values: **14**

### Segment difficulty breakdown (NOT piste counts)

| OSM difficulty | Segment count | Approximate French display colour |
|---|---:|---|
| novice | 144 | green |
| easy | 214 | blue |
| intermediate | 106 | red |
| advanced | 31 | black |
| freeride | 9 | off-piste / check |
| unknown | 9 | unverified |

## Official benchmark (not yet reconciled)

Flaine's resort site states **64 pistes and 24 lifts**. Its 2025/26 guide states **139 marked runs and 62 lifts** for Grand Massif. The Grand Massif trail-map page instead states **138 slopes and 60 lifts**, while the 2026/27 Flaine skipass page states **139 marked runs and 60 lifts**. These are inconsistent official totals; we must establish a season-specific named inventory before treating any figure as a pass/fail target.

Sources:
- https://www.flaine.com/en/ski-area/
- https://www.flaine.com/wp-content/uploads/2025/07/FLAINE_Guide2026-EN-MD.pdf
- https://www.grand-massif.com/en/trail-map/
- https://www.flaine.com/en/skipasses/

## Priority manual checks

**Names tagged with conflicting difficulties** (may represent legitimate shared segments, variant branches, or mapping errors):

- Chamois (intermediate, advanced)
- Stade (intermediate, novice)
- Biollaire (easy, novice)
- Blanchot (easy, intermediate)
- Sairon (easy, novice)
- Labérieu (intermediate, novice, easy)
- Cascades (intermediate, novice)
- Bergin (intermediate, novice, easy)
- Almandine (intermediate, easy)
- Combe de Véret (advanced, easy)
- Sarbotte (easy, intermediate)
- Martre (novice, easy)
- Plateau (intermediate, novice)
- Charnia (easy, novice)

**Why raw counts do not match:** The current extraction uses a broad rectangular bounding box covering more than Flaine. Some official runs have multiple OSM segments, some segments are unnamed, OSM names may differ from official names, and pistes may include connectors, freeride itineraries and variants not counted by the resort. A unique OSM name is **not** proof of a unique official piste.

## Next verification work

1. Obtain a **2026/27 named piste and lift inventory** from official Grand Massif/Flaine information, retaining source and season.
2. Normalize name variants, accents, aliases, and piste vs connector vs freeride classifications without destroying the original OSM tags.
3. Assign each OSM way to Flaine / Les Carroz / Morillon / Samoëns / Sixt using verified resort boundaries, not a crude latitude-longitude split.
4. Match official names to OSM groups with confidence levels (verified, possible, missing, extra); review mixed difficulties and unnamed sections.
5. Only then publish a reconciliation rate and begin navigation QA. Never manufacture a match just to hit the official headline total.

**Safety:** This audit is not evidence that any route is open, safe, navigable, or correctly classified. Check official resort information and signage.
