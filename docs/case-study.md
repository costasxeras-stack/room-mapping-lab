# Case study: Room Mapping Lab

## The question

Every hotel supplier names the same room differently. Mapping those names to one master room is what makes rates comparable, so a traveller sees one room with the best price instead of five confusing ones. The hard part is not matching, it is deciding how much to automate: every threshold trades automation against wrong rooms booked and review work. I built this lab to make that trade-off concrete on real LiteAPI data.

## Approach

I reused what I had learned building KostasTravel on LiteAPI: rates with room mapping on carry a mappedRoomId, and /data/hotel lists the master rooms. A GitHub Action pulls both for a few hundred hotels. Three simple matchers score every supplier name against the master rooms, and the lab compares them to LiteAPI's mapping. The decision tab converts the confidence threshold into money using inputs a business owns.

## Findings

### 1. Simple methods agree with LiteAPI's mapping on most names, but not enough to automate everything (confirmed on sandbox data, 22 November 2026)

On 1,710 distinct rate names from 187 hotels in 8 cities, the hybrid method and text similarity picked the same master room as LiteAPI for 85% of names, rules for 65%. At a confidence of 0.8 the hybrid would auto-map 62% of names with 94% agreement.

### 2. Whole hotels point to room IDs that are not in their room list (confirmed on sandbox data, cause is a hypothesis)

In 3 of 187 hotels, all in Barcelona, every rate (37 names) is mapped to a room ID missing from the hotel's content room list. Because it is all rates in each hotel, it looks like a per-hotel ID mismatch between rate mapping and content, not a matching error.

### 3. Some accessible rates are mapped to rooms not marked accessible (confirmed on sandbox data)

Of 73 mapped rate names that mention accessibility, 4 (in 4 New York hotels) are mapped to a room with no accessibility marker, although each hotel has accessible rooms in its list. Small in number, high in cost per error.

### 4. Duplicate master rooms in content (confirmed on sandbox data)

45 extra copies of a master room name across 24 hotels, for example the same room name twice in one hotel. Rates for one room can split across the copies.

### 5. Destination search: the first result for "Rome" is Rome, Georgia (confirmed on sandbox data)

The places endpoint returned 5 candidates for "Rome" and the first was Rome, GA, USA. My first pull took the first result and got 11 hotels in Georgia. The fetch now picks the candidate in the expected country.

### 6. Clean on consistency, and no coverage gap in the sandbox (confirmed on sandbox data)

No supplier name maps to two different rooms within one hotel. Every rate returned had a mapping, so the real unmapped share needs production data: [to measure].

### 7. The best threshold depends on business inputs, not only on the model (design finding)

With the example inputs, the best threshold is 0.85. Halving the cost of a wrong room moves it to 0.35, doubling it moves it to 0.90.

## Decisions

### LiteAPI's mapping as the reference, not the truth

There is no hand-labelled set. LiteAPI's mappedRoomId is the best available answer.

**Decision:** Score methods on agreement with LiteAPI, call it agreement everywhere, and show disagreements as the most useful rows for a mapping team.

Full record: [decisions/0001-reference-not-truth.md](decisions/0001-reference-not-truth.md)

### Treat the threshold as a business decision

Teams often set one confidence threshold on model metrics alone.

**Decision:** Model net value from volume, review capacity, review cost, booking share, cost of a wrong room and value of a mapped name, and show where the best threshold sits and how it moves.

Full record: [decisions/0002-threshold-as-business-decision.md](decisions/0002-threshold-as-business-decision.md)

### No LLM judge in the first version

An LLM judge could resolve uncertain cases but adds cost and latency, and needs a key the page cannot hold.

**Decision:** List it as an option for the uncertain slice only, with accuracy, cost per 1,000 calls and latency as [to measure].

Full record: [decisions/0003-no-llm-in-v0.md](decisions/0003-no-llm-in-v0.md)

### The API key lives in a GitHub secret

A static page cannot hide an API key.

**Decision:** Fetch with a GitHub Action that reads the secret and commits only the derived data.

Full record: [decisions/0004-key-in-actions.md](decisions/0004-key-in-actions.md)

## What I learned as a PM

- Matching quality is only half the product. The threshold is where product, operations and finance meet
- Disagreements with the reference are the most useful output for a mapping team
- Room names hide attributes (bed, view, extras) that decide whether two rooms are the same

## Limits

- Sandbox data may differ from production
- Agreement with LiteAPI is not accuracy
- Simple matchers, no LLM judge yet

## What I would do next

1. Add a per-hotel integrity check for mapped room IDs missing from the content room list
2. Add an LLM judge for the uncertain slice and measure accuracy, cost and latency
3. Hand-label an audit sample to measure precision against truth, not agreement
4. Thresholds per room risk class (suites and views stricter than simple doubles)

## My role

I framed the problem, made the product calls, checked every number and wrote the conclusions. 
