# logging_utils.py
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log_error(error_message):
    logging.error(error_message)

def log_info(info_message):
    logging.info(info_message)

# Test for logging_utils.py
if __name__ == "__main__":
    print("Testing logging_utils.py...")
    setup_logging()
    
    # Test logging functions
    log_info("This is an info message.")
    log_error("This is an error message.")
    
    print("All tests passed! Check the logs above.")