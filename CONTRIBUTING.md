This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency management. Python 3.12 is required.

```shell
git clone https://github.com/snigdhasjg/aws-fusion.git
cd aws-fusion
uv sync                          # create .venv and install deps + project (editable)
uv run aws-fusion --help         # run the CLI from the project venv
```

To build distributions locally:

```shell
uv build                         # produces dist/*.whl and dist/*.tar.gz
```
