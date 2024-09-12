from datetime import datetime  # Import the datetime module

class DataIngestion:
    def __init__(self, checks, publisher):
        self.checks = checks
        self.publisher = publisher

    def process_data(self, df, expected_types):
        for column in df.columns:
            self._check_column(df, column)

    def process_single_record(self, record, expected_types):
        """
        Process a single customer record for data quality checks.
        """
        print("Incoming record:", record)  
        for column in expected_types.keys():
            if column in record:
                self._check_single_value(record, column, expected_types[column])

    def _check_single_value(self, record, column, expected_type):
        
        original_value = record[column]  
        print(f"Original value for '{column}': {original_value} (type: {type(original_value).__name__})")  

        # Null value check
        if record[column] is None:
            metrics = {
                "timestamp": datetime.utcnow().isoformat() + "Z", 
                "column": column,
                "issue": "Null value found",
                "category": "Null Percentage",
                "total_rows": 1,
                "null_count": 1,
                "null_percentage": 100.0,
                "threshold": self.checks.null_threshold,
            }
            self.publisher.publish('data_quality_metrics', metrics)
            return 

        # Data type check
        type_check_result = self.checks.check_data_type(record[column], expected_type)
        print(f"Converted value for '{column}': {record[column]} (type: {type(record[column]).__name__})")  # Debugging info

        if not type_check_result["is_correct_type"]:
            metrics = {
                "timestamp": datetime.utcnow().isoformat() + "Z",  # Use current UTC time
                "column": column,
                "issue": "Data type mismatch",
                "category": "Data Type",
                "expected_type": type_check_result["expected_type"],
                "actual_type": type_check_result["actual_type"],
            }
            self.publisher.publish('data_quality_metrics', metrics)
