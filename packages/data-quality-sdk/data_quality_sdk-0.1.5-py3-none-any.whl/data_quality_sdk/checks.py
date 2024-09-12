from datetime import datetime
import re

class NullCheck:
    def has_issues(self, record, column):
        """Check for null values in the specified column of a record."""
        is_null = record.get(column) is None
        return {
            "is_null": is_null,
            "metrics": {
                # "timestamp": datetime.utcnow().isoformat() + "Z",
                # "column": column,
                # "issue": "Null value found" if is_null else None,
                # "category": "Null Percentage",
                # "total_rows": 1,
                # "null_count": 1 if is_null else 0,
                # "null_percentage": 100.0 if is_null else 0.0,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": column,
                "check_type": "NullCheck",
                "check_category": 'Completeness',
                "check_name":"NullCheck",
                "quality_dimension":"",
                "status": 'failed' if is_null else 'passed'
            }
        }

class CompletenessCheck:
    def check(self, record, column):
        """Check the completeness of the specified column in a record."""
        is_complete = record.get(column) is not None
        return {
            "is_complete": is_complete,
            "metrics": {
                # "timestamp": datetime.utcnow().isoformat() + "Z",
                # "column": column,
                # "issue": "Incomplete data" if not is_complete else None,
                # "category": "Completeness",
                # "total_rows": 1,
                # "null_count": 1 if not is_complete else 0,
                # "completeness_percentage": 100.0 if is_complete else 0.0,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": column,
                "check_type": "CompletenessCheck",
                "check_category": 'Completeness',
                "check_name":"CompletenessCheck",
                "quality_dimension":"",
                "status": 'failed' if not is_complete else 'passed'
            }
        }

class TypeCheck:
    def __init__(self, schema):
        self.schema = schema

    def has_issues(self, value, column):
        """Check the data type of the value against the expected type."""
        expected_type = self.schema[column]
        actual_type = type(value).__name__  # Get the actual type of the value
        is_correct_type = (expected_type == "int" and isinstance(value, int)) or \
                          (expected_type == "string" and isinstance(value, str))
        return {
            "is_correct_type": is_correct_type,
            "metrics": {
                # "timestamp": datetime.utcnow().isoformat() + "Z",
                # "column": column,
                # "issue": "Data type mismatch" if not is_correct_type else None,
                # "category": "Data Type",
                # "expected_type": expected_type,
                # "actual_type": actual_type,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": column,
                "check_type": "",
                "check_category": 'Schema',
                "check_name":"TypeCheck",
                "quality_dimension":"Schema",
                "status": 'failed' if not is_correct_type else 'passed'
            }
        }

class RangeCheck:
    def __init__(self, column, min_value, max_value):
        self.column = column
        self.min_value = min_value
        self.max_value = max_value

    def has_issues(self, record):
        """Check if the value in the specified column is within the range."""
        value = record.get(self.column)
        is_in_range = (value is not None) and (self.min_value <= value <= self.max_value)
        return {
            "is_in_range": is_in_range,
            "metrics": {
                # "column": self.column,
                # "issue": "Value out of range" if not is_in_range else None,
                # "value": value,
                # "min_value": self.min_value,
                # "max_value": self.max_value,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": self.column,
                "check_type": "",
                "check_category": 'Validation',
                "check_name":"RangeCheck",
                "quality_dimension":"Validation",
                "status": 'failed' if not is_in_range else 'passed'
            }
        }

class FormatCheck:
    def __init__(self, column, pattern):
        self.column = column
        self.pattern = pattern

    def has_issues(self, record):
        """Check if the value in the specified column matches the format."""
        value = record.get(self.column)
        matches = re.match(self.pattern, value) is not None if value is not None else False
        return {
            "matches_format": matches,
            "metrics": {
                # "column": self.column,
                # "issue": "Format mismatch" if not matches else None,
                # "value": value,
                # "expected_format": self.pattern,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": self.column,
                "check_type": "",
                "check_category": 'Validation',
                "check_name":"FormatCheck",
                "quality_dimension":"Validation",
                "status": 'failed' if not matches else 'passed'
            }
        }

