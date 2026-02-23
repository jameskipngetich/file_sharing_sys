terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# TODO ADDD IaC logic for the aws services used in the application

# TODO add network IaC -> vpc-> public subnets, and private subnets(db) -> security groups for lambda

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  cidr   = "10.0.0.0/16"
  name   = var.vpc_name
  tags = {
    name        = var.vpc_name
    environment = "dev"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id     = vpc.vpc_id
  cidr_block = "10.0.1.0/16"

  tags = {
    name = "public_subnet"
  }
  # how do we attach internet gte waay
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = vpc.vpc_id
  cidr_block = "10.0.2.0/16"

  tags = {
    name = "private_subnet"
  }
}

resource "aws_security_group" "lambda_sg" {
  vpc_id = vpc.vpc_id
  # configure inbound and outbound rules

  tags = {
    name = "lambda_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow-ssh" {
  security_group_id = aws_security_group.lambda_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = "22"
  ip_protocol       = "ssh"
  to_port           = "22"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_ports" {
  security_group_id = aws_security_group.lambda_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}

# ToDO add s3 bucket IaC (bucket name is a variable)

module "aws_s3" {
  source = "terraform-aws-modules/s3-bucket/aws"
  bucket = var.bucket_name # remember to output bucket name
  acl    = "private"

  control_object_ownership = true
  object_ownership         = "ObjectWriter"

  force_destroy = true
}

# TODO add api gateway IaC
#TODO add lambda IaC -> how to add already written lambda handlers
/*
resource "aws_lambda" "filesharing_lambda" {
  # do reasearch on this module
}
*/
# TODO add dynamo db IaC -> a table -> with the provided attributes

module "dynamodb_table" {
  source                      = "terraform-aws-modules/dynamodb-table/aws"
  name                        = var.dynamodb_table_name
  hash_key                    = "id"
  deletion_protection_enabled = false

  attributes = [
    {
      name = "id"
      type = "N"
    },
    {
      name = "file_id"
      type = "S"
    },
    {
      name = "user_id"
      type = "S"
    },
    {
      name = "file_name"
      type = "S"
    },
    {
      name = "s3_key"
      type = "S"
    },
    {
      name = "content_type"
      type = "S"
    },
    {
      name = "upload_date"
      type = "N" # what is the type of date
    },
    {
      name = "status"
      type = "S"
    },
    {
      name = "id"
      type = "N"
    },

  ] # do research on this module
}
