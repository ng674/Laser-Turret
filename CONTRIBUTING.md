# Contributing

`nikil-dev` is the integration branch. Create one feature branch per work track:

```bash
git fetch origin
git switch nikil-dev
git pull --ff-only
git switch -c feature/<short-name>
```

Before opening a pull request:

```bash
make check
git status --short
```

Keep pull requests small and confined to the owned paths listed in the applicable
track file. Contract changes belong in standalone commits. Do not rewrite shared
branch history, commit recordings/model weights/run output, or exchange ZIP files
instead of Git commits.

Merge order for the first milestone:

1. Fake-plant/controller pull request.
2. Recorded-video detection/evaluation pull request.
3. Small integration pull request replaying saved tracks into the simulated path.
