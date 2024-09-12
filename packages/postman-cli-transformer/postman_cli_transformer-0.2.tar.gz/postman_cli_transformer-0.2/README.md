# postman-cli-transformer

[![PyPI](https://img.shields.io/pypi/v/postman-cli-transformer.svg)](https://pypi.org/project/postman-cli-transformer/)
[![Changelog](https://img.shields.io/github/v/release/cerdmann/postman-cli-transformer?include_prereleases&label=changelog)](https://github.com/cerdmann/postman-cli-transformer/releases)
[![Tests](https://github.com/cerdmann/postman-cli-transformer/actions/workflows/test.yml/badge.svg)](https://github.com/cerdmann/postman-cli-transformer/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/cerdmann/postman-cli-transformer/blob/master/LICENSE)

Initially created from: `https://github.com/simonw/click-app`

This package will take as input the STDOUT from a Postman CLI collection run and transform the output text to a JSON doc which may in turn be transformed.

## Installation

Install this tool using `pip`:

```bash
pip install postman-cli-transformer
```

## Usage

For help, run:

```bash
postman-cli-transformer --help
```

You can also use:

```bash
python -m postman_cli_transformer --help
```

As this is intended to be used as a transformer for the Postman CLI output, usage would look something like this with the CLI output transformed into JSON and output to the file output.json

**PLEASE NOTE: THE VERBOSE FLAG IS NOT SUPPORTED YET ON THE CLI COMMAND**

```bash
postman collection run 11111111-11111111-1111-1111-1111-111111111111 -e 11111111-11111111-1111-1111-1111-111111111111  | postman-cli-transformer output.json
```

To output both JSON and a Junit formatted xml file use:

```bash
postman collection run 11111111-11111111-1111-1111-1111-111111111111 -e 11111111-11111111-1111-1111-1111-111111111111  | postman-cli-transformer output.json --junit-out-file junit.xml
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

```bash
cd postman-cli-transformer
python -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install -e '.[test]'
```

To run the tests:

```bash
python -m pytest
```
