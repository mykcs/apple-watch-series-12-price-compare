# Agent documentation index

This repository is intentionally small. This file is navigation-only and does not duplicate page content.

## Project map

| Task | Read / verify |
|---|---|
| Overall site scope | `README.md` |
| Homepage/navigation | `index.html` |
| Apple Watch comparison | `watch/index.html` |
| iPhone comparison | `iphone/index.html` |
| Mac chooser | `mac/index.html` and the relevant `mac/*/index.html` route |
| Current Apple price/spec/config claim | current official Apple source first, then the route HTML |
| Exchange-rate conversion | the dated snapshot stated in `README.md` / route copy |
| Deployment status | live Vercel state + public route |

## Knowledge boundary

The site contains both durable structure and time-sensitive purchasing facts.

Treat:
- route structure and explanation design as repository-owned;
- current product availability, prices, specs and education-store state as external/live facts that must be refreshed;
- dated exchange rates as snapshots, not timeless truth.

## Agent continuity

Shared cross-tool Agent architecture and handoff semantics live in:

- `mykcs/.agents/docs/agents/KNOWLEDGE-ARCHITECTURE.md`
- `mykcs/.agents/docs/agents/HANDOFF_PATTERN.md`

Do not create a project-local copy of those shared rules.
