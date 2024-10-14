from osbot_utils.utils.Files import path_combine, file_exists, file_contents, file_write

from osbot_utils.utils.Functions import function_source_code

from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Objects import dict_to_obj

from osbot_local_stack.aws.lambdas.dev.temp_lambda                  import temp_lambda_return_message
from osbot_utils.utils.Env                                          import get_env
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda


class test_TestCase__Local_Stack__Temp_Lambda(TestCase__Local_Stack__Temp_Lambda):

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        assert get_env('OSBOT_LAMBDA_S3_BUCKET') is None
        assert cls.lambda_function.exists()      is False

    def test__setUpClass(self):
        lambda_name = 'an-test-lambda'
        #with Lambda() as _:
        assert get_env('OSBOT_LAMBDA_S3_BUCKET') == self.s3_bucket
        assert self.lambda_function.exists()     is True

    def test_invoke(self):
        assert self.lambda_function.invoke() == temp_lambda_return_message

    def test_invoke__return_logs(self):
        from osbot_utils.utils.Dev import pprint
        result = dict_to_obj(self.lambda_function.invoke_return_logs())
        assert list_set(result)    == ['execution_logs', 'name', 'request_id', 'return_value', 'status']
        assert result.name         == 'osbot_local_stack_aws_lambdas_dev_temp_lambda'
        assert result.return_value == temp_lambda_return_message

    def test_update_lambda_code(self):
        def run(event, context):
            return 'return dynamic lambda code'

        new_source_code = function_source_code(run)

        from osbot_utils.utils.Dev import pprint
        with self.lambda_function as _:
            assert _.invoke() == temp_lambda_return_message                             # lamda

            lambda_file      = _.original_name.replace('.','/') + '.py'
            lambda_file_path = path_combine(_.folder_code, lambda_file)
            assert file_exists(lambda_file_path) is True
            file_write(path=lambda_file_path, contents=new_source_code)
            assert _.update().get('status')                 == 'ok'
            assert _.wait_for_function_update_to_complete() == 'Successful'
            assert _.invoke() == 'return dynamic lambda code'

        # with self.deploy_lambda as _:
        #     pprint(_.obj())
        #     #
        #     #_.update()
        #     #pprint(code)

    # def test_create__temp_lambda(self):
    #     bucket_name = self.s3_bucket
    #     #pprint(aws_config.region_name())
    #     with S3() as _:
    #         set_env('OSBOT_LAMBDA_S3_BUCKET', bucket_name)
    #         assert _.bucket_exists(bucket_name) is True
    #
    #     deploy_lambda = Deploy_Lambda(handler=run)
    #     assert deploy_lambda.osbot_setup.s3.client().meta.endpoint_url == DEFAULT__LOCAL_STACK__TARGET_SERVER
    #
    #     update_status = deploy_lambda.update()
    #
    #     if update_status == "Pending":
    #         update_status = deploy_lambda.lambda_function().wait_for_function_update_to_complete(wait_time=0.5)  # in GH actions it can take up to 10 seconds to update the lambda
    #     assert update_status  == 'Successful'
    #
    #     with Lambda() as _:
    #        assert 'osbot_local_stack_aws_lambdas_dev_hello_world' in _.functions_names()
    #
    #     with S3() as _:
    #          assert 'lambdas/osbot_local_stack.aws.lambdas.dev.hello_world.zip'  in _.find_files(bucket_name)
    #
    #     assert deploy_lambda.invoke() == 'Hello "World"'
    #     assert deploy_lambda.invoke(dict(name='OSBot')) == 'Hello "OSBot"'
    #
    # def test_execute_lambda(self):
    #     lambda_name = "osbot_local_stack_aws_lambdas_dev_hello_world"
    #     region_name = 'ap-southeast-1'
    #     aws_config.set_aws_session_region_name(region_name)
    #     with Lambda(lambda_name) as _:
    #         assert _.exists() is True
    #         result = _.invoke_return_logs(dict(name='abc'))
    #         pprint(result)