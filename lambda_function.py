import pulumi
import pulumi_aws as aws

class LambdaFunction(pulumi.ComponentResource):
    def __init__(self, name, role_arn, bucket_id, bucket_arn, table_name, opts=None):
        super().__init__('custom:LambdaFunction', name, {}, opts)

        self.lambda_function = aws.lambda_.Function(name,
            runtime='python3.8',
            role=role_arn,
            handler='index.handler',
            code=pulumi.AssetArchive({
                '.': pulumi.FileArchive('./lambda_code')
            }),
            environment={
                'variables': {
                    'TABLE_NAME': table_name
                }
            }
        )

        self.lambda_permission = aws.lambda_.Permission(f"{name}-permission",
            action="lambda:InvokeFunction",
            function=self.lambda_function.name,
            principal="s3.amazonaws.com",
            source_arn=bucket_arn
        )

        self.bucket_notification = aws.s3.BucketNotification(f"{name}-notification",
            bucket=bucket_id,
            lambda_functions=[{
                'lambda_function_arn': self.lambda_function.arn,
                'events': ['s3:ObjectCreated:*']
            }],
            opts=pulumi.ResourceOptions(depends_on=[self.lambda_permission])
        )

        self.register_outputs({
            'lambda_function': self.lambda_function,
            'lambda_permission': self.lambda_permission,
            'bucket_notification': self.bucket_notification
        })
