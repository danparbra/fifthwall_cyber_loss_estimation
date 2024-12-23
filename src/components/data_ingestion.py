import os
import sys
from dataclasses import dataclass
import pandas as pd
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started the data ingestion process")
        try:
            # Use proper path
            df = pd.read_csv("notebooks/data/breached_services_info.csv")
            logging.info("Dataset read successfully")

            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True
            )

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(f"Raw data saved at {self.ingestion_config.raw_data_path}")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )
            logging.info("Train-test split completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    ingestion = DataIngestion()
    train_data_path, test_data_path = ingestion.initiate_data_ingestion()
    print(f"Train data path: {train_data_path}")
    print(f"Test data path: {test_data_path}")

    data_transformer = DataTransformation()
    train_arr, test_arr, preprocessor_obj_file_path = (
        data_transformer.initiate_data_transformation(train_data_path, test_data_path)
    )
    print(f"Preprocessor object saved at {preprocessor_obj_file_path}")

    model_trainer = ModelTrainer()
    metric = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(f"Model trained successfully. Performance metric (MAPE): {metric}")
