#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_learning.BucketStack import BucketStack
from cdk_learning.network_stack import NetworkStack


app = cdk.App()

BucketStack(
    app,
    "BucketStack"
)

NetworkStack(
    app,
    "NetworkStack"
)

app.synth()