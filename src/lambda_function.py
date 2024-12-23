import json
import logging
import traceback

from src.pipeline import PredictPipeline, CustomData

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        # Parse incoming JSON
        if "body" in event and event["body"]:
            input_data = json.loads(event["body"])
        else:
            # Direct invocation or raw test event
            input_data = event

        custom_data = CustomData(
            PwnCount=input_data.get("PwnCount", 0),
            IsSensitive=input_data.get("IsSensitive", False),
            IsRetired=input_data.get("IsRetired", False),
            IsSpamList=input_data.get("IsSpamList", False),
            IsMalware=input_data.get("IsMalware", False),
            IsSubscriptionFree=input_data.get("IsSubscriptionFree", False),
            TimeToDiscovery=input_data.get("TimeToDiscovery", 0),
            DataClassesCount=input_data.get("DataClassesCount", 0),
        )

        # Convert to a DataFrame
        df = custom_data.get_data_as_dataframe()

        # Initialize the pipeline
        pipeline = PredictPipeline()

        # Perform prediction
        preds = pipeline.predict(df)

        # Construct response
        response_body = {
            "prediction": preds[0] if len(preds) > 0 else None,
            "input": input_data,
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_body),
        }

    except Exception as e:
        logger.error("Error during Lambda execution: %s", str(e))
        traceback.print_exc()

        # Return an error response
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
