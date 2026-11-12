from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
)

from constructs import Construct


class BucketStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "MyBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN
        )