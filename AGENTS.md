# Repository Agent instructions

This is a small static Apple purchase-comparison site. Keep the Agent surface thin.

## Read first

1. `README.md` — current product/page scope and public URL.
2. `docs/agents/README.md` — route/ownership map.
3. Only the HTML route(s) relevant to the requested change.

Do not recursively read every page for a one-route edit.

## Authority boundaries

- Human-facing scope and comparison intent → `README.md`.
- Rendered content and interaction → the relevant route `index.html`.
- Apple prices, education-store availability, product configurations, technical specifications and purchase URLs → current official Apple pages; re-verify before changing dated/current claims.
- Exchange-rate claims → the explicitly dated snapshot documented in the site; do not silently mix dates.
- Deployment/provider status → live Vercel state when a deployment claim matters. Repository prose is not proof that a deployment is currently healthy.

## Editing rules

- Preserve route independence: a Watch-only edit should not rewrite iPhone/Mac pages unless the shared claim actually changes.
- Keep product/configuration comparisons like-for-like. Do not compare different storage, case size, connectivity or tax assumptions without making the difference explicit.
- Current/future Apple product facts are time-sensitive. Verify them before editing rather than relying on model memory.
- Do not add Wish/Dev/Current folders merely for account-wide symmetry; this repository is small enough to use this router + README + source files.
- Historical values may remain when clearly dated; current purchase guidance must use current sources.

## Validation

For a changed route:
- inspect the final HTML;
- verify internal links affected by the change;
- verify external purchase/source links when they are part of the task;
- after deployment work, verify the actual public route rather than assuming repository merge equals Production success.
