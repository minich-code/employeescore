# Import necessary modules
import os  # Operating system module for interacting with the file system
import sys  # System-specific parameters and functions
import pickle  # Module for serializing and deserializing Python objects
from src.exception import CustomException  # Custom exception class for handling errors

# after model trainer 
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

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
    
# Function to evaluate multiple models using GridSearchCV
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        # Dictionary to store evaluation results for each model
        report = {}

        # Loop through each model in the dictionary of models
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            # Perform grid search to find the best parameters for the model
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            # Update the model with the best hyperparameters
            model.set_params(**gs.best_params_)

            # Fit the model to the training data
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

             # Predict the target variable for the training and testing data
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            # Calculate the R2 scores for the training and testing data
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

             # Add the model name and its R2 score to the report
            report[list(models.keys())[i]] = test_model_score
        
        # Return the report dictionary containing R-squared scores for each model
        return report
    
    # Handle exceptions
    except Exception as e:
        raise CustomException(e, sys)
    
# Function to load an object from a file    
def load_object(file_path):
    try:
         # Open the file in binary read mode and load the object using pickle
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    
    # Handle exceptions
    except Exception as e:
        raise CustomException(e, sys)
