mod blob "sdks/blob-az/Justfile"
mod cosmos "sdks/cosmosdb/Justfile"
mod pubsub "sdks/pubsub-az/Justfile"
mod queue "sdks/queue-az/Justfile"
mod aad "sdks/aad-b2c/Justfile"

VENV := ".venv"
PYTHON := VENV + "/bin/python"

help:
  @just --list

init:
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt
