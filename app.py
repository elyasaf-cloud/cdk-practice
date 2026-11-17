#!/usr/bin/env python3

import aws_cdk as cdk
import json

from cdk_learning.bucket_stack import BucketStack
from cdk_learning.network_stack import NetworkStack
from cdk_learning.lambda_stack import LambdaStack

app = cdk.App()

environment = app.node.try_get_context("environment") or "prod"

with open(f"config/{environment}.json") as file:
    config = json.load(file)

env = cdk.Environment(account=config["account"], region=config["region"])

networkStack = NetworkStack(app, "NetworkStack", env=env, config=config)

bucketStack= BucketStack(app, "BucketStack", gatwayEndpoint=networkStack.gatewayEndpoint, env=env, config=config)

LambdaStack(app, "LambdaStack", vpc=networkStack.vpc, bucket=bucketStack.bucket, env=env, config=config)

app.synth()
