from unittest import TestCase

from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint

from osbot_local_stack.local_stack.Local_Stack__Internal import Local_Stack__Internal, \
    DEFAULT__LOCAL_STACK__TARGET_SERVER
from osbot_utils.utils.Objects import __


class test_Local_Stack__Internal(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.local_stack__internal = Local_Stack__Internal()

    def test__init__(self):
        with self.local_stack__internal as _:
            assert _.obj() == __()

    def test_get__aws_lambda_runtimes(self):
        with self.local_stack__internal as _:
            assert _.get__aws_lambda_runtimes() == __(Runtimes=[ 'dotnet6', 'java8.al2', 'python3.8', 'provided.al2', 'python3.9', 'java21', 'nodejs16.x',
                                                                 'python3.10', 'provided.al2023', 'nodejs20.x', 'dotnet8', 'java11', 'ruby3.2',
                                                                 'nodejs18.x', 'python3.12', 'java17', 'ruby3.3', 'python3.11'])

    def test_get__internal_health(self):
        with self.local_stack__internal as _:
            health = _.get__internal_health()
            assert getattr(health.services, 'lambda'         ) == 'available'         # name clashes with lambda keyword
            assert getattr(health.services, 'resource-groups') == 'disabled'          # name has a - in it
            assert health.services.s3                          in ['available', 'running']
            assert health.services.iam                         in ['available', 'running']
            assert health.version                              == '3.8.2.dev15'
            # skipping this since there were a couple inconsistencies in the data when running this in GH Actions
            #delattr(obj_data.services, 'lambda'         )
            #delattr(obj_data.services, 'resource-groups')
            # assert obj_data == __(services=__( acm='disabled',  apigateway='disabled', cloudformation='disabled', cloudwatch='disabled', config='disabled', dynamodb='disabled', dynamodbstreams='disabled',
            #                                    ec2='disabled', es='disabled', events='disabled', firehose='disabled', iam='available', kinesis='disabled', kms='disabled', logs='disabled', opensearch='disabled',
            #                                    redshift='disabled', resourcegroupstaggingapi='disabled', route53='disabled', route53resolver='disabled', s3='running', s3control='disabled', scheduler='disabled',
            #                                    secretsmanager='disabled', ses='disabled', sns='disabled', sqs='disabled', ssm='disabled', stepfunctions='disabled', sts='available', support='disabled', swf='disabled', transcribe='disabled'),
            #                         edition='community',
            #                         version='3.8.2.dev14')

    def test_get__internal_init(self):
        with self.local_stack__internal as _:
            assert _.get__internal_init() == __(completed=__(BOOT=True, START=True, READY=True, SHUTDOWN=False), scripts=[])

    def test_get__internal_plugins(self):
        with self.local_stack__internal as _:
            assert list_set(_.get__internal_plugins()) == [ 'localstack.aws.provider'                        ,
                                                            'localstack.hooks.configure_localstack_container',
                                                            'localstack.hooks.on_infra_ready'                ,
                                                            'localstack.hooks.on_infra_shutdown'             ,
                                                            'localstack.hooks.on_infra_start'                ,
                                                            'localstack.hooks.prepare_host'                  ,
                                                            'localstack.init.runner'                         ]

    def test_target_server(self):
        with self.local_stack__internal as _:
            assert _.target_server() == DEFAULT__LOCAL_STACK__TARGET_SERVER
