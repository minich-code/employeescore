from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize/Create a Flask application 
application = Flask(__name__)
app = application  # Alias for the application

# Route for the home page
@app.route('/')
def index():
    # Render the index.html template Render the home page.(create the index.html page)
    return render_template('index.html')

# Route for predicting data point
@app.route('/predictdata', methods=['GET', 'POST'])
# Predict the math score for a given set of features and Returns the  Rendered home page with prediction result.
def predict_datapoint():
    if request.method == 'GET':  # If request is GET, render home.html template
        return render_template('home.html')
    else:
        # If the request is a POST request, process the form data and create CustomData object
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))
        )
        
        # Convert CustomData object to DataFrame
        pred_df = data.get_data_as_data_frame()

        # Print the DataFrame for debugging purposes
        print(pred_df)  

        # Log the start of the prediction process        
        print("Before Prediction")
        
        # Initialize PredictPipeline
        predict_pipeline = PredictPipeline()
        # Log the mid-point of the prediction process
        print("Mid Prediction")
        
        # Make prediction using PredictPipeline
        results = predict_pipeline.predict(pred_df)
        # Log the end of the prediction process
        print("After Prediction")
        
        # Render home.html template with prediction results
        return render_template('home.html', results=results[0])

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0")
