import os
import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ["PwnCount", "TimeToDiscovery", "DataClassesCount"]
            categorical_columns = [
                "IsSensitive",
                "IsRetired",
                "IsSpamList",
                "IsMalware",
                "IsSubscriptionFree",
            ]

            num_pipeline = Pipeline(steps=[("scaler", StandardScaler())])

            cat_pipeline = Pipeline(
                steps=[
                    ("onehot", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", num_pipeline, numerical_columns),
                    ("cat", cat_pipeline, categorical_columns),
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        try:
            train_df = pd.read_csv(train_path)
            train_df["AddedDate"] = pd.to_datetime(
                train_df["AddedDate"], utc=True
            ).dt.tz_localize(None)
            train_df["BreachDate"] = pd.to_datetime(
                train_df["BreachDate"], utc=True
            ).dt.tz_localize(None)
            train_df["TimeToDiscovery"] = (
                train_df["AddedDate"] - train_df["BreachDate"]
            ).dt.days
            train_df["DataClassesCount"] = train_df["DataClasses"].str.count(",") + 1

            test_df = pd.read_csv(test_path)
            test_df["AddedDate"] = pd.to_datetime(
                test_df["AddedDate"], utc=True
            ).dt.tz_localize(None)
            test_df["BreachDate"] = pd.to_datetime(
                test_df["BreachDate"], utc=True
            ).dt.tz_localize(None)
            test_df["TimeToDiscovery"] = (
                test_df["AddedDate"] - test_df["BreachDate"]
            ).dt.days
            test_df["DataClassesCount"] = test_df["DataClasses"].str.count(",") + 1

            logging.info("Loaded train and test datasets")

            preprocessing_obj = self.get_data_transformer_object()

            # The target column
            target_column_name = "financial_estimated_loss"
            input_features_train_df = train_df.drop(
                columns=[target_column_name], axis=1
            )
            target_feature_train_df = train_df[target_column_name]
            input_features_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing to dataframes")
            input_features_train_arr = preprocessing_obj.fit_transform(
                input_features_train_df
            )
            input_features_test_arr = preprocessing_obj.transform(
                input_features_test_df
            )

            train_arr = np.c_[
                input_features_train_arr, target_feature_train_df.to_numpy()
            ]
            test_arr = np.c_[input_features_test_arr, target_feature_test_df.to_numpy()]

            logging.info("Saving preprocessing object")
            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                preprocessing_obj,
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
