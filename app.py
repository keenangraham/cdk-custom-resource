import aws_cdk as cdk

from shared_infrastructure.igvf_dev.environment import US_WEST_2

from cdk_custom_resource.cdk_custom_resource_stack import CustomResourceStack


app = cdk.App()

CustomResourceStack(
    app,
    'CdkCustomResourceStack',
    env=US_WEST_2,
)

app.synth()
