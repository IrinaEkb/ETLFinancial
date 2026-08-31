#!/bin/bash

set -e

cd "$(dirname "$0")"

source venv/bin/activate

export AIRFLOW_HOME="$PWD/airflow_config"

airflow dags trigger xbrl_financial_pipeline