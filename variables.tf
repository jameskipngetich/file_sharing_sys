variable "project_name"{
    description = "Project name for resource definition"
    type = string
    default = "uploadfile"
}

variable "aws_region" {
    description = "Define the AWS region"
    type = string
    default = "us-east-1"
}

variable "lambda_runtime" {
    description = "Lambda runtime version"
    type = string
    default = "python 3.11"
}