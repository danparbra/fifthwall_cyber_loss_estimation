variable "aws_region" {
    type = string
    default = "us-east-1"
}

variable "ecr_repo_name" {
    type = string
    default = "fifthwall-poc-repo"
}

variable "ecr_image_tag" {
    type = string
    default = "latest"
}