from aws_cdk import Stack
from aws_cdk import Tags
from aws_cdk import Duration
from aws_cdk import CustomResource
from aws_cdk import CfnOutput

from constructs import Construct

from aws_cdk.custom_resources import Provider
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from aws_cdk.aws_lambda import Runtime
from aws_cdk.aws_logs import RetentionDays

from aws_cdk.aws_iam import PolicyStatement

from aws_cdk.aws_rds import DatabaseInstanceFromSnapshot
from aws_cdk.aws_rds import DatabaseInstanceEngine
from aws_cdk.aws_rds import PostgresEngineVersion

from shared_infrastructure.cherry_lab.vpcs import VPCs
from aws_cdk.aws_ec2 import SubnetSelection
from aws_cdk.aws_ec2 import SubnetType
from aws_cdk.aws_ec2 import InstanceClass
from aws_cdk.aws_ec2 import InstanceType
from aws_cdk.aws_ec2 import InstanceSize
from aws_cdk.aws_ec2 import SecurityGroup


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
                'db_instance_identifier': 'lrowe-graphql-demo-rds',
            }
        )

        CfnOutput(
            self,
            'LatestDBSnapshotArn',
            value=latest_snapshot.get_att_string(
                'DBSnapshotArn'
            )
        )

        vpcs = VPCs(
            self,
            'VPCs'
        )

        database = DatabaseInstanceFromSnapshot(
            self,
            'DatabaseFromSnapshot',
            snapshot_identifier=latest_snapshot.get_att_string(
                'DBSnapshotArn'
            ),
            engine=DatabaseInstanceEngine.postgres(
                version=PostgresEngineVersion.VER_14_1
            ),
            vpc_subnets=SubnetSelection(
                subnet_type=SubnetType.PUBLIC,
            ),
            vpc=vpcs.default_vpc,
            allocated_storage=20,
            max_allocated_storage=30,
            instance_type=InstanceType.of(
                InstanceClass.BURSTABLE3,
                InstanceSize.MEDIUM,
            ),
            copy_tags_to_snapshot=False,
        )

        Tags.of(database).add(
            'new_tag',
            'from snapshot db',
        )
