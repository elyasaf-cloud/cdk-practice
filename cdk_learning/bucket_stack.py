from aws_cdk import Stack, RemovalPolicy, aws_s3 as s3, aws_ec2 as ec2

from constructs import Construct


class BucketStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        gatwayEndpoint: ec2.IGatewayVpcEndpoint,
        config: dict,
        **kwargs,
    ) -> None:

        super().__init__(scope, construct_id, **kwargs)

        # Bucket with policy
        self.bucketName = f"{config['prefix']}-bucket-{config['account']}"

        bucket = s3.Bucket(
            self,
            "MyBucket",
            bucket_name=self.bucketName,
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.RETAIN,
        )

        # define variables
        bucket_arn = bucket.bucket_arn
        vpc_endpoint_id = gatwayEndpoint.vpc_endpoint_id
        user_name = config["admin"]

        # create policy as pyhton ditionary
        policy_dict = {
            "Version": "2012-10-17",
            "Statement": [
                # Denies reading, writing and deleting objects unless the request comes through our VPC endpoint.
                # All conditions in a statement must be true for it to apply.
                {
                    "Sid": "DenyAccessOutsideVPC",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                    "Resource": [bucket_arn, f"{bucket_arn}/*"],
                    "Condition": {
                        "StringNotEquals": {"aws:SourceVpce": vpc_endpoint_id},
                        "Bool": {"aws:PrincipalIsAWSService": "false"},
                        "StringNotLike": {"aws:userid": f"*:{user_name}"},
                    },
                },
                # Denies any request sent over plain HTTP, so data is always encrypted in transit.
                # AWS service principals are excluded so AWS's own internal access isn't blocked.
                {
                    "Sid": "DenyInsecureTransport",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:*",
                    "Resource": [bucket_arn, f"{bucket_arn}/*"],
                    "Condition": {
                        "Bool": {
                            "aws:SecureTransport": "false",
                            "aws:PrincipalIsAWSService": "false",
                        }
                    },
                },
            ],
        }

        bucket_policy = s3.CfnBucketPolicy(
            self,
            "BucketPolicy",
            bucket=self.bucketName,
            policy_document=policy_dict,
        )
