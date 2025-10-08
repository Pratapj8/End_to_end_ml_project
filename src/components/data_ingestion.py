# Reading the data
# Data Ingestion
# python src/components/data_ingestion.py

import os
import sys

# Read the Errors/loggings from the src folder
from src.exception import CustomException
from src.logger import logging

import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


# This module is like a map telling your ML pipeline exactly where to find and store the key data files.
# Creating a data class to store all file paths related to data ingestion
@dataclass
class DataIngestionConfig:
    # train_data_path: variable that stores the training dataset path
    # str = defines the variable type as a string
    # os.path.join('artifacts', 'train.csv') = creates 'artifacts' folder and saves file as 'train.csv'
    train_data_path: str = os.path.join("artifacts", "train.csv")

    # test_data_path: variable that stores the testing dataset path
    # str = defines the variable type as a string
    # os.path.join('artifacts', 'test.csv') = creates 'artifacts' folder and saves file as 'test.csv'
    test_data_path: str = os.path.join("artifacts", "test.csv")

    # raw_data_path: variable that stores the raw/original dataset path
    # str = defines the variable type as a string
    # os.path.join('artifacts', 'raw.csv') = creates 'artifacts' folder and saves file as 'raw.csv'
    raw_data_path: str = os.path.join("artifacts", "raw.csv")


# -----------------------------------------
# Summary:
# This code defines a configuration class (DataIngestionConfig)
# that sets up file paths for saving raw, training, and testing data
# inside an 'artifacts' folder. It helps organize dataset locations
# for the data ingestion step in a machine learning pipeline.
# -----------------------------------------


# This class automates the data loading and splitting stage of your ML pipeline — preparing clean, structured inputs for model training and testing.
# Class to handle the process of reading, saving, and splitting data
class DataIngestion:
    def __init__(self):
        # Create an instance of DataIngestionConfig to access file paths
        self.ingestion_config = DataIngestionConfig()

    # Function to start the data ingestion process
    def initiate_data_ingestion(self):
        logging.info("Data Ingestion method starts")  # Log start of data ingestion

        try:
            # Read the dataset from a CSV file into a pandas DataFrame
            df = pd.read_csv("/Users/apple/Downloads/Data_science_file/Agent8/Projects/currency_ml_project/notebook/data/data.csv")
            logging.info("Dataset read as pandas DataFrame")

            # (Optional) You can modify this to read from cloud (AWS, SQL, API, etc.)
            # df = ...

            # Create the directory for storing raw data if it doesn't exist
            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True
            )

            # Save the raw/original dataset as a CSV file
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            logging.info("Train test split initiated")
            # Split the dataset into training and testing sets (70% train, 30% test)
            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)

            # Save the training dataset as 'train.csv' in artifacts folder
            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )

            # Save the testing dataset as 'test.csv' in artifacts folder
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )

            logging.info("Ingestion of Data is completed")  # Log successful completion

            # Return paths of training and testing data for later use
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            # Log if any exception occurs during data ingestion
            logging.info("Exception occurred at Data Ingestion stage")

            # Raise a custom exception with system info for debugging
            raise CustomException(e, sys)
        
        
# -----------------------------------------
# Summary:
# Reads raw data from a CSV file.
# Creates necessary folders to store processed files.
# Saves a copy of raw data for backup.
# Splits data into training and testing sets.
# Saves both datasets into the artifacts folder.
# Handles any errors gracefully using CustomException.
# -----------------------------------------



if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
