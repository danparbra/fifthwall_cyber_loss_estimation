import os
import sys

import numpy as np
import dill
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException


def save_object(file_path: str, obj: dict):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(
    X_train,
    y_train,
    X_test,
    y_test,
    models,
    params,
    scoring="neg_mean_absolute_percentage_error",
):
    try:
        report = {}

        for model_name, model in models.items():
            param = params.get(model_name, {})

            gs = GridSearchCV(model, param, cv=3, scoring=scoring, n_jobs=-1)
            gs.fit(X_train, y_train)

            best_model = gs.best_estimator_
            best_params = gs.best_params_

            best_model.fit(X_train, y_train)

            # Predictions
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            # Scores
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)
            test_mse = mean_squared_error(y_test, y_test_pred)
            test_mape = mean_absolute_percentage_error(y_test, y_test_pred)

            report[model_name] = {
                "best_params": best_params,
                "train_r2": train_r2,
                "test_r2": test_r2,
                "test_mse": test_mse,
                "test_mape": test_mape,
            }

            print(
                f"{model_name} completed. Test R^2: {test_r2}, Test MSE: {test_mse}, Test MAPE: {test_mape}"
            )

        return report

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path: str):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)
