#We have numerical and categorical variables, What kind of transformation we'll apply to each
#The main purpose of data transformation is to do basically Feature Engineering, data cleaning, convert my 
#categorical features into numerical

import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer # for missing values
from sklearn.pipeline import Pipeline #for implementing the pipeline

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import os

# Let's create inputs required for the data transformation path 
@dataclass #A Python decorator that automatically creates a class with less boilerplate code. It's a cleaner way to create simple configuration classes.
class DataTransformationConfig: # Defines WHERE to save the preprocessing pipeline
    preprocessor_obj_file_path = os.path.join("artifacts","prepocessor.pkl")
# creates the path "artifacts/prepocessor.pkl"
# This is a configuration constant - if you want to change where files are saved, you only change it here


class DataTransformation:
    def __init__(self):
        """
        This function is responsible for data transformation based on the different types of data

        :param self: Description
        """
        self.data_transformation_config = DataTransformationConfig()
# Creates a DataTransformation class
# __init__: Constructor that runs when you create an instance
# Creates a config object and stores it as self.data_transformation_config
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]

            categorical_columns = [
            "gender",
            "race_ethnicity",
            "parental_level_of_education",
            "lunch",
            "test_preparation_course",
            ]

            #let's create pipelines for both

# A Pipeline chains multiple preprocessing steps together
# Data flows through each step in order
# Think of it like an assembly line

            num_pipeline = Pipeline( # numerical pipeline
                steps= [
                    ("imputer",SimpleImputer(strategy="median")), #handling missing values (Why median? More robust to outliers than mean)
                    ("scaler",StandardScaler(with_mean=False)) ## After StandardScaler(with_mean=False)
# Scales values to have unit variance
# with_mean=False:

# Skips centering: Doesn't subtract mean, only divides by std
# Preserves zeros: Critical for sparse data like one-hot encoding
# Keeps interpretation clear: 0 still means "category not present"
                ]
            )

            cat_pipeline = Pipeline( # categorical pipeline
                steps= [
                    ("imputer",SimpleImputer(strategy="most_frequent")), #handling missing values
                    ("one_hot_encoder",OneHotEncoder()), #one_hot_encoding
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
    #Use Mean if :
# Data has no outliers
# Data is normally distributed (bell curve)
# You want to preserve the total sum

# Let's just display our numerical and categorical columns
            logging.info(f"categorical columns: {categorical_columns}")
            logging.info(f"numerical columns: {numerical_columns}")
            
            preprocessor = ColumnTransformer( # combining the two pipelines
#  ColumnTransformer applies different transformations to different columns
# Think of it as a "master pipeline" that manages sub-pipelines
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )
# All outputs are combined into final array

            return preprocessor #we're returning  the entire preprocessing pipeline
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self,train_path,test_path):
# This is where the actual transformation happens. It takes file paths and returns transformed data.
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            #Now i'll be reading all my preprocessing object

            preprocessor_obj = self.get_data_transformer_object() #preprocessor_obj whatever object i created on top (this one : return preprocessor)
            #I will be getting this particular object over here
# Gets the preprocessing pipeline (ColumnTransformer with num + cat pipelines)
# Stores it in preprocessor_obj

            target_column = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            #axis=1: Drop column (axis=0 would drop rows)
            print(input_feature_train_df)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info("Applying preprocessing object on training dataframe and on test dataframe ")

            input_feature_train_arr=preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_obj.transform(input_feature_test_df)
# fit: Learns the parameters (median, mean, categories, etc.)
# transform: Applies the transformation

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
                ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
#np.c_ NumPy's column concatenation
# Sticks arrays together side-by-side

#Exemple:
# input_feature_train_arr (after preprocessing):
# [[0.85, 0.90, 1, 0, ...],  # All features (scaled, encoded)
#  [1.0,  1.1,  0, 1, ...]]

# # target_feature_train_df:
# [70, 88]

# # train_arr (combined):
# [[0.85, 0.90, 1, 0, ..., 70],  # Features + Target
#  [1.0,  1.1,  0, 1, ..., 88]]

# Convenient format for model training
# Some functions expect features and target together

            logging.info(f"Saved preprocessing object.")
# we need to convert our preprocessor into   pkl file. We've already taken a path and we're going to save this pkl file into the same same location

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
#So above with rhis function , we're saving the pkl file in the hard disk

# What's saved:

# The median values learned
# The categories for one-hot encoding
# The scaling parameters
# Everything needed to preprocess new data identically


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path

            )

# What's returned:

# train_arr: Preprocessed training data (features + target)
# test_arr: Preprocessed test data (features + target)
# preprocessor_obj_file_path: Path where preprocessor is saved

# Why return the path?

# So other parts of your code know where to find the saved preprocessor
# For example, the model training script needs to know this path
        except Exception as e:
            raise CustomException(e,sys)
        #if something happened succesfully but you don't see error , check if you write the exception
        






