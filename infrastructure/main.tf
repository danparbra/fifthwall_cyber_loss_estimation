terraform {
  backend "s3" {
    bucket = "fifthwall-poc-cyber-loss-prediction-tfstate"
    key    = "np-rag/terraform.tfstate"
    region = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
  required_version = "~> 1.5"
}

provider "aws" {
  region = var.aws_region
}