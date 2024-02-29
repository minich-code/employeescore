import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
import os

# Class responsible for making predictions using a trained model
class PredictPipeline:
    def __init__(self):
        pass

    # Method to make predictions using the saved model
    def predict(self, features):
        try:
            # Define paths for model and preprocessor (Load the model from the artifacts folder)
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join('artifacts', 'proprocessor.pkl')
            
            # Load trained model and preprocessor
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            
            # Transform input features using preprocessor
            data_scaled = preprocessor.transform(features)
            
            # Make predictions using the model
            preds = model.predict(data_scaled)
            
            # Return predictions
            return preds
        
        # Handle exceptions
        except Exception as e:
            raise CustomException(e, sys)


# Custom data class to represent input data for prediction
# CustomData class allows you to create instances representing individual data points
class CustomData:
    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        # Initialize attributes
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    # Method to convert custom data object to a DataFrame
    # the get_data_as_data_frame method helps convert these instances into DataFrames, which can be used as input for various data processing tasks
    def get_data_as_data_frame(self):
        try:
            # Create a dictionary from custom data attributes
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            # Convert the dictionary to a DataFrame
            return pd.DataFrame(custom_data_input_dict)

        # Handle exceptions
        except Exception as e:
            raise CustomException(e, sys)
