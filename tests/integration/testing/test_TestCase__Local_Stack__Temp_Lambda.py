from osbot_utils.utils.Files                                        import path_combine, file_exists, file_write
from osbot_utils.utils.Functions                                    import function_source_code
from osbot_utils.utils.Misc                                         import list_set
from osbot_utils.utils.Objects                                      import dict_to_obj
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
        assert get_env('OSBOT_LAMBDA_S3_BUCKET') == self.s3_bucket
        assert self.lambda_function.exists()     is True

    def test_update_lambda_code(self):
        def run(event, context):                                                        # this is going to be the new lambda handler
            return 'dynamic lambda code'                                                # updated return value (which we confirm below after updating the lambda code)

        with self.lambda_function as _:
            lambda_file       = _.original_name.replace('.','/') + '.py'               # get the real path to the lambda handler
            lambda_file_path  = path_combine(_.folder_code, lambda_file)               # combine it with the temp folder (that has the lambda function code)
            new_source_code   = function_source_code(run)                              # get the function source code for the temp lambda code
            file_write(path=lambda_file_path, contents=new_source_code)                # update file with the local code (in the run function above)

            assert file_exists(lambda_file_path) is True                               # confirm file exists
            assert _.invoke()                    == temp_lambda_return_message         # invoke current version of the lambda (using the code in temp_lambda.py file)
            assert _.update().get('status')                 == 'ok'                    # update the lambda function (i.e, upload zip to s3 and trigger lambda update)
            assert _.wait_for_function_update_to_complete() == 'Successful'            # wait for the function update to happen
            assert _.invoke()                               == 'dynamic lambda code'   # confirm that the lambda code has now been replaced with the text above

    def test_invoke(self):
        assert self.lambda_function.invoke() == temp_lambda_return_message

    def test_invoke__return_logs(self):
        result = dict_to_obj(self.lambda_function.invoke_return_logs())
        assert list_set(result)    == ['execution_logs', 'name', 'request_id', 'return_value', 'status']
        assert result.name         == 'osbot_local_stack_aws_lambdas_dev_temp_lambda'
        assert result.return_value == temp_lambda_return_message