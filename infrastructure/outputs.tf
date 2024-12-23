output "invoke_url" {
  description = "Base URL of the API Gateway"
  value       = "${aws_api_gateway_deployment.api_deployment.invoke_url}"
}