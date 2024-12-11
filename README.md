# opr
The tool combines uv/poetry and git cliff to bump a python projects version,
generate the changelog, commit both and tag the release.

## Installation
```bash
$ pip install "git+https://github.com/glencoe/opr@0.3.0"
```

## Usage

```bash
$ opr-bump uv
```
or
```bash
$ opr-bump poetry
```

## Known Issues

Git cliff will take the version number from git tags, while
we read the version number from the pyproject file.
This may cause inconsistencies, when the latest git version
tag does not match the number in the pyproject.toml


## Todo
- [ ] make the tool work without uv as well
