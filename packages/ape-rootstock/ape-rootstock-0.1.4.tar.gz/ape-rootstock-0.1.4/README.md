# Quick Start

Ecosystem Plugin for Rootstock support in Ape

## Dependencies

- [python3](https://www.python.org/downloads) version 3.9 up to 3.12.

## Installation

### via `pip`

You can install the latest release via [`pip`](https://pypi.org/project/pip/):

```bash
ape plugins install rootstock
```

or via config file:

```yaml
# ape-config.yaml
plugins:
  - name: rootstock
```

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
git clone https://github.com/rsksmart/ape-rootstock.git
cd ape-rootstock
python3 setup.py install
```

## Quick Usage

Installing this plugin adds support for the Rootstock ecosystem:

```bash
ape console --network rootstock:mainnet
```

## Development

This project is in development and should be considered a beta.
Things might not be in their final state and breaking changes may occur.
Comments, questions, criticisms and pull requests are welcomed.
