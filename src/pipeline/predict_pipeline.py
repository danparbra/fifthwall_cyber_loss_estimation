"""
Pipeline for prediction using the trained model.
"""

import os
import sys
import pandas as pd
from dataclasses import dataclass
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self) -> None:
        model_path = os.path.join("artifacts", "model.pkl")
        preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
        self.model = load_object(file_path=model_path)
        self.preprocessor = load_object(file_path=preprocessor_path)

    def predict(self, features: pd.DataFrame) -> list:
        try:
            data_scaled = self.preprocessor.transform(features)
            preds = self.model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e, sys)


@dataclass
class CustomData:
    PwnCount: int
    IsSensitive: bool
    IsRetired: bool
    IsSpamList: bool
    IsMalware: bool
    IsSubscriptionFree: bool
    TimeToDiscovery: int
    DataClassesCount: int

    def get_data_as_dataframe(self):
        return pd.DataFrame([self.__dict__])
