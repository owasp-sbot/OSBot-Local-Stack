from osbot_aws.aws.s3.S3                                            import S3
from osbot_utils.utils.Env                                          import set_env
from osbot_local_stack.local_stack.Local_Stack__Internal            import DEFAULT__LOCAL_STACK__TARGET_SERVER
from osbot_aws.deploy.Deploy_Lambda                                 import Deploy_Lambda
from osbot_local_stack.aws.lambdas.dev.hello_world                  import run
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda
from osbot_aws.aws.lambda_.Lambda                                   import Lambda


class test_TestCase__Local_Stack__Temp_Lambda(TestCase__Local_Stack__Temp_Lambda):

    def test__setUpClass(self):
        lambda_name = 'an-test-lambda'
        #with Lambda() as _:
        set_env('OSBOT_LAMBDA_S3_BUCKET', self.s3_bucket)

    def test_create__temp_lambda(self):
        bucket_name = self.s3_bucket
        with S3() as _:
            set_env('OSBOT_LAMBDA_S3_BUCKET', bucket_name)
            assert _.bucket_exists(bucket_name) is True

        deploy_lambda = Deploy_Lambda(handler=run)
        assert deploy_lambda.osbot_setup.s3.client().meta.endpoint_url == DEFAULT__LOCAL_STACK__TARGET_SERVER

        update_status = deploy_lambda.update()

        if update_status == "Pending":
            update_status = deploy_lambda.lambda_function().wait_for_function_update_to_complete(wait_time=0.5)  # in GH actions it can take up to 10 seconds to update the lambda
        assert update_status  == 'Successful'

        with Lambda() as _:
           assert 'osbot_local_stack_aws_lambdas_dev_hello_world' in _.functions_names()

        with S3() as _:
             assert 'lambdas/osbot_local_stack.aws.lambdas.dev.hello_world.zip'  in _.find_files(bucket_name)

        assert deploy_lambda.invoke() == 'Hello "World"'
        assert deploy_lambda.invoke(dict(name='OSBot')) == 'Hello "OSBot"'
