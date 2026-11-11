# About the terminal profile

An original Python/SVG implementation inspired by [Andrew Grant's terminal-style profile](https://github.com/Andrew6rant/Andrew6rant). The artwork is an ASCII interpretation of this account's existing avatar. It is stored as text, so generation needs only Python's standard library.

## Public data

The [workflow](../.github/workflows/refresh-profile.yml) runs daily at 08:23 UTC, on relevant changes to main, and on manual dispatch. GitHub may delay scheduled jobs or disable schedules after extended repository inactivity; the last successfully generated card remains visible.

The generator uses unauthenticated public GitHub REST endpoints. It does not receive a personal access token, query private repositories, or track visitors.

- **Public repos:** owned repositories returned by the public API, including this profile and release repositories.
- **Languages:** language-byte totals across public source repositories. Forks and this profile's generation code are excluded. These are repository observations, not a measure of expertise.
- **Release versions:** the newest published release among the ten most recent release entries for each featured release repository. Public prereleases are included; drafts are excluded.
- **Joined:** the account creation month.
- **Updated:** the date the public snapshot was collected, in UTC.

Name, focus, desktop stack, and other editorial text live in [profile.json](../profile.json). They do not change automatically.

The workflow's standard GitHub token has contents-write access to this profile repository so it can commit generated files. Data collection uses no authentication. No ChordShot or Nodetaker application code is part of this repository.

## Reproduce

From the repository root:

```sh
python3 scripts/generate_profile.py
```

To render the committed snapshot without network access:

```sh
python3 scripts/generate_profile.py --input data/public-profile.json
```

Four SVGs cover desktop/mobile and light/dark layouts. The README uses a picture element to select a version. The cursor respects reduced-motion preferences. Ordinary text and links below the card remain readable without the image.

Fetches, validation, and rendering finish before output files are replaced. An API failure preserves the previous cards and fails the workflow rather than showing invented or zeroed data.
