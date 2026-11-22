# Case study: Room Mapping Lab

## The question

Every hotel supplier names the same room differently. Mapping those names to one master room is what makes rates comparable, so a traveller sees one room with the best price instead of five confusing ones. The hard part is not matching, it is deciding how much to automate: every threshold trades automation against wrong rooms booked and review work. I built this lab to make that trade-off concrete on real LiteAPI data.

## Approach

I reused what I had learned building KostasTravel on LiteAPI: rates with room mapping on carry a mappedRoomId, and /data/hotel lists the master rooms. A GitHub Action pulls both for a few hundred hotels. Three simple matchers score every supplier name against the master rooms, and the lab compares them to LiteAPI's mapping. The decision tab converts the confidence threshold into money using inputs a business owns.

## Findings

### 1. Simple methods agree with LiteAPI's mapping on most names, but not enough to automate everything (confirmed on sandbox data, 22 November 2026)

On 1,638 distinct rate names from 173 hotels in 8 cities, the hybrid method picked the same master room as LiteAPI for 84%, text similarity 84% and rules 65%. At a confidence of 0.8 the hybrid would auto-map 59% of names with 94% agreement, and at 0.95 it would auto-map 40% with 98% agreement.

### 2. Every rate returned already had a mapping (confirmed on sandbox data)

All 1,638 names came back with a mappedRoomId, so the sandbox shows no coverage gap. The real gap, rates that stay unmapped in production, needs production data: [to measure].

### 3. Whole hotels point to room IDs that are not in their room list (confirmed on sandbox data, cause is a hypothesis)

In 3 of 173 hotels, all in Barcelona, every rate (35 names) is mapped to a room ID missing from the hotel's content room list. Because it is all rates in each hotel, not random ones, it looks like an ID mismatch between rate mapping and content for those hotels, not a matching error. Worth an integrity check that runs per hotel.

### 4. Disagreements are the most useful output (confirmed on sandbox data)

Several disagreements look like the reference could be refined, for example "2 Single Beds, Garden View" mapped to "2 Single Beds" while the hotel also has "2 Single Beds, Garden View". Others are clear errors by my methods. Either way they form an audit list.

### 5. The best threshold depends on business inputs, not only on the model (design finding)

With the example inputs, doubling the cost of a wrong room moves the best threshold from 0.35 to 0.90, and doubling review capacity moves it to 0.85.

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

I framed the problem, made the product calls, checked every number and wrote the conclusions. Claude (Anthropic) wrote the code with me. 
