from unittest import TestCase

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

    def test_get__internal_health(self):
        with self.local_stack__internal as _:
            health = _.get__internal_health()
            assert getattr(health.services, 'lambda'         ) == 'available'         # name clashes with lambda keyword
            assert getattr(health.services, 'resource-groups') == 'disabled'          # name has a - in it
            assert health.services.s3                          in ['available', 'running']
            assert health.services.iam                         in ['available', 'running']
            assert health.version                              == '3.8.2.dev15'

    def test_get__internal_init(self):
        with self.local_stack__internal as _:
            assert _.get__internal_init() == __(completed=__(BOOT=True, START=True, READY=True, SHUTDOWN=False), scripts=[])


            #delattr(obj_data.services, 'lambda'         )
            #delattr(obj_data.services, 'resource-groups')

            # assert obj_data == __(services=__( acm='disabled',                       # there were a couple inconsistencies in the data when running this in GH Actions
            #                                    apigateway='disabled',
            #                                    cloudformation='disabled',
            #                                    cloudwatch='disabled',
            #                                    config='disabled',
            #                                    dynamodb='disabled',
            #                                    dynamodbstreams='disabled',
            #                                    ec2='disabled',
            #                                    es='disabled',
            #                                    events='disabled',
            #                                    firehose='disabled',
            #                                    iam='available',
            #                                    kinesis='disabled',
            #                                    kms='disabled',
            #                                    logs='disabled',
            #                                    opensearch='disabled',
            #                                    redshift='disabled',
            #                                    resourcegroupstaggingapi='disabled',
            #                                    route53='disabled',
            #                                    route53resolver='disabled',
            #                                    s3='running',
            #                                    s3control='disabled',
            #                                    scheduler='disabled',
            #                                    secretsmanager='disabled',
            #                                    ses='disabled',
            #                                    sns='disabled',
            #                                    sqs='disabled',
            #                                    ssm='disabled',
            #                                    stepfunctions='disabled',
            #                                    sts='available',
            #                                    support='disabled',
            #                                    swf='disabled',
            #                                    transcribe='disabled'),
            #                        edition='community',
            #                        version='3.8.2.dev14')

    def test_target_server(self):
        with self.local_stack__internal as _:
            assert _.target_server() == DEFAULT__LOCAL_STACK__TARGET_SERVER
