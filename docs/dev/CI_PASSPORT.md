# CI Passport

Status: **active — lightweight required PR gate**

Repository: `mykcs/apple-watch-series-12-price-compare`  
Integration branch: `main`  
CI mode: `STANDARD_CI`

## Contract

- command: `python3 scripts/validate_site.py`
- provider: public GitHub Actions
- runner: Ubuntu
- expected runtime: seconds
- required external services: none
- secrets: none
- deployment side effects: none
- required main check: `Price and route validation` (GitHub Actions, integration ID `15368`; strict ruleset `24133819`)

The pull-request workflow checks out the exact PR head SHA before validation. The required check is bound to the GitHub Actions app and blocks stale candidates when `main` advances. Vercel remains independent deployment evidence.
