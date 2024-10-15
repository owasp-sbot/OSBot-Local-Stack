import pytest

from osbot_utils.utils.Env import set_env

from osbot_aws.deploy.Deploy_Lambda import Deploy_Lambda

from osbot_aws.AWS_Config import aws_config

from osbot_aws.aws.lambda_.Lambda import Lambda

from osbot_local_stack.testing.TestCase__Local_Stack                import TestCase__Local_Stack
from osbot_utils.utils.Dev                                          import pprint
from osbot_local_stack.aws.lambdas.workflows.s3_events              import run
from osbot_local_stack.utils.Version                                import version__osbot_local_stack
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda, \
    LAMBDA__DEPENDENCIES__REQUESTS


class test_s3_events__create_bucket_and_lambda(TestCase__Local_Stack__Temp_Lambda):
    lambda_handler = run
    #delete_after_run = False

    @classmethod
    def create_temp_lambda(cls):
        cls.deploy_lambda.add_osbot_utils()
        cls.deploy_lambda.add_modules(LAMBDA__DEPENDENCIES__REQUESTS)
        super().create_temp_lambda()

    def test_invoke(self):
        response = self.lambda_function.invoke()
        assert response == '200'

@pytest.mark.skip("Only for local development")
class test_s3_events(TestCase__Local_Stack):
    aws_region     = 'sa-east-1' #'ap-south-1'
    s3_bucket      = "local-stack-jfpzjbftqgxd"
    lambda_handler = run

    def setUp(self):
        set_env('OSBOT_LAMBDA_S3_BUCKET', self.s3_bucket)

    def test_invoke(self):

        with Deploy_Lambda(handler=self.lambda_handler) as _:
            _.add_osbot_utils()
            _.add_modules(LAMBDA__DEPENDENCIES__REQUESTS)
            _.update()
            response = _.invoke()
            pprint(response)

# *** Skipping delete Lambda function: osbot_local_stack.aws.lambdas.workflows.s3_events
# *** Skipping delete bucket ***
# *** bucket name: local-stack-jfpzjbftqgxd
# *** region name: sa-east-1

