from aws_cdk import Stack
from aws_cdk import Duration


from constructs import Construct

#from aws_cdk.custom_resource import Provider

from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_lambda import Runtime

from aws_cdk.aws_iam import PolicyStatement


class CustomResourceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_latest_rds_snapshot_id = PythonFunction(
            self,
            'GetLatestRDSSnapshotID',
            entry='cdk_custom_resource/runtime/lambda/',
            runtime=Runtime.PYTHON_3_9,
            index='functions.py',
            handler='get_latest_rds_snapshot_id',
            timeout=Duration.seconds(60),
        )

        get_latest_rds_snapshot_id.role.add_to_policy(
            PolicyStatement(
                actions=['rds:DescribeDBSnapshots'],
                resources=['*'],
            )
        )
