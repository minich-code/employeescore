import sys
from src.logger import logging

# Define a function to extract error message details
def error_message_detail(error, error_detail: sys):
    # Get the traceback information from the error_detail
    _, _, exc_tb = error_detail.exc_info()
    # Extract the filename from the traceback
    file_name = exc_tb.tb_frame.f_code.co_filename
    # Create a formatted error message containing filename, line number, and error message
    error_message = "Error occurred in Python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    # Return the formatted error message
    return error_message

# Define a custom exception class
class CustomException(Exception):
    # Constructor to initialize the exception with an error message and error detail
    def __init__(self, error_message, error_detail: sys):
        # Call the parent class constructor to set the error message
        super().__init__(error_message)
        # Call the error_message_detail function to get detailed error message
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    # Override the __str__ method to return the error message
    def __str__(self):
        return self.error_message


# # Try the exception if it will work
# if __name__ == "__main__":
#     try:
#         a = 1/1
#     except Exception as e:
#         logging.info("Divide by zero error occurred")
#         raise CustomException(e, sys)
