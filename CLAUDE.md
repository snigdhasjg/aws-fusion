# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`aws-fusion` is a Python CLI that bundles several AWS authentication / convenience helpers behind one entry point. Published to PyPI as `aws-fusion`; the version lives in `aws_fusion/__init__.py` and is what triggers a publish (see CI section).

## Development

```shell
pip install -e .        # editable install — pulls deps from setup.py
aws-fusion --help       # console_scripts entry point → aws_fusion.app:main
python -m aws_fusion.app --help   # equivalent invocation used by the `aws fusion` alias
```

There is no test suite, lint config, or formatter wired up. Don't fabricate one.

## Architecture

Entry point flow: `aws_fusion/app.py` builds an `argparse` parser, then each module in `aws_fusion/commands/` exposes a `setup(subparsers, parent_parser)` function that registers its subcommand and binds `args.func` to a `run` callable. To add a new top-level command, create a module under `commands/`, implement `setup` + `run(args)`, and append it to the `commands` list in `app.py`. `--debug` is a global flag handled in `app.py`.

Subcommands and what they wrap:

- `init` — writes a `[toplevel] fusion = !"<python>" -m aws_fusion.app` entry into `~/.aws/cli/alias` so `aws fusion ...` proxies to this tool.
- `open-browser` — `commands/open_browser.py` → `aws/session.py` resolves boto3 credentials (and rewires the assume-role / sso credential providers to use `~/.aws/cli/cache` so caching matches the AWS CLI) → `aws/api.py` exchanges them for a federation signin token and builds a console signin URL. Requires session credentials (`creds.token` must be non-null), so it only works for assume-role / SSO / federated profiles, not raw IAM user keys.
- `iam-user-credentials store|get` — stores/retrieves secret keys via `keyring` (OS credential store). Service name is `aws-<account-id>-<username>`, username field is the access key. `get --credential-process` emits the JSON shape AWS CLI expects for `credential_process`.
- `okta device-auth` — `okta/api.py` runs OAuth device-code flow → token exchange → `/login/token/sso` → parses SAML assertion with BeautifulSoup → `aws/assume_role.py` calls `sts:AssumeRoleWithSAML` and caches the response under `~/.aws/saml/cache/<sha1(role-arn)>` via `botocore.utils.JSONFileCache`. The cache is checked first and reused if it has >1 min of validity left; on `ClientError` (typically session-duration too long for the role) it retries with `DurationSeconds=3600`.
- `config-switch profile|region` — interactive `inquirer` picker that writes the chosen value to `~/.aws/fusion/profile` or `~/.aws/fusion/region`. These files are read by the `bin/_awsp` / `bin/_awsr` shell scripts (and `.ps1` equivalents) which then `export AWS_PROFILE` / `AWS_REGION` in the caller's shell. The scripts must be sourced (e.g. `alias awsp="source _awsp"`) — running them as a child process has no effect.

Two credential caches with different shapes coexist: `~/.aws/cli/cache` (AWS CLI–compatible, used by `open-browser` for boto3's built-in providers) and `~/.aws/saml/cache` (this tool's own, used only by `okta device-auth`).

## Release / CI

`.github/workflows/publish.yml` is the only workflow. It runs on:
- `push` to `main` **only when `aws_fusion/__init__.py` changes** → publishes to real PyPI and pushes a `v<version>` git tag.
- `pull_request` to `main` or manual `workflow_dispatch` → publishes to **Test** PyPI with a version suffixed by `.<github.run_number>`.

So bumping `__version__` in `aws_fusion/__init__.py` on `main` is the release trigger. Don't bump it casually.

The `scripts=[...]` list in `setup.py` installs `bin/_awsp`, `bin/_awsr`, and their `.ps1` siblings onto the user's PATH — keep that list in sync if new shell helpers are added.
