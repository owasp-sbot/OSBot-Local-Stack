from unittest                                            import TestCase

from osbot_utils.utils.Env import not_in_github_action

from osbot_aws.aws.route_53.Route_53                     import Route_53
from osbot_aws.aws.sts.STS                               import STS
from osbot_aws.testing.Temp__Random__AWS_Credentials     import Temp_AWS_Credentials
from osbot_aws.aws.lambda_.Lambda                        import Lambda
from osbot_aws.AWS_Config                                import aws_config
from osbot_local_stack.local_stack.Local_Stack__Internal import DEFAULT__LOCAL_STACK__TARGET_SERVER
from osbot_aws.aws.s3.S3                                 import S3
from osbot_local_stack.local_stack.Local_Stack           import Local_Stack


class test_Local_Stack(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.local_stack = Local_Stack()

    # @trace_calls(include=['*'],show_class=True, show_duration=True, duration_bigger_than=0.1,
    #              show_locals=True)
    def test_activate(self):
        with Temp_AWS_Credentials():
            with self.local_stack as _:
                assert type(_) is Local_Stack
                assert _.check__local_stack__health             () is True
                assert _.check__local_stack__boto3_setup        () is True
                assert _.is_local_stack_configured_and_available() is True
                assert S3      ().client().meta.endpoint_url    == DEFAULT__LOCAL_STACK__TARGET_SERVER
                assert STS     ().client().meta.endpoint_url    == DEFAULT__LOCAL_STACK__TARGET_SERVER
                assert Lambda  ().client().meta.endpoint_url    == DEFAULT__LOCAL_STACK__TARGET_SERVER
                assert Route_53().client().meta.endpoint_url    == DEFAULT__LOCAL_STACK__TARGET_SERVER

            current_region = aws_config.region_name()
            assert _.check__local_stack__health             () is True
            if not_in_github_action():                                      # todo: figure out why this is failing in github actions
                assert _.check__local_stack__boto3_setup        () is False
                assert _.is_local_stack_configured_and_available() is False
                assert S3()    .client().meta.endpoint_url         in [f"https://s3.{current_region}.amazonaws.com", 'https://s3.amazonaws.com']
                assert STS     ().client().meta.endpoint_url       == f'https://sts.amazonaws.com'
                assert Lambda  ().client().meta.endpoint_url       == f'https://lambda.{current_region}.amazonaws.com'
                assert Route_53().client().meta.endpoint_url       == f'https://route53.amazonaws.com'


