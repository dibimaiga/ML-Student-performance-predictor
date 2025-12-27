from flask import Flask,request,render_template
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler #because i'll will probably try to use the pkl file
from src.pipelines.predict_pipeline import PredictPipeline,CustomData

application = Flask(__name__) #create an flask app and Flask(_name_) will  give us the entry point where we need to excute it

app = application #because later on we need to write the route and all

# Route for a home page

@app.route('/') # just create a blakect (/) (just like an home page)
def index():
    return render_template('index.html') # this will go search template (so we need to create it)

@app.route('/predictdata', methods = ['GET','POST'])
def predict_datapoint():
    """
    Getting and predicting my data 
    """
    if request.method == 'GET':
        return render_template('home.html') #returning our default home page
    #what will be there in the home.html is the simple input data fields that we need to provide to our model to do the prediction 
    
    #home.html is a simple html file who has all the data available over here  
     
    else: # the POST part
         #creating my data, Has to be in the predicting piplenine also
            
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        # above we're just reading and assigning our features. Basically if we 'POST' the request will get all the information about the features
        # and by doing this , we're getting those information

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        pred_pipeline = PredictPipeline()

        results = pred_pipeline.predict(pred_df)
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0")
    #host="0.0.0.0" will just mapped it to 127.0.0.1

#we delete debug=True for our deploiement 







