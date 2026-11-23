# 0005: Open with the mapping board

**Status:** Accepted · 23 November 2026

## Context

Version 0.2.0 opened tab 1 with five number tiles and a city table, and showed one hotel's mapping as grey chip groups further down. It shared one visual template with the other portfolio apps, and the core problem (many supplier names for one room) was easy to scroll past.

## Decision

Open tab 1 with a mapping board for one hotel. Supplier rate names sit on the left, each group points with an arrow to the master room it was mapped to, shown as a yellow card on the right. Names left unmapped, and names mapped to a room ID that is not in the hotel's room list, point to a dashed card. The page still opens on the "messiest" hotel by the same score as before, and the picker and buttons stay.

The tiles and the city table follow below the board. The app gets its own look: ocean teal, sun yellow, Outfit, and a dark board.

## Consequences

- The problem reads in one look: three or more names for one room, and the names that point nowhere.
- On phones the board stacks: master room card first, its supplier names under it, no arrows.
