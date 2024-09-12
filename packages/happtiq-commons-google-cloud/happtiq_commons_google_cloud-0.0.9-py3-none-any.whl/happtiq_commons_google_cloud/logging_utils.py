import google.cloud.logging
import logging
import os

def setup_logging():
    if is_cloud_function():
        setup_cloud_function_logger()
    else:
        logging.basicConfig(level=logging.INFO)

def is_cloud_function():
    K_SERVICE = os.getenv('K_SERVICE')
    return K_SERVICE != None

def setup_cloud_function_logger():
    google.cloud.logging.Client().setup_logging()
