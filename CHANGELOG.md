# Changelog

All notable changes to this project. Versions follow [docs/versioning.md](docs/versioning.md).

## [0.3.0] - 2026-11-23

### Changed
- New design. Tab 1 opens on a mapping board for one hotel: every supplier rate name on the left, an arrow to the yellow master room it was mapped to on the right, and unmapped names or missing room IDs shown with a dashed target. On phones each master room comes first with its supplier names under it.
- The hotel name and city now show above the board.
- Own look for this app: ocean teal, sun yellow, Outfit, dark board.

### Added
- Decision record: open with the mapping board.

Data, matching methods and the decision model are unchanged.

## [0.2.0] - 2026-11-22

### Added
- Data checks tab: rates mapped to room IDs missing from content, accessible rates mapped to rooms not marked accessible, duplicate master rooms, mapping consistency and destination search.
- Hotel addresses and the destination candidates in the data file.

### Fixed
- The fetch now picks the destination in the expected country. The first pull took the first result for "Rome", which was Rome, Georgia, USA.
- Supplier names with leading zeros ("01 Bedroom") are read as numbers.

## [0.1.0] - 2026-11-21

First release.

### Added
- The problem: coverage by city, names per master room, and one hotel up close with its supplier names grouped by master room and the unmapped ones in red
- Three matching methods: rules (room class, bed, view, extras, with abbreviations such as DBL, TWN, DLX), character trigram similarity, and a hybrid that is confident only when both agree
- Scored against LiteAPI's mapping, with the share auto-mapped and the agreement at a confidence threshold
- Data checks: rates mapped to room IDs missing from content, accessible rates mapped to non-accessible rooms, duplicate master rooms, mapping consistency and destination search
- Disagreements and suggestions: where a method disagrees with LiteAPI, and what the hybrid would suggest for rates LiteAPI left unmapped
- The decision: a threshold slider, business inputs (volume, review capacity, review cost, booking share, cost of a wrong room, value of a mapped name), net value by threshold and the best threshold
- Sensitivity: how the best threshold moves when the cost of a wrong room or review capacity change
- A one-page operating plan: metrics, the first 90 days, trade-offs for engineering, and the decision to ask for
- Data job: a GitHub Action pulls the data from the LiteAPI sandbox with a key kept as a repository secret
