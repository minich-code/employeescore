# Import necessary libraries 
import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer # Import ColumnTransformer for column-wise transformations
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline # Import Pipeline for chaining multiple transformers
# # Import OneHotEncoder and StandardScaler for preprocessing categorical and numerical data
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

# Define a dataclass to hold the data transformation configuration. 
# It's essentially a container for holding transformation data.
# it is responsible for holding the transformation details such as preprocessor.pkl files
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")


# Define a class for data transformation.
# It is a class responsible for performing the actual data transformation
class DataTransformation:
    def __init__(self):
        # Initialize the DataTransformationConfig object
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):

        try:
            # Define numerical and categorical columns
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            # Create a pipeline for numerical columns
            num_pipeline= Pipeline(
                steps=[
                # Impute missing values with the median
                ("imputer",SimpleImputer(strategy="median")),
                # Scale the data using StandardScaler
                ("scaler",StandardScaler())

                ]
            )
            # Create a pipeline for categorical columns
            cat_pipeline=Pipeline(
                steps=[
                # Impute missing values with the most frequent value
                ("imputer",SimpleImputer(strategy="most_frequent")),
                # One hot encode the categorical data
                ("one_hot_encoder",OneHotEncoder()),
                # Scale the data using StandardScaler
                ("scaler",StandardScaler(with_mean=False))
                ]

            )
            # Log the categorical and numerical columns
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Create a ColumnTransformer to combine the numerical and categorical pipelines
            preprocessor=ColumnTransformer(
                [
                # Apply the numerical pipeline to the numerical columns
                ("num_pipeline",num_pipeline,numerical_columns),
                # Apply the categorical pipeline to the categorical columns
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]
            )

            return preprocessor
        
        except Exception as e:
            # If an exception occurs, raise a CustomException with details
            raise CustomException(e, sys)
        
    # Method to initiate data transformation        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            # Read the train and test data into pandas DataFrame
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            # Log information about reading train and test data
            logging.info("Read train and test data completed")

            # Log information about obtaining preprocessing object
            logging.info("Obtaining preprocessing object")

            # Get the preprocessing object for data transformation
            preprocessing_obj=self.get_data_transformer_object()

            # Define target column name and numerical columns
            # you will need to drop the target_column_name if you used a code to combine all numeric columns
             # Define the target column name
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # Drop the target column from the input feature dataframes in training and testing sets
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            # Log the application of the preprocessing object on the training and testing dataframes
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # Fit the preprocessing object to the training data and transform both the training and testing data 
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            # Concatenate the transformed input features with the target feature for both the training and testing data
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # Log the saving of the preprocessing object
            logging.info(f"Saved preprocessing object.")

            # Save the preprocessing object
            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            # Return the transformed train and test arrays and preprocessing object file path
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)