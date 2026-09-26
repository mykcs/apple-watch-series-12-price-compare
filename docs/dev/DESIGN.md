# Development and CI design

## Why CI is useful here

Although the site is static HTML, the content is not purely decorative. Price conversion and regional comparisons can become internally inconsistent when one number changes without its derived values.

A few seconds of deterministic Python validation is cheaper than discovering those mistakes after deployment.

## What CI checks

- required pages and internal routes;
- non-empty HTML titles;
- Watch fixed 46 mm policy and preselected purchase URLs;
- README exchange-rate snapshot;
- Watch CNY conversions and regional deltas;
- iPhone 18 Pro Max 256GB fixed-model price conversions.

## What CI does not do

- no browser/E2E farm;
- no live Apple price scraping;
- no automatic exchange-rate refresh;
- no Vercel deployment;
- no shopping/availability claim.

Live prices remain content-maintenance evidence, not something CI invents.

## Provider roles

- GitHub: source / PR / lightweight correctness gate.
- Vercel: Preview / Production deployment.
