from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Define FastAPI app
app = FastAPI()


# Define your data model using Pydantic
class CustomDataModel(BaseModel):
    PwnCount: int
    IsSensitive: bool
    IsRetired: bool
    IsSpamList: bool
    IsMalware: bool
    IsSubscriptionFree: bool
    TimeToDiscovery: int
    DataClassesCount: int


@app.get("/")
def read_root():
    return {"message": "Welcome to the Cyber Risk Prediction API"}


@app.post("/predict")
def predict(data: CustomDataModel):
    try:
        # Convert incoming data to DataFrame
        custom_data = CustomData(**data.dict())
        input_df = custom_data.get_data_as_dataframe()

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(input_df)

        return {"estimated_loss": results[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# uvicorn app:app --reload
