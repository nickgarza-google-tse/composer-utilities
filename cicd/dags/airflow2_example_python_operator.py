# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.operators.python import PythonOperator

# Refactored for Airflow 2/3 compatibility and best practices:
# 1. Imported PythonOperator from airflow.operators.python instead of deprecated airflow.operators.python_operator.
# 2. Replaced deprecated schedule_interval with schedule.
# 3. Used static start_date (datetime with timezone) instead of dynamic days_ago().
# 4. Removed deprecated provide_context=True parameter from PythonOperator.
# 5. Access logical_date from task execution kwargs instead of removed execution_date.
# 6. Added default_args with retries and retry_delay.


def print_execution_date(**kwargs):
    # Retrieve logical_date from context kwargs (replaces legacy execution_date in modern Airflow)
    logical_date = kwargs.get("logical_date") or kwargs.get("execution_date")
    print(f"The execution date is: {logical_date}")


with DAG(
    dag_id="airflow2_example_python_operator",
    schedule="@daily",
    start_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["airflow2", "compatibility_test", "new_tag_3"],
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:
    print_date = PythonOperator(
        task_id="print_execution_date_task",
        python_callable=print_execution_date,
    )
