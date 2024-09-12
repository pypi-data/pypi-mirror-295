# Data Quality SDK

A Python SDK for performing data quality checks on individual records. This SDK allows you to validate records against specified checks and publish metrics to a Kafka topic.

## Features

- **Null Checks**: Identify records with null values in specified fields.
- **Completeness Checks**: Verify that all required fields are populated.
- **Type Checks**: Validate that data types of fields match expected types.
- **Kafka Integration**: Publish metrics for failed checks to a Kafka topic.

## Installation

You can install the SDK via pip. Run the following command:

```bash
pip install data-quality-sdk

## Usage 

```bash
from data_quality_sdk import dq
from data_quality_sdk.checks import NullCheck, TypeCheck, CompletenessCheck
bootstrap_server = 'localhost:9092'
topic = 'data-quality-metrics' 
schema = {
    "customer_id": "int",
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "registration_date": "string"
}
checks = [
    NullCheck(),  # Create an instance of NullCheck
    CompletenessCheck(),  # Create an instance of CompletenessCheck
    TypeCheck(schema)  # Create an instance of TypeCheck with the schema
]
record = {
    "customer_id": 12354,
    "first_name": "Alice",
    "last_name": None,  # This will trigger a null check
    "email": "alice.johnson@example.com",
    "registration_date": "2024-09-01"
}
result = dq(record, checks, bootstrap_server, topic, schema)
