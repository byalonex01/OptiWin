import logging
import os
from datetime import datetime

# Configure logging
log_file = 'operation_log.txt'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# List to track operations for rollback
operation_history = []

def log_operation(operation):
    """Logs an operation."""
    logging.info(operation)
    operation_history.append(operation)

def rollback():
    """Rollback the last operation."""
    if operation_history:
        last_operation = operation_history.pop()
        logging.info(f'Rolled back operation: {last_operation}')
        return last_operation
    else:
        logging.warning('No operations to rollback')
        return None

# Example usage
if __name__ == "__main__":
    log_operation("Initialized logging system")
