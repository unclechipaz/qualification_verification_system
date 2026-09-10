# Contributing to the MSU Qualification Verification System

This repository supports the team's software engineering assignment. Keep each contribution traceable to the person making it, describe the actual change, and link it to the relevant requirement or defect.

## Responsibilities

| Member | Assigned role | Scope |
| --- | --- | --- |
| Charlton | Project Manager and DevOps Lead | Architecture, Django configuration, Git repository management, Docker, CI and cloud deployment |
| Simba | Database and Qualification Registry Lead | Requirement 1: `Student`, `Qualification`, `Certificate`, migrations and `seed_db` |
| Mncedisi (Artwell) | Search and Retrieval Specialist | Requirement 2: certificate/student/ID/name search, resource APIs and query indexing |
| Doreen | Verification and Frontend UI Specialist | Requirement 3: public/employer verification pages, Bootstrap layout, status stamps and QR interface |
| Cleopatra | Audit Trail and QA/Documentation Lead | Requirement 4: `AuditLog`, verification/screening history, tests, manuals and diagrams |

These allocations do not establish that all assigned features are complete. Use code, test results, pull requests and reviews as contribution evidence.

## Branches and integration

- `main` is the intended release branch. A release needs review and verification; the branch name alone does not establish production readiness.
- `develop` is the integration branch.
- Use a relevant `feature/*`, `fix/*` or `docs/*` branch for changes.
- `docs/repository-corrections` is the branch for the current documentation corrections. PR #7 brought the application fixes from `develop` into that branch.
- Feature and correction work should enter `develop` through a pull request. A later release pull request can bring reviewed changes from `develop` into `main`.

For documentation changes, the eventual pull request must have **base `develop`** and **compare `docs/repository-corrections`**. This direction is the reverse of the earlier synchronisation PR.

## Working locally

First check `git status` and commit or otherwise preserve any existing work. From an existing clone:

```bash
git fetch origin
git switch docs/repository-corrections
git pull --ff-only origin docs/repository-corrections
```

If the documentation branch is not yet local, replace the switch command with:

```bash
git switch --track origin/docs/repository-corrections
```

To bring later integration changes into the checked-out documentation branch:

```bash
git merge origin/develop
```

Resolve conflicts by reviewing both versions. Check the result before committing and pushing. Do not force-push as a routine synchronisation step.

Stage only the files belonging to the change. For this documentation set:

```bash
git add README.md CONTRIBUTING.md docs/
git diff --cached --stat
git diff --cached
git commit -m "docs: align repository guides with implemented behaviour"
git push origin docs/repository-corrections
```

Confirm the configured Git name/email belong to your own GitHub account. Preserve the original authorship of commits you merge.

The repository's `git_history_setup.py` is not an installation or contribution step. It changes local Git identity to a fixed account, stages all files and creates a scripted sequence of commits using `--allow-empty`. Do not run it in your working clone or use its generated commit descriptions as evidence that features were implemented.

## Validation before a pull request

For application changes, run these commands from the repository root using the installed virtual environment:

```bash
python backend/manage.py check
python backend/manage.py makemigrations --check --dry-run
python -m pytest --tb=short
```

Use the interpreter paths in the [Installation Guide](docs/INSTALLATION_GUIDE.md) if the environment is not activated. Add migrations only when model changes require them. The pytest configuration uses `--nomigrations`, so passing tests do not replace migration checks or testing migration application.

For documentation changes, verify relative links, route names, commands, role permissions, model fields and examples against the source. Record any steps you did not run.

The current Actions workflow runs on pushes to `main`, `develop` and `feature/*`, and on pull requests targeting `main` or `develop`. A push to `docs/*` alone does not trigger that workflow. Despite the workflow's name and job identifier, it contains no lint, coverage, security scanning, deployment or image-publishing step.

## Pull request and review

1. Select the intended source and destination branches and inspect **Files changed**.
2. Explain the problem, the resulting behaviour and the validation performed.
3. Obtain a teammate's review. Review the actual diff and check results before approval.
4. Address comments and conflicts, then merge once the team's review requirements are met.
5. Confirm the destination contains the changes and keep documentation aligned with the merged code.

Do not commit demonstration databases, generated media, passwords, tokens or virtual environments. The current ignore file does not exclude SQLite databases, so check staged files explicitly. Report contributions accurately, including any AI assistance required by the assignment's rules.
