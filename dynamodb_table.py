import pulumi
import pulumi_aws as aws

class DynamoDBTable(pulumi.ComponentResource):
    def __init__(self, name, opts=None):
        super().__init__('custom:DynamoDBTable', name, {}, opts)

        self.table = aws.dynamodb.Table(name,
            attributes=[{
                'name': 'id',
                'type': 'S',
            }],
            hash_key='id',
            read_capacity=5,
            write_capacity=5
        )
        
        self.register_outputs({
            'table': self.table
        })
