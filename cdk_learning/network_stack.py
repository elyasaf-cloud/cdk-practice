from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, config: dict, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC with 2 Availability Zones
        self.vpc = ec2.Vpc(
            self,
            "MyVpc",
            vpc_name="my-cdk-vpc",
            ip_addresses=ec2.IpAddresses.cidr("10.50.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PrivateSubnet1",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                )
            ],
            nat_gateways=0,
        )

        self.gatewayEndpoint = self.vpc.add_gateway_endpoint(
            "BucketEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.S3,
        )
