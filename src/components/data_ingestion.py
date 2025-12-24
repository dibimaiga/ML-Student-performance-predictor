#The main aim is to read the dataset from some data source. That data source can be created from the big data team
#or from the cloud Team or may be reading from the live stream data
#So we will read , then split the dataset and then transform it


import os 
import sys
#The reason we're importing these is because we'll use our customException
from src.exception import CustomException
from src.logger import logging

import pandas as pd #we have a dataframe

from sklearn.model_selection import train_test_split

from dataclasses import dataclass #(used to create class variables)

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig # Just to check everything is working fine


# In order to implement the dataingestion component there should be some input required
#for exemple where will I save the train dataset or test dataset or even the raw data 

@dataclass # because i will just create some class variables 
# Just stores configuration variables (no methods)
# Makes the class simpler and cleaner
class dataIngestionConfig: #WHERE to save three files:
    train_data_path: str = os.path.join("artifacts","train.csv")
    test_data_path: str = os.path.join("artifacts","test.csv")
    raw_data_path: str = os.path.join("artifacts","data.csv")

# here are those inputs above. Now we know where to save train data and all
# Why save the raw data?

# Backup: Keep original data unchanged
# Debugging: Compare if transformations went wrong
# Reproducibility: Others can start from the same raw data

class DataIngestion: #here w're not just gonna crete class variables, there will some functions(that's why we don't need the (@dataclass)and so we will create a constructor part )
    """
    This class will have methods (functions), not just variables
    We need __init__ to set up the config
    """
    def __init__(self):
        self.ingestion_config = dataIngestionConfig() # to initialize the path(all 3 in this single variable)
#Now I'll write my own fucntion
    def initiate_data_ingestion(self):
        """
        Here we'll focus on reading the data from a database
        :param self: Description
        """
        logging.info("Entered the data ingestion component or method")
        try:
            df=pd.read_csv("notebook\data\stud.csv")
# The path "notebook\data\stud.csv" is hardcoded here. In production, you might:

# Read from a database
# Read from an API
# Read from cloud storage (S3, GCS)
# Pass the path as a parameter
            logging.info("Read the data as dataframe")

            #Now let's create the folders(artifacts) (we know the paths already)

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #I have to combine the directory pathname inside
            # Creates "artifacts" folder if it doesn't exist

            #let's save the raw data into 'raw_data_path' 
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Train test split initiated")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            # Saves training data to "artifacts/train.csv"

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            # Saves test data to "artifacts/test.csv"
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Ingestion of the data is completed")

            # Returns the file paths (not the data itself!)
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
# Why return paths instead of data?

# Memory efficient: Don't keep large DataFrames in memory
# Flexibility: Other components can load data when needed
# Persistence: Data is saved, can be used anytime
# Standard practice: Next component needs to know WHERE to find data

#return these two(train_data_path and test_data_path) , so that our data transfotmation component will take it and use it
        except Exception as e:
            raise CustomException(e,sys)
        
# If ANY error occurs in the try block, catch it
# Wrap it in your custom exception (better error messages)
# Raise it so the program stops with useful info


if __name__ == "__main__": #This code only runs when you execute this file directly
# Allows you to test this component standalone
# Doesn't run when imported by other files
# Common Python pattern

# Exemple: # Importing from another file:
# from src.components.data_ingestion import DataIngestion  # ✗ Code inside doesn't run

    obj = DataIngestion() #initialization(data ingestion object)
    train_data,test_data = obj.initiate_data_ingestion()

#So abve we've combined dataingestion then down we've combined DataTransformation
    data_transformation = DataTransformation()  # To initialize (and you'll see that it will be able to call this self.data_transformation_config function)
    data_transformation.initiate_data_transformation(train_data,test_data)



