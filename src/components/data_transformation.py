# This file is to change the categorical features to numerical, Onehotencoding,Label encoding
# If confussed check Notebook


import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# importing CustomException from src folder
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


# DataTransformationConfig class to store configuration for data transformation
@dataclass
class DataTransformationConfig:
    # Path to save preprocessor object as 'preprocessor.pkl' inside 'artifacts' folder
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


# DataTransformation class handles creation of preprocessing pipelines
class DataTransformation:
    def __init__(self):
        # Initializing configuration for data transformation
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function creates preprocessing pipelines for both
        numerical and categorical columns and returns a combined preprocessor object.
        """
        try:
            # Defining numerical and categorical feature names
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "class_groups",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Pipeline for numerical data:
            # - Fill missing values with median
            # - Standardize numerical features
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            # Pipeline for categorical data:
            # - Fill missing values with most frequent category
            # - Convert categories into one-hot encoded variables
            # - Scale encoded values (without centering)
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            # Logging for debugging/tracking
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info("Categorical columns encoding pipeline created successfully")
            logging.info("Numerical columns scaling pipeline created successfully")
            logging.info(f"Numerical columns: {numerical_columns}")

            # Combining both pipelines using ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns),
                ]
            )

            # Returning the combined preprocessor object
            return preprocessor

        except Exception as e:
            # Raising custom exception for better error tracking
            raise CustomException(e, sys)



    def initiate_data_transformation(self, train_path, test_path):
        """
        Reads training and test datasets, applies preprocessing transformations,
        saves the preprocessor object, and returns transformed arrays.
        """
        try:
            # Reading the train and test CSV files into pandas DataFrames
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and test data loaded successfully")

            # Get the preprocessor object (created in get_data_transformer_object)
            preprocessing_obj = self.get_data_transformer_object()

            # Define target column and numerical columns
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # Separate input features (X) and target variable (y) for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Separate input features (X) and target variable (y) for testing data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing on training and test data")

            # Fit preprocessor on training data and transform both train & test sets
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combine input features and target variable back into arrays
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Preprocessing complete. Saving preprocessor object.")

            # Save the fitted preprocessor object to the specified file path
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj,
            )

            # Return processed train & test arrays and preprocessor path
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            # Raise a custom exception for better error tracking
            raise CustomException(e, sys)
