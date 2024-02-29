# Import necessary modules
import os  # Operating system module for interacting with the file system
import sys  # System-specific parameters and functions
import pickle  # Module for serializing and deserializing Python objects
from src.exception import CustomException  # Custom exception class for handling errors

# Define function to save an object to a file
def save_object(file_path, obj):
    try:
        # Extract the directory path from the given file path
        # Get the directory path of the file
        dir_path = os.path.dirname(file_path)

        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)

        # Open the file specified by file_path in binary write mode
        with open(file_path, "wb") as file_obj:
            # Serialize the object (obj) and write it to the file using pickle.dump()
            pickle.dump(obj, file_obj)

    # Handle exceptions that may occur within the try block
    except Exception as e:
        # Raise a CustomException with details of the error
        raise CustomException(e, sys)
