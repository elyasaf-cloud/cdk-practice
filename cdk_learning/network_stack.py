from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC with 2 Availability Zones
        vpc = ec2.Vpc(
            self,
            "MyVpc",
            vpc_name="my-cdk-vpc",
            cidr="10.60.0.0/16",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet1",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                )
            ],
            gateway_endpoints=[
                vpc.addGatewayEndpoint(
                    name="BucketEndpoint",
                    service=ec2.GatewayVpcEndpointAwsService.S3,
                )
            ],
        )
