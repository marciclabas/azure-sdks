mod blob "sdks/blob-az/Justfile"

VENV := ".venv"
PYTHON := VENV + "/bin/python"

help:
  @just --list

init:
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt
