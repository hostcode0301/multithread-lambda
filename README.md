# Multithreading & Multiprocessing with Lambda

This demo shows how to use the `multithreading` and `multiprocessing` features of the `lambda` module by concurrently/parallel updating data to dynamodb.

## Infrastructure set up

- Create IAM account for running Terraform code with following Policy.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "iam:CreateRole",
                "lambda:GetFunctionConfiguration",
                "iam:AttachRolePolicy",
                "iam:PutRolePolicy",
                "lambda:ListProvisionedConcurrencyConfigs",
                "lambda:GetProvisionedConcurrencyConfig",
                "dynamodb:DescribeTable",
                "iam:ListAttachedRolePolicies",
                "dynamodb:DescribeContinuousBackups",
                "lambda:ListLayerVersions",
                "lambda:ListLayers",
                "lambda:ListCodeSigningConfigs",
                "lambda:GetAlias",
                "iam:ListRolePolicies",
                "iam:GetRole",
                "cloudtrail:LookupEvents",
                "lambda:ListFunctions",
                "lambda:GetEventSourceMapping",
                "ecr:CreateRepository",
                "lambda:ListAliases",
                "ecr:DescribePullThroughCacheRules",
                "lambda:GetFunctionUrlConfig",
                "iam:DeleteRole",
                "ecr:GetAuthorizationToken",
                "lambda:GetFunctionCodeSigningConfig",
                "dynamodb:CreateTable",
                "lambda:UpdateFunctionCode",
                "lambda:ListFunctionEventInvokeConfigs",
                "lambda:ListFunctionsByCodeSigningConfig",
                "lambda:GetFunctionConcurrency",
                "lambda:ListEventSourceMappings",
                "iam:GetRolePolicy",
                "lambda:ListVersionsByFunction",
                "lambda:GetLayerVersion",
                "dynamodb:ListTagsOfResource",
                "lambda:GetAccountSettings",
                "lambda:GetLayerVersionPolicy",
                "ecr:CreatePullThroughCacheRule",
                "ecr:PutRegistryPolicy",
                "ecr:GetRegistryScanningConfiguration",
                "iam:ListInstanceProfilesForRole",
                "lambda:ListTags",
                "iam:DeleteRolePolicy",
                "ecr:GetRegistryPolicy",
                "lambda:GetFunction",
                "ecr:DescribeRegistry",
                "lambda:ListFunctionUrlConfigs",
                "ecr:PutRegistryScanningConfiguration",
                "dynamodb:DescribeTimeToLive",
                "ecr:DeletePullThroughCacheRule",
                "ecr:BatchImportUpstreamImage",
                "lambda:GetFunctionEventInvokeConfig",
                "lambda:GetCodeSigningConfig",
                "ecr:DeleteRegistryPolicy",
                "lambda:GetPolicy",
                "ecr:PutReplicationConfiguration"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "ecr:*",
            "Resource": "arn:aws:ecr:<region>:<account_id>:repository/multithread-lambda-repository"
        }
    ]
}
```

- You can set your account tokens to profile `terraform` with

```
aws configure --profile terraform
```

- Run the following commands to set up the infrastructure:

```
terraform init
terraform apply -auto-approve
```

## Add init data to db

Go to `dynamo_dump_data` folder and run the following commands to add data to the db:

```
aws dynamodb --profile terraform batch-write-item --request-items file://prite-item --request-items file://processed_data.json
```

## Build & Run the demo

- Build:

```
docker build -t lambda_func -f <type>.Dockerfile .
```

- Run:

```
docker run
-p 9000:8080 --env-file .env  lambda-func:latest
```