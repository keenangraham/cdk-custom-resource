#!/usr/bin/env python3
import os

import aws_cdk as cdk

from shared_infrastructure.cherry_lab import US_WEST_2

from cdk_custom_resource.cdk_custom_resource_stack import CustomResourceStack


app = cdk.App()

CustomResourceStack(
    app,
    'CdkCustomResourceStack',
    env=US_WEST_2,
)

app.synth()
