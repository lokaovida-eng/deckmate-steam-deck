# Contributing

Thanks for helping improve DeckMate. The project is experimental, primarily
targets Steam Deck and Linux, and is not yet packaged for Flathub.

## Before making changes

- Check existing issues and describe the problem or proposed change.
- Keep changes focused and explain user-visible behavior changes.
- Do not add credentials, access tokens, private logs, or personal device data.
- Do not claim a platform or repair path is supported unless it has been tested.
- Do not add broad host permissions or bypass Flatpak sandboxing to make a
  potential package appear functional.

## Validation

Use Python 3.10 or newer. Before opening a pull request, run:

```bash
python3 -m py_compile assistente.py
python3 -m unittest discover -s tests -v
```

The Qt translucency contract is tested offscreen; visual compositor behavior
and Copilot integration still need testing on a real graphical Linux system
with an account that can access Copilot.

## User reports and maintenance

Bug reports should include the DeckMate version or commit, operating system and
desktop session, steps to reproduce, and what happened versus what was
expected. Reports are optional; do not include Copilot credentials, tokens,
private logs, serial numbers, or other identifying device data. Remove sensitive
details before attaching any diagnostic output.

Reports from real devices help distinguish automated checks from behavior
verified on Steam Deck or another Linux system. Do not describe a platform,
feature, or user base as tested unless there is a reproducible test or an actual
user report supporting that statement.

## Release readiness

Do not tag a release solely to increase the commit count. Before creating a
version tag:

- The release must provide a coherent, working set of user-facing changes.
- The full validation commands below must pass on the release commit.
- The changelog must describe the changes and known limitations.
- Core behavior must have been exercised on a real supported desktop; identify
  which environment was tested and which remains unverified.
- Installation and upgrade instructions must match the published dependencies.

Use an annotated `vMAJOR.MINOR.PATCH` tag for a release that meets these checks.
There is no fixed commit-count or waiting-period threshold that guarantees
Flathub eligibility; sustained development, real-world use, and maintenance
must be demonstrated over time.

## Pull requests

Include a concise description, the reason for the change, validation performed,
and any known limitations. For changes affecting diagnostics or actions, explain
what host access is required and how user data is protected. Maintainers may ask
for revisions before accepting changes.
