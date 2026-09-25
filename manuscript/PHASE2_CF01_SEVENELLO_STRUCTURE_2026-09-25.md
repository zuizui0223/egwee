# CFTQ0001 Sevenello structural-unit audit — 2026-09-25

This audit uses only source identifiers, exposure fields and treatment labels/counts.
No bee abundance, flower-number or seed-production values are read.

## Bee structural frame

- public bee transect rows: **20**
- unique source site labels: **12**
- unique site × crop sampling units: **13**
- site × crop units with both Edge and Core rows: **7**
- unique remnant-area values: **9**

Source site labels: Buntine, Latham, LathamPrivate, Maya, MayaPrivate, Milton, WA12427, WA12428, WA12429, WA12430, XantippeEast, XantippeTank

Edge/Core-paired site × crop units:
- Buntine | Canola | area=38.03 km2
- Buntine | Wheat | area=38.03 km2
- Maya | Canola | area=2.53 km2
- MayaPrivate | Canola | area=6.38 km2
- Milton | Wheat | area=4.14 km2
- XantippeEast | Wheat | area=2.6 km2
- XantippeTank | Canola | area=2.07 km2

## Plant structural frame

- public individual treatment rows: **2080**
- species × site × crop × transect structural rows: **52**
- plant-site labels: **9**
- treatment labels: Bag, BagSup, OP, OPSupp

- GORO: site×crop units=6; transect rows=12
- LARO: site×crop units=8; transect rows=16
- POAR: site×crop units=6; transect rows=12
- POGN: site×crop units=8; transect rows=12

## Gate

The independent-unit contract must reconcile the article's 11 independently sampled remnants /
21 total transects with the public response tables before effects are opened. Any missing bee
transect or site alias must be handled as source missingness/identity, not silently imputed.
