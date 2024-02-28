
import logging  # Import the logging module
import os  # Import the os module
from datetime import datetime  # Import the datetime class from the datetime module

# Define the log file name using the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the path to the log file inside a 'logs' directory in the current working directory
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the 'logs' directory if it doesn't exist already
os.makedirs(logs_path, exist_ok=True)

# Define the full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the logging module with basic settings
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Specify the log file path
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Define the log message format
    level=logging.INFO,  # Set the logging level to INFO, meaning only INFO level messages and above will be logged
)

# # Testing the logger
# if __name__ == "__main__":
#     # Log an information message
#     logging.info("Logging into the system")

