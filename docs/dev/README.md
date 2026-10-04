# Dev — Apple comparison site

CI mode: **STANDARD_CI**

- [LATEST.md](LATEST.md) — current development direction.
- [DESIGN.md](DESIGN.md) — why the site uses a tiny public CI lane plus Vercel deployment.
- [CI_PASSPORT.md](CI_PASSPORT.md) — current validation contract.
- [ARCHIVE.md](ARCHIVE.md) — replaced decisions only.
- [Shared Dev protocol](https://github.com/mykcs/.agents/blob/main/docs/agents/DEV_PROTOCOL.md)
- [Shared CI standard](https://github.com/mykcs/.agents/blob/main/docs/agents/CI_STANDARD.md)

The website source is static HTML. Vercel remains the deployment/hosting role; repository correctness is checked independently by a dependency-free Python validator.


## Production deployment contract

Production is owned by the existing Vercel project `apple-watch-series-12-price-compare` and its GitHub integration. The production branch is `main`.

The Vercel GitHub App intentionally uses **Only select repositories**. This repository must remain in that selected set. If GitHub `main` advances but Production does not:

1. compare the current GitHub `main` SHA with the latest Vercel Production deployment;
2. verify the Vercel GitHub App installation still includes `mykcs/apple-watch-series-12-price-compare`;
3. restore the repository selection / Git link before creating any probe commit;
4. use a direct Vercel CLI production deploy only as a bounded recovery fallback;
5. close the incident only after the canonical Production URL serves the expected changed routes.

A repository merge is not deployment proof, and a manual recovery deploy does not by itself prove future Git pushes will auto-deploy.
