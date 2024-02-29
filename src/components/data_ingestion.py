# Import the necessary modules.
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Import after data_transformation and utils 
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# Import after model trainer 
from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

# Define a dataclass to hold the data ingestion configuration. 
# It's essentially a container for holding configuration data.
# it is responsible for holding the configuration details such as file paths for training data, testing data, and raw data
@dataclass
class DataIngestionConfig:
    # Define default file paths for train, test, and raw data
    # We indicate that the training data will be stored in a folder named 'artifacts', and the filename will be 'train.csv'.
    train_data_path: str = os.path.join('artifacts', "train.csv")
    # The path to the test data.
    test_data_path: str = os.path.join('artifacts', "test.csv")
    # The path to the raw data.
    raw_data_path: str = os.path.join('artifacts', "data.csv")

# Define a class for data ingestion.
# It is a class responsible for performing the actual data ingestion operations
class DataIngestion:
    # Constructor method to initialize the DataIngestion object
    def __init__(self):
        # Create an instance of DataIngestionConfig to store configuration
        # The ingestion_config attribute of the DataIngestion class is used to store the configuration for the data ingestion process.
        # This configuration includes the paths to the train data, test data, and raw data.
        self.ingestion_config = DataIngestionConfig()

    # Method to initiate data ingestion process
    def initiate_data_ingestion(self):
        # Log the message to indicate the start of the data ingestion process.
        logging.info("Entered the data ingestion method or component")
        try:
            # Read the dataset as a dataframe.
            df = pd.read_csv('notebook\data\stud.csv')
            # Log the successful reading of the dataset.
            logging.info('Read the dataset as dataframe')
            # Create the directory for the train data if it doesn't exist.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            # Save the dataframe to the raw data path.
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            # Log the successful saving of the raw data.
            logging.info("Train test split initiated")
            # Split the dataframe into train and test sets.
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            # Save the train set to the train data path.
            # The ingestion_config.train_data_path attribute is used to specify the path to the train data. 
            # This path is used to save the train set to a CSV file.
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            # Save the test set to the test data path.
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            # Log the successful completion of the data ingestion process.
            logging.info("Ingestion of the data is completed")
            # Return the paths to the train and test data.
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            # Log the exception.
            logging.error(e)
            # Raise a custom exception.
            raise CustomException(e, sys)
        
# if __name__=="__main__":
#     obj = DataIngestion()
#     obj.initiate_data_ingestion()


# After data transformation and utils 

# We have combined data transformation and data ingestion
# when the script is run directly, it performs data ingestion and transformation operations 
# if __name__=="__main__":
#     obj = DataIngestion() # creates an instance of the DataIngestion class, which is responsible for data ingestion operations.
#     train_data, test_data =  obj.initiate_data_ingestion() # This line calls the initiate_data_ingestion() method of the DataIngestion.

#     data_transformation = DataTransformation() # Creates an instance of the DataTransformation class, responsible for data transformation operations.
#     data_transformation.initiate_data_transformation(train_data, test_data) # This method initiates the data transformation process


# After model trainer 
if __name__=="__main__":
    obj = DataIngestion() 
    train_data, test_data =  obj.initiate_data_ingestion() 

    data_transformation = DataTransformation() 
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data) 

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr, test_arr))

    