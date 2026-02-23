variable "project_name" {
  description = "Project name for resource definition"
  type        = string
  default     = "uploadfile"
}

variable "aws_region" {
  description = "Define the AWS region"
  type        = string
  default     = "eu-north-1"
}

variable "lambda_runtime" {
  description = "Lambda runtime version"
  type        = string
  default     = "python 3.11"
}

variable "vpc_name" {
  description = "name of the vpc"
  type        = string
  default     = "filesharing_vpc"
}

variable "bucket_name" {
  description = "name of the bucket to store the files"
  type        = string
  default     = "123_filesharing_bucket_321" # should be globally unique
}

variable "dynamodb_table_name" {
  description = "The table name of the table to store file metadate"
  type        = string
  default     = "secure_upload_db"
}
