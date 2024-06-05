import pulumi
from s3_bucket import S3Bucket
from dynamodb_table import DynamoDBTable
from iam_role import LambdaIAMRole
from lambda_function import LambdaFunction

bucket = S3Bucket('my-bucket')

table = DynamoDBTable('my-table')

role = LambdaIAMRole('lambdaRole', bucket.bucket.arn, table.table.arn)

lambda_function = LambdaFunction('myLambda', role.role.arn, bucket.bucket.id, bucket.bucket.arn, table.table.name)

pulumi.export('bucket_name', bucket.bucket.id)
pulumi.export('table_name', table.table.name)
