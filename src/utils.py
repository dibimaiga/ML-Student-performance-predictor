#Utils we'll have all the common things

import os
import sys

import numpy as np 
import pandas as pd
import pickle # this will help us create the pkl file
# pickle: It converts Python objects
# (like trained models, scalers, encoders) into a byte stream that can be saved to disk,
# then loaded back later. Think of it as "freezing" your object to use it later.
# Pickle lets you separate training time (expensive, one-time)
# from inference time (cheap, repeated). Without it, you couldn't build practical ML applications.

from src.exception import CustomException

from sklearn.metrics import r2_score

def save_object(file_path, obj):
    """
    file_path: A string like "artifacts/model.pkl" - where to save the file

    obj: The Python object you want to save (could be a model, preprocessor, dictionary, etc.)
    """
    try:
        dir_path = os.path.dirname(file_path)
#         os.path.dirname(): Extracts the directory path from the full file path.
# Example: If file_path = "artifacts/models/model.pkl", then dir_path = "artifacts/models"
# This is needed because we need to ensure the directory exists before saving the file.

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            
# "with" = Automatically manage opening/closing
# "open(...)" = Open the file
# "model.pkl" = File path
# "wb" = Write mode + Binary mode
# "as file_obj" = Call it 'file_obj' so I can use it
# pickle.dump(...) = Save the model to that file
# (exit block) = File automatically closes

    except Exception as e: #Catches any exception that occurred in the try block and assigns it to variable e.
        raise CustomException(e, sys)


def evaluate_models(X_train,y_train,X_test,y_test,
                    models):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]

            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)