# lintian-codeclimate

This project provides a Python-based parser for Lintian to write
CodeClimate-format reports, mainly to assist using Lintian in
Gitlab CI/CD pipelines.

## Install

```shell
python -m pip install lintian-codeclimate
```

## Usage

Just pipe the output of `lintian --info` to the `lintian_codeclimate` module.

```shell
lintian --info | python -m lintian_codeclimate
```
