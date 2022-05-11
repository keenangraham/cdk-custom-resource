import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_custom_resource.cdk_custom_resource_stack import CdkCustomResourceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_custom_resource/cdk_custom_resource_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkCustomResourceStack(app, "cdk-custom-resource")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
