# Dev — Apple comparison site

CI mode: **STANDARD_CI**

- [LATEST.md](LATEST.md) — current development direction.
- [DESIGN.md](DESIGN.md) — why the site uses a tiny public CI lane plus Vercel deployment.
- [CI_PASSPORT.md](CI_PASSPORT.md) — current validation contract.
- [ARCHIVE.md](ARCHIVE.md) — replaced decisions only.
- [Shared Dev protocol](https://github.com/mykcs/.codex/blob/main/engineering/DEV_PROTOCOL.md)

The website source is static HTML. Vercel remains the deployment/hosting role; repository correctness is checked independently by a dependency-free Python validator.
