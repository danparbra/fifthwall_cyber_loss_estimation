import os
import sys
from dataclasses import dataclass
import numpy as np
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
from xgboost import XGBRegressor
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(
        self, train_array: np.ndarray, test_array: np.ndarray
    ) -> float:
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(
                    objective="reg:squarederror", random_state=42
                ),
            }
            params = {
                "Random Forest": {
                    "n_estimators": [50, 100],
                    "max_features": ["sqrt", "log2", None],
                    "max_depth": [None, 10],
                    "min_samples_split": [2, 5],
                    "min_samples_leaf": [1, 2],
                },
                "Gradient Boosting": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.1, 0.01],
                    "max_depth": [3, 5],
                },
                "XGBRegressor": {
                    "learning_rate": [0.1, 0.01],
                    "n_estimators": [50, 100],
                    "max_depth": [3, 5],
                },
            }

            model_report = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                params=params,
                scoring="neg_mean_absolute_percentage_error",
            )

            # Find the best model based on MAPE
            best_model_name, best_model_info = min(
                model_report.items(), key=lambda item: item[1]["test_mape"]
            )
            best_model_score = best_model_info["test_mape"]
            best_model_params = best_model_info["best_params"]

            # Initialize and fit the best model with training data
            best_model = models[best_model_name].set_params(**best_model_params)
            best_model.fit(X_train, y_train)

            if best_model_score > 0.06:
                raise CustomException("No model meets the acceptance criterion!")

            logging.info(f"Best model: {best_model_name}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            mse = mean_squared_error(y_test, predicted)
            mape = mean_absolute_percentage_error(y_test, predicted)

            logging.info(
                f"Model performance - R^2: {r2_square}, MSE: {mse}, MAPE: {mape}"
            )
            return mape

        except Exception as e:
            raise CustomException(e, sys)
