resource "aws_lambda_function" "prediction_function" {
    function_name = "fifthwall-poc-prediction-lambda"
    role = aws_iam_role.prediction_lambda_role.arn
    timeout = 300
    image_uri = "${data.aws_ecr_repository.lambda_ecr_repo.repository_url}:${var.ecr_image_tag}"
    
    logging_config {
        application_log_level = "INFO"
        log_format = "JSON"
        system_log_level = "INFO"
    }

    image_config {
        command = ["src.lambda_function.lambda_handler"]
    }
}

data "aws_ecr_repository" "lambda_ecr_repo" {
  name = var.ecr_repo_name
}