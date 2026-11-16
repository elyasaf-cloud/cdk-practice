from pathlib import Path
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigwv2,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from constructs import Construct


class LambdaStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: ec2.IVpc,
        bucketName: str,
        config: dict,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create lambda with role
        my_role = iam.Role(
            self, "My Role", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        reader_fn = _lambda.Function(
            self,
            "MyFunction",
            runtime=_lambda.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=_lambda.Code.from_asset(str(Path(__file__).parent / "lambda_code")),
            role=my_role,
            environment={"BUCKET_NAME": bucketName},
        )

        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
        my_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaVPCAccessExecutionRole"
            )
        )

        # Insert the lambda to the vpc
        security_group = ec2.SecurityGroup(
            self,
            "CustomSG",
            vpc=vpc,
            description="Allow HTTPS outbound access",
            allow_all_outbound=False,
        )

        security_group.add_egress_rule(
            ec2.Peer.prefix_list(f"com.amazonaws.{config["region"]}.s3"),
            ec2.Port.tcp(443),
            "Allow HTTPS traffic",
        )

        capacity_provider = _lambda.CapacityProvider(
            self,
            "MyCapacityProvider",
            capacity_provider_name="my-capacity-provider",
            subnets=vpc.private_subnets,
            security_groups=[security_group],
        )

        capacity_provider.add_function(reader_fn)

        # Create API gateway for the lambda
        read_object_integration = HttpLambdaIntegration(
            "ReadObjectIntegration", reader_fn
        )
        http_api = apigwv2.HttpApi(self, "HttpApi")

        http_api.add_routes(
            path="/object/{file-name+}",
            methods=[apigwv2.HttpMethod.GET],
            integration=read_object_integration,
        )

        CfnOutput(
            self,
            "ApiOutput",
            value=http_api.api_endpoint,
            description="The endpoint of the api",
        )
