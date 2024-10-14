from osbot_utils.utils.Json                                       import json_parse
from osbot_utils.utils.Objects                                    import dict_to_obj, __
from osbot_local_stack.aws.lambdas.dev.with__requests             import run
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda import TestCase__Local_Stack__Temp_Lambda, \
    LAMBDA__DEPENDENCIES__REQUESTS


class test_with__requests(TestCase__Local_Stack__Temp_Lambda):

    @classmethod
    def setUpClass(cls):
        cls.lambda_handler   = run
        # cls.delete_after_run = False                      # when enabling this:
        #cls.s3_bucket        = "local-stack-tcbdeidxdqjy"  #    set the bucket name here
        #cls.aws_region       = 'ap-south-1'                #    and the region here
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    @classmethod
    def create_temp_lambda(cls):
        with cls.deploy_lambda as _:
            _.add_modules(LAMBDA__DEPENDENCIES__REQUESTS)

        super().create_temp_lambda()

    def test_invoke(self):
        payload  = dict(url="https://httpbin.org/get")
        url_data = dict_to_obj(json_parse(self.lambda_function.invoke(payload)))
        assert url_data.args == __()
        assert url_data.url  == payload.get('url')
        assert url_data.headers.Host == 'httpbin.org'

# class test_non_deleted_lambda(TestCase__Local_Stack):
#     aws_region  = 'eu-west-2'
#     lambda_name = 'osbot_local_stack_aws_lambdas_dev_with__requests'
#     bucket_name = 'local-stack-tcbdeidxdqjy'
#
#     def test__check_bucket_and_lambda_exists(self):
#         pprint(aws_config.region_name())
#         assert S3    ().bucket_exists(bucket_name   = self.bucket_name) is True
#         assert Lambda().exists       (function_name = self.lambda_name) is True
#         #pprint(Lambda().info(function_name=self.lambda_name))
#         #pprint(Lambda().exists(function_name=self.lambda_name))
#         #pprint(Lambda().functions_names())
#
#     def test__invoke_function(self):
#         payload = dict(url="https://httpbin.org/get")
#         result  = Lambda(name=self.lambda_name).invoke(payload=payload)
#         pprint(result)

