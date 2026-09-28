# CI Passport

Status: **candidate — lightweight public logic gate**

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

The pull-request workflow checks out the exact PR head SHA before validation. Before making the check required, obtain a successful hosted run for that raw candidate commit. Vercel remains independent deployment evidence.
