# Don't enter id , pwd in this code in production


# 🧱 1. Install Required Libraries , Make sure these are installed:

# pip install pymysql sqlalchemy pymongo boto3 pandas scikit-learn

import pandas as pd
import os
import logging
import sys
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
from pymongo import MongoClient
import boto3
from io import StringIO


#
class DataIngestionConfig:
    def __init__(self):
        self.source_type = "mysql"  # or "mongodb" or "s3"
        self.mysql_config = {
            "host": "localhost",
            "user": "your_user",
            "password": "your_password",
            "database": "your_db",
            "table": "your_table",
        }
        self.mongodb_config = {
            "uri": "mongodb://localhost:27017",
            "database": "your_db",
            "collection": "your_collection",
        }
        self.s3_config = {
            "bucket_name": "your-bucket",
            "file_key": "data/data.csv",
            "aws_access_key_id": "your-access-key",
            "aws_secret_access_key": "your-secret-key",
        }
        self.raw_data_path = "artifacts/raw_data.csv"
        self.train_data_path = "artifacts/train.csv"
        self.test_data_path = "artifacts/test.csv"


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def load_data_from_mysql(self):
        config = self.ingestion_config.mysql_config
        engine = create_engine(
            f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}/{config['database']}"
        )
        query = f"SELECT * FROM {config['table']}"
        return pd.read_sql(query, con=engine)

    def load_data_from_mongodb(self):
        config = self.ingestion_config.mongodb_config
        client = MongoClient(config["uri"])
        db = client[config["database"]]
        collection = db[config["collection"]]
        data = list(collection.find())
        df = pd.DataFrame(data)
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)
        return df

    def load_data_from_s3(self):
        config = self.ingestion_config.s3_config
        s3 = boto3.client(
            "s3",
            aws_access_key_id=config["aws_access_key_id"],
            aws_secret_access_key=config["aws_secret_access_key"],
        )
        obj = s3.get_object(Bucket=config["bucket_name"], Key=config["file_key"])
        return pd.read_csv(StringIO(obj["Body"].read().decode("utf-8")))

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion method starts")

        try:
            source_type = self.ingestion_config.source_type.lower()

            if source_type == "mysql":
                df = self.load_data_from_mysql()
            elif source_type == "mongodb":
                df = self.load_data_from_mongodb()
            elif source_type == "s3":
                df = self.load_data_from_s3()
            else:
                raise ValueError(f"Unsupported source type: {source_type}")

            logging.info("Dataset loaded into DataFrame")

            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True
            )
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)
            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )

            logging.info("Ingestion of Data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            logging.error("Exception occurred at Data Ingestion stage")
            raise CustomException(e, sys)


if __name__ == "__main__":
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()
    print("Train data saved to:", train_path)
    print("Test data saved to:", test_path)
