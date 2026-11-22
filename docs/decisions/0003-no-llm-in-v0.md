# 0003: No LLM judge in the first version

**Status:** accepted, 0.1.0

## Context

An LLM judge could resolve uncertain cases but adds cost and latency, and needs a key the page cannot hold.

## Decision

List it as an option for the uncertain slice only, with accuracy, cost per 1,000 calls and latency as [to measure].

## Tradeoff

- The comparison is incomplete
- Keeps the first version free, fast and safe
