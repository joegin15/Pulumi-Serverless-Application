import pulumi
import pulumi_aws as aws

class S3Bucket(pulumi.ComponentResource):
    def __init__(self, name, opts=None):
        super().__init__('custom:S3Bucket', name, {}, opts)

        self.bucket = aws.s3.Bucket(name)
        
        self.register_outputs({
            'bucket': self.bucket
        })
