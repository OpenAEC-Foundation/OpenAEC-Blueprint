# Conventions

Coding conventions and style guide for OpenAEC Foundation projects.

## Contents

- `CONVENTIONS.md` — detailed coding style guide
- `conventions.yaml` — machine-readable convention definitions used by [repo-cleaner](https://github.com/OpenAEC-Foundation/repo-cleaner)
- `RUST.md` — enforced Rust conventions and their official Rust-project sources

## Shared issue assignment

Repositories can call `.github/workflows/auto-assign-issues.yml` to assign newly
opened issues to their product owners:

```yaml
name: Auto-assign issues to product owner

on:
  issues:
    types: [opened]

permissions:
  issues: write

jobs:
  assign:
    uses: OpenAEC-Foundation/conventions/.github/workflows/auto-assign-issues.yml@main
    with:
      assignees: '["JohnHeikens"]'
```

The required `assignees` input is a JSON array of GitHub usernames and supports
multiple owners. The workflow uses the calling repository's token and issue
number. Callers must grant `issues: write`; reusable workflows cannot increase
their callers' permissions. No additional token or secret is required.

To assign an existing issue manually, add this trigger to the caller:

```yaml
  workflow_dispatch:
    inputs:
      issue_number:
        description: Existing issue number to assign
        required: true
        type: number
```

Pass `issue_number: ${{ fromJSON(format('{0}', inputs.issue_number || github.event.issue.number || github.event.pull_request.number)) }}`
alongside `assignees` in the calling job's `with` block. The optional
`issue_number` input otherwise defaults to the triggering issue or pull request.
The conversion ensures manually entered values are passed as numbers.
Manual runs require write access to the calling repository.

Callers that also assign pull requests can retain their `pull_request: opened`
trigger and grant `pull-requests: write` alongside `issues: write`. Assignment
errors fail the workflow so they remain visible. Calls reference `@main` so
changes to the shared implementation apply to all callers.
