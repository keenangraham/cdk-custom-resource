from aws_cdk import Stack
from aws_cdk import Duration
from aws_cdk import CustomResource
from aws_cdk import CfnOutput

from constructs import Construct

from aws_cdk.custom_resources import Provider
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_logs import RetentionDays

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
            handler='custom_resource_handler',
            timeout=Duration.seconds(60),
        )

        get_latest_rds_snapshot_id.role.add_to_policy(
            PolicyStatement(
                actions=['rds:DescribeDBSnapshots'],
                resources=['*'],
            )
        )

        provider = Provider(
            self,
            'Provider',
            on_event_handler=get_latest_rds_snapshot_id,
            log_retention=RetentionDays.ONE_MONTH,
        )

        latest_snapshot = CustomResource(
            self,
            'LatestRDSSnapshopID',
            service_token=provider.service_token,
            properties={
                'database_id': 'abc123',
            }
        )

        CfnOutput(
            self,
            'LatestDBSnapshotArn',
            value=latest_snapshot.get_att_string(
                'DBSnapshotArn'
            )
        )
