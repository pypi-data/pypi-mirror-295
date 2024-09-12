# dq_ops.py

from .checks import NullCheck, TypeCheck, CompletenessCheck, DataQualityCheck, RangeCheck
from .metrics_publisher import MetricsPublisher

def dq(record, checks, bootstrap_server, topic, schema):
    """
    Perform data quality checks on a record.

    Args:
        record (dict): The record to be checked.
        checks (list): A list of instances of check classes to perform (e.g., [NullCheck(), TypeCheck()]).
        bootstrap_server (str): The Kafka bootstrap server address.
        topic (str): The name of the Kafka topic to send metrics to.
        schema (dict): The expected schema for the record.

    Returns:
        list: A list of issues found during the checks.
    """
    # Initialize the publisher
    publisher = MetricsPublisher(bootstrap_server)

    # Create a DataQualityCheck instance with the provided checks
    data_quality_check = DataQualityCheck(checks)

    # Perform data quality checks
    issues = data_quality_check.perform_checks(record, schema)

    # Publish issues to Kafka if any
    if issues:
        for issue in issues:
            publisher.publish(topic, issue)
        print(f"Record failed data quality checks. Issues published to Kafka: {issues}")
    else:
        print(f"Record passed data quality checks.")

    return issues  # Return the list of issues
