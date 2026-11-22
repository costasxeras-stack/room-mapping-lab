# 0004: The API key lives in a GitHub secret

**Status:** accepted, 0.1.0

## Context

A static page cannot hide an API key.

## Decision

Fetch with a GitHub Action that reads the secret and commits only the derived data.

## Tradeoff

- Data is a snapshot, refreshed weekly or on demand
- The key never reaches the browser or the repo
