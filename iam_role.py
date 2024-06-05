import pulumi
import pulumi_aws as aws

class LambdaIAMRole(pulumi.ComponentResource):
    def __init__(self, name, bucket_arn, table_arn, opts=None):
        super().__init__('custom:LambdaIAMRole', name, {}, opts)

        self.role = aws.iam.Role(name, assume_role_policy="""
        {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow",
              "Sid": ""
            }
          ]
        }
        """)

        self.role_policy = aws.iam.RolePolicy(f'{name}-policy',
            role=self.role.id,
            policy=pulumi.Output.all(bucket_arn, table_arn).apply(lambda args: f"""
            {{
                "Version": "2012-10-17",
                "Statement": [
                    {{
                        "Effect": "Allow",
                        "Action": [
                            "s3:GetObject",
                            "s3:PutObject",
                            "dynamodb:PutItem"
                        ],
                        "Resource": [
                            "{args[0]}/*",
                            "{args[1]}"
                        ]
                    }},
                    {{
                        "Effect": "Allow",
                        "Action": [
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"
                        ],
                        "Resource": "*"
                    }}
                ]
            }}
            """)
        )

        self.register_outputs({
            'role': self.role,
            'role_policy': self.role_policy
        })
