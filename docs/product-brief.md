# Product brief: Room Mapping Lab

## Problem

Every hotel supplier names the same room differently. Mapping those names to one master room is what makes rates comparable, so a traveller sees one room with the best price instead of five confusing ones. The hard part is not matching, it is deciding how much to automate: every threshold trades automation against wrong rooms booked and review work. I built this lab to make that trade-off concrete on real LiteAPI data.

## Users

- Mapping and content product teams deciding how much matching to automate
- Engineering leads weighing rules, models and LLMs for entity matching
- Hiring managers who want to see product judgement connected to business outcomes

## Goals for 0.1.0

- Make the automation trade-off concrete on real data
- Show how I would run mapping as a product

## Non-goals for 0.1.0

- A production matcher
- Claims about Nuitée's internal performance

## Success measures

| Measure | Definition | Target |
|---|---|---|
| Correct-mapping share | Share of bookable rates mapped correctly, weighted by bookings (from an audit sample) | [target] |
| Coverage | Share of rate names mapped, by city and supplier | [target] |
| Time to map | Hours from a new hotel or supplier to 95% coverage | [target] |
| Guardrail | Wrong-room complaints and refunds per 10,000 bookings | [target] |
