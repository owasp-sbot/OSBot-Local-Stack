from osbot_utils.context_managers.print_duration                 import print_duration
from osbot_utils.testing.Temp_Env_Vars                           import Temp_Env_Vars
from osbot_utils.utils.Env                                       import set_env
from osbot_aws.deploy.Deploy_Lambda                              import Deploy_Lambda
from osbot_local_stack.aws.lambdas.dev.temp_lambda               import run
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Bucket import TestCase__Local_Stack__Temp_Bucket

DEPLOY_LAMBDA__UPDATE_WAIT_TIME = 1.0

class TestCase__Local_Stack__Temp_Lambda(TestCase__Local_Stack__Temp_Bucket):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()                                                                                    # call the base class setUpClass(),  which will create the temp S3 Bucket (in Local Stack)
        cls.temp_env_vars   = Temp_Env_Vars(env_vars={'OSBOT_LAMBDA_S3_BUCKET': cls.s3_bucket}).set_vars()      # temporarily set the OSBOT_LAMBDA_S3_BUCKET to the temp S3 Bucket
        cls.deploy_lambda   = Deploy_Lambda(run)                                                                # create a Deploy_Lambda instance with the lambda handler from osbot_local_stack.aws.lambdas.dev.temp_lambda
        cls.lambda_function = cls.deploy_lambda.lambda_function()                                               # helper variable to reference the lambda function
        cls.create_temp_lambda()                                                                                # create the lambda function

    @classmethod
    def tearDownClass(cls):
        cls.delete_temp_lambda()
        super().tearDownClass()
        cls.temp_env_vars.restore_vars()

    @classmethod
    def create_temp_lambda(cls):
        with print_duration():
            update_status = cls.deploy_lambda.update()
            if update_status == "Pending":
                wait_time     = DEPLOY_LAMBDA__UPDATE_WAIT_TIME
                update_status = cls.deploy_lambda.lambda_function().wait_for_function_update_to_complete(wait_time=wait_time)       # in GH actions and locally it can take up to 10 seconds to update the lambda on the first run (I think due to the time it takes to download the docker image)
            assert update_status == 'Successful'
            assert cls.deploy_lambda.exists() is True

    @classmethod
    def delete_temp_lambda(cls):
        assert cls.deploy_lambda.delete() is True

    def invoke(self, params=None):
        return self.lambda_function.invoke(params)

    def invoke__return_logs(self, params=None):
        return self.lambda_function.invoke_return_logs(params)