class LengthCheck:
    def __init__(self, column, min_length, max_length):
        self.column = column
        self.min_length = min_length
        self.max_length = max_length

    def has_issues(self, record):
        """Check if the length of the value in the specified column is within the limits."""
        value = record.get(self.column)
        length = len(value) if value is not None else 0
        is_valid_length = self.min_length <= length <= self.max_length
        return {
            "is_valid_length": is_valid_length,
            "metrics": {
                # "column": self.column,
                # "issue": "Length out of bounds" if not is_valid_length else None,
                # "value": value,
                # "length": length,
                # "min_length": self.min_length,
                # "max_length": self.max_length,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": self.column,
                "check_type": "",
                "check_category": 'Validation',
                "check_name":"LengthCheck",
                "quality_dimension":"Validation",
                "status": 'failed' if not is_valid_length else 'passed'
            }
        }

class ConsistencyCheck:
    def __init__(self, start_column, end_column):
        self.start_column = start_column
        self.end_column = end_column

    def has_issues(self, record):
        """Check if the start date is before the end date."""
        start_date = record.get(self.start_column)
        end_date = record.get(self.end_column)
        
        # Assuming dates are in string format 'YYYY-MM-DD'
        is_consistent = (start_date <= end_date) if start_date and end_date else True
        
        return {
            "is_consistent": is_consistent,
            "metrics": {
                # "start_column": self.start_column,
                # "end_column": self.end_column,
                # "issue": "Inconsistent dates" if not is_consistent else None,
                # "start_value": start_date,
                # "end_value": end_date,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": self.start_column,
                "check_type": "",
                "check_category": 'Consistency',
                "check_name":"ConsistencyCheck",
                "quality_dimension":"Consistency",
                "status": 'failed' if not is_consistent else 'passed'
            }
        }
 




class DependencyCheck:
    def __init__(self, column_a, column_b):
        self.column_a = column_a
        self.column_b = column_b

    def has_issues(self, record):
        """Check if both fields are present or absent together."""
        a_present = record.get(self.column_a) is not None
        b_present = record.get(self.column_b) is not None
        
        # If one is present, the other must also be present
        is_valid = (a_present and b_present) or (not a_present and not b_present)
        
        return {
            "is_valid": is_valid,
            "metrics": {
                # "column_a": self.column_a,
                # "column_b": self.column_b,
                # "issue": "One of the fields is present while the other is missing" if not is_valid else None,
                # "a_present": a_present,
                # "b_present": b_present,
                "id": datetime.utcnow().isoformat() + "Z",
                "column_name": self.column_a,
                "check_type": "",
                "check_category": 'Schema',
                "check_name":"DataTypeCheck",
                "quality_dimension":"Schema",
                "status": 'failed' if not is_valid else 'passed'
            }
        }



class DataQualityCheck:
    def __init__(self, checks):
        self.checks = checks

    def perform_checks(self, record, expected_types):
        metrics = []  
        
        for check in self.checks:
            if isinstance(check, NullCheck):
                for column in expected_types.keys():
                    result = check.has_issues(record, column)
                    metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, CompletenessCheck):
                for column in expected_types.keys():
                    result = check.check(record, column)
                    metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, TypeCheck):
                for column in expected_types.keys():
                    if column in record:
                        result = check.has_issues(record[column], column)
                        metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, RangeCheck):
                result = check.has_issues(record)
                metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, FormatCheck):
                result = check.has_issues(record)
                metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, LengthCheck):
                result = check.has_issues(record)
                metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, ConsistencyCheck):
                result = check.has_issues(record)
                metrics.append(result["metrics"])  # Append metric regardless of pass/fail

            elif isinstance(check, DependencyCheck):
                result = check.has_issues(record)
                metrics.append(result["metrics"])  # Append metric regardless of pass/fail

        return metrics  # Return all metrics (passed and failed)
