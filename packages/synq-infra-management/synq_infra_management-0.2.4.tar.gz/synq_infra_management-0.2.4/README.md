# synq-infra-management
manages Synq tooling

# initial setup

## 1. Install dependancies

NOTE - this also pulls down the Synq proto files

```bash
python -m venv .env
source .env/bin/activate

pip install -r requirements.txt

pip install pre-commit
pre-commit install

python3 -m pip install getsynq-api-grpc-python --extra-index-url https://buf.build/gen/python
```

# Project Documentation

## Overview

This project automates the management of SQL tests using Synq's gRPC API. It provides functionality to deploy, update, and delete SQL tests based on configurations stored in YAML files (tests_def.yaml and core_data.yaml). The project compares local test definitions with the tests already deployed in Synq and handles any necessary updates or deletions.

## Project Structure

`main.py`: The entry point of the project, which handles argument parsing and controls the execution of the deployment or planning of SQL tests.

`create_sql_tests.py`: Contains the logic to parse YAML files, generate SQL tests, and manage the deployment and deletion of tests.

`grpc_client/client.py`: Handles the gRPC channel setup to connect with the Synq API.

`proto_parsers/sqltest_parser.py`: Contains the sqlTestParser class to parse and manage SQL tests.

## Dependencies

`gRPC`: Used for communication with Synq's API.

`YAML`: For loading and parsing YAML configuration files.

## Setup

<b>1. Environment Variables</b>

You need to set up two environment variables in your GitHub Actions production environment:

- `SYNQ_LONG_LIVED_TOKEN`: API Token from Synq.

- `SNOWFLAKE_ACCOUNT`: List of Snowflake Account IDs (comma-separated if more than one)

<b>2. YAML Files</b>

`tests_def.yaml`: Contains the test definitions, including SQL templates and tags.

`*_data.yaml`: Contains the actual tests with tables, columns, and specific tag information.

## Usage

The project can be run in two modes:

1. `Plan Mode`: This mode compares the local YAML files with the deployed tests in Synq and shows the differences without making any changes. Use the --plan argument for this mode.

2. `Apply Mode`: This mode deploys new tests, updates existing ones, and deletes outdated tests based on the differences found between the local YAML files and the deployed tests. Use the --apply argument for this mode.

## Example commands

- <b>Plan Mode</b>:
``` bash
python main.py --plan
```
- <b>Apply Mode</b>:

``` bash
python main.py --apply
```

## Example SQL Test Setup

Here is an example of how to set up an SQL test:

`tests_def.yaml`:

```yaml
- id: test_1_id
  sql: |
    select {.Column} from {.Table} where {.Column} <= {.WhereA} or {.Column} >= {.WhereB};
  tags:
    type: values_between
```

`*_data.yaml`:

```yaml
- account: "your_snowflake_account"
  database: "your_database"
  table: "your_table"
  tags:
    owner: "team_name"
    datacentre: "location"
    product: "product_name"
    environment: "production"
  columns:
    - name: your_column
      where_a : foo
      where_b : bar
      tests:
        - values_between 
    - name: your_column_2
      tests:
        - test_1_id:
            values: "expected_value_2"
```

In this example:

1. <b>Test Definition</b>: In `tests_def.yaml`, `test_1` is defined with a SQL template that will count rows where a specific condition is met.

2. <b>Data</b>: In `*_data.yaml`, the test is applied to a specific table and column, with the condition value provided as `expected_value`. Each file that matches with `*_data.yaml`` inside of synq_tests directory will be read by the program

## GitHub Actions Pipeline

The project can be integrated into a CI/CD pipeline using GitHub Actions. The pipeline should consist of two stages:

1. <b>Plan Stage</b>: This stage runs when a pull request is opened. It executes `main.py --plan` and prints the possible changes without applying them.

2. <b>Apply Stage</b>: This stage requires approval before execution. After the pull request is merged, the pipeline runs `main.py --apply` to deploy the changes.

Example GitHub Actions Workflow:

<b>Plan:</b>
```yaml
name: PR Plan

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  plan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run Plan
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
      run: python main.py --plan
```

<b>Apply:</b>
```yaml
name: Apply

on:
  push:
    branches:
      - main

jobs:
  plan:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run Plan for Verification
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
      run: python main.py --plan

  apply:
    runs-on: ubuntu-latest
    needs: plan
    environment:
      name: production

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Approve and Apply
      env:
        SYNQ_LONG_LIVED_TOKEN: ${{ secrets.SYNQ_LONG_LIVED_TOKEN }}
        SNOWFLAKE_ACCOUNT: ${{ vars.SNOWFLAKE_ACCOUNT }}
      run: python main.py --apply

```