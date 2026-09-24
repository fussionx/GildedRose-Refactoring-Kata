# Gilded Rose starting position in Python

For exercise instructions see [top level README](../README.md)

## Set up

Dependencies are declared in `pyproject.toml`. With [uv](https://docs.astral.sh/uv/):

```
uv sync --group test
```

or with a plain virtual environment: `python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`.

## Run the tests from the Command-Line

```
uv run pytest
```

This runs both the unit tests in `tests/test_gilded_rose.py` (one focused test per
inventory rule) and the 30-day approval test described below. For a coverage report:

```
uv run coverage run -m pytest && uv run coverage report
```

## How the rules are organised

`gilded_rose.py` has one `ItemUpdater` subclass per item category (ordinary, Aged Brie,
backstage passes, Sulfuras, Conjured). `updater_for(item)` picks the rule set from the
item's name and `GildedRose.update_quality()` delegates to it. To add a new category,
add a subclass and register it in `updater_for`; the `Item` class is unchanged.

## Run the TextTest fixture from the Command-Line

For e.g. 10 days:

```
python texttest_fixture.py 10
```

You should make sure the command shown above works when you execute it in a terminal before trying to use TextTest (see below).


## Run the TextTest approval test that comes with this project

There are instructions in the [TextTest Readme](../texttests/README.md) for setting up TextTest. You will need to specify the Python executable and interpreter in [config.gr](../texttests/config.gr). Uncomment these lines:

    executable:${TEXTTEST_HOME}/python/texttest_fixture.py
    interpreter:python

## Run the ApprovalTests.Python test

This test uses the framework [ApprovalTests.Python](https://github.com/approvals/ApprovalTests.Python)
and runs as part of `uv run pytest`. It captures 30 days of `texttest_fixture.py` output and
compares it with `tests/approved_files/*.approved.txt`. On a mismatch the diff is printed to
the console; if the new output is correct, approve it by copying `xxx.received.txt` over
`xxx.approved.txt`.
