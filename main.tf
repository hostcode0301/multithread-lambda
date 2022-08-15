terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

variable "aws_region" {
  default = "us-east-1"
}

provider "aws" {
  region  = var.aws_region
  profile = "terraform"
}

data "aws_caller_identity" "current" {}

resource "aws_dynamodb_table" "multithread_lambda_dynamodb_table" {
  name           = "multithread-lambda-dynamodb-table"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "PK"
  range_key      = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  attribute {
    name = "GSI1PK"
    type = "S"
  }

  attribute {
    name = "GSI1SK"
    type = "S"
  }

  global_secondary_index {
    name            = "GSI1"
    hash_key        = "GSI1PK"
    range_key       = "GSI1SK"
    projection_type = "ALL"
    read_capacity   = 5
    write_capacity  = 5
  }
}

resource "aws_ecr_repository" "multithread_lambda_repository" {
  name                 = "multithread-lambda-repository"
  image_tag_mutability = "IMMUTABLE"
}

data "aws_ecr_image" "multithread_lambda_image" {
  repository_name = aws_ecr_repository.multithread_lambda_repository.name
  image_tag       = "v0.1.0"
}

resource "aws_iam_role" "multithread_lambda_role" {
  name = "multithread-lambda-role"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.multithread_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "multithread_lambda_policy" {
  name = "multithread-lambda-policy"
  role = aws_iam_role.multithread_lambda_role.id
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : ["dynamodb:*"],
        "Resource" : "${aws_dynamodb_table.multithread_lambda_dynamodb_table.arn}"
      }
    ]
  })
}

resource "aws_lambda_function" "multithread_lambda" {
  function_name = "multithread-lambda"
  role          = aws_iam_role.multithread_lambda_role.arn
  image_uri     = "${aws_ecr_repository.multithread_lambda_repository.repository_url}@${data.aws_ecr_image.multithread_lambda_image.id}"
  package_type  = "Image"
}
