# Current development direction

CI mode: **STANDARD_CI**

This public static site contains real purchasing logic: fixed models/sizes, exchange-rate conversion, regional price deltas and internal navigation.

The current cheap validation contract is:

```bash
python3 scripts/validate_site.py
```

Public GitHub Actions runs that validator on pull requests. Vercel remains the website Preview/Production provider; CI does not replace deployment.

The validator intentionally avoids browser farms and package-manager setup. It protects only high-value deterministic logic that has actually been easy to break during edits.
