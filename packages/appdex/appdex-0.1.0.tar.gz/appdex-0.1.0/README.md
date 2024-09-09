# Appdex

A highly opinionated CLI tool for installing and setting up apps on debian-based systems.

## Features

- Install and setup apps & packages

## Prerequisites

- [Advanced Package Tool (APT)](https://wiki.debian.org/Apt)
- [wget](https://www.gnu.org/software/wget/)
- [curl](https://curl.se/)

## Installation

```shell
pip install appdex
```

## Usage

```shell
appdex --help
```

## Usage (without installing)

```shell
pipx run appdex --help
```

or

```shell
python -m appdex --help
```

## Examples

All examples will show using `appdex` as a command (installed). All uses of `appdex` are interchangeable with
`python -m appdex` and `pipx run appdex`.

### Run install wizard

This will prompt you to select which apps to install.

```shell
appdex install
```

### Install all apps

This will install all apps. Prompting you with any questions that are required from tools like `apt`.

```shell
appdex install all
```

### Install all apps, accepting all prompts

(Coming soon)
This will install all apps. Accepting all prompts. This flag works with all commands.

```shell
appdex install all --accept-all-prompts
```

## License

This project is licensed under the TBA License - see the [LICENSE](LICENSE) file for details

