from aws_cdk import Stack, RemovalPolicy, aws_s3 as s3, aws_ec2 as ec2, aws_iam as iam

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
        self.bucket = s3.Bucket(
            self,
            "MyBucket",
            bucket_name=f"{config['prefix']}-bucket-{config['account']}",
            versioned=False,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            enforce_ssl=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # define variables
        bucket_arn = self.bucket.bucket_arn
        vpc_endpoint_id = gatwayEndpoint.vpc_endpoint_id
        user_id = f"{config['roleId']}:{config['admin']}"

        # Denies reading, writing and deleting objects unless the request comes through our VPC endpoint.
        # All conditions in a statement must be true for it to apply
        self.bucket.add_to_resource_policy(
            iam.PolicyStatement(
                sid="DenyAccessOutsideVPC",
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                resources=[self.bucket, self.bucket.arn_for_objects("*")],
                conditions={
                    "StringNotEquals": {
                        "aws:SourceVpce": gatwayEndpoint.vpc_endpoint_id
                    },
                    "Bool": {"aws:PrincipalIsAWSService": "false"},
                    "StringNotLike": {"aws:userid": user_id},
                },
            )
        )
