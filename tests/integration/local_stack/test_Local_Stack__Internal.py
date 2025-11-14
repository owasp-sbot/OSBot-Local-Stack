from unittest                                            import TestCase
from osbot_utils.testing.__                              import __
from osbot_utils.utils.Misc                              import list_set
from osbot_local_stack.local_stack.Local_Stack__Internal import Local_Stack__Internal, DEFAULT__LOCAL_STACK__TARGET_SERVER


class test_Local_Stack__Internal(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.local_stack__internal = Local_Stack__Internal()

    def test__init__(self):
        with self.local_stack__internal as _:
            assert _.obj() == __(endpoint_url='http://localhost:4566')

    def test_get__aws_lambda_runtimes(self):
        with (self.local_stack__internal as _):
            assert 'python3.11' in _.get__aws_lambda_runtimes().Runtimes
            assert 'python3.12' in _.get__aws_lambda_runtimes().Runtimes
            #   __(Runtimes=[ 'dotnet6', 'java8.al2', 'python3.8', 'provided.al2', 'python3.9', 'java21', 'nodejs16.x',
            #                                                     'python3.10', 'provided.al2023', 'nodejs20.x', 'dotnet8', 'java11', 'ruby3.2',
            #                                                     'nodejs18.x', 'python3.12', 'java17', 'ruby3.3', 'python3.11'])

    def test_get__internal_health(self):
        with self.local_stack__internal as _:
            expected_available_services = ['s3','_lambda', 'iam', 'cloudwatch', 'dynamodb', 'logs', 'sts']
            health = _.get__internal_health()                           # obj_to_dict will make all fields to be valid python names
            #assert health == __()
            assert health.services.resource_groups == 'disabled'
            for service_name in expected_available_services:
                assert getattr(health.services,service_name)   in ['available', 'running']

            #assert health.version.startswith('3.8.')           is True

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
            assert list_set(_.get__internal_plugins()) == [ 'localstack_aws_provider'                        ,          # obj_to_dict will make all fields to be valid python names
                                                            'localstack_hooks_configure_localstack_container',
                                                            'localstack_hooks_on_infra_ready'                ,
                                                            'localstack_hooks_on_infra_shutdown'             ,
                                                            'localstack_hooks_on_infra_start'                ,
                                                            'localstack_hooks_prepare_host'                  ,
                                                            'localstack_init_runner'                         ]

    def test_target_server(self):
        with self.local_stack__internal as _:
            assert _.endpoint_url == DEFAULT__LOCAL_STACK__TARGET_SERVER
