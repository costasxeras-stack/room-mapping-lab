# Case study: Room Mapping Lab

## The question

Every hotel supplier names the same room differently. Mapping those names to one master room is what makes rates comparable, so a traveller sees one room with the best price instead of five confusing ones. The hard part is not matching, it is deciding how much to automate: every threshold trades automation against wrong rooms booked and review work. I built this lab to make that trade-off concrete on real LiteAPI data.

## Approach

I reused what I had learned building KostasTravel on LiteAPI: rates with room mapping on carry a mappedRoomId, and /data/hotel lists the master rooms. A GitHub Action pulls both for a few hundred hotels. Three simple matchers score every supplier name against the master rooms, and the lab compares them to LiteAPI's mapping. The decision tab converts the confidence threshold into money using inputs a business owns.

## Findings

### 1. How well simple methods agree with LiteAPI's mapping (to measure on live data)

[result once the sandbox data is in]

### 2. How many rates LiteAPI leaves unmapped, by city (to measure on live data)

[result once the sandbox data is in]

### 3. The best threshold depends on business inputs, not only on the model (design finding)

In the lab, the best threshold moves with the cost of a wrong room and with review capacity. That is why the plan starts by agreeing those numbers with finance and operations.

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

1. Add an LLM judge for the uncertain slice and measure accuracy, cost and latency
2. Hand-label an audit sample to measure precision against truth, not agreement
3. Thresholds per room risk class (suites and views stricter than simple doubles)

## My role

I framed the problem, made the product calls, checked every number and wrote the conclusions. Claude (Anthropic) wrote the code with me. 
