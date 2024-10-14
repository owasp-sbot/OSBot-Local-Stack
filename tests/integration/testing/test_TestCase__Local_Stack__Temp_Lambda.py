from osbot_utils.context_managers.print_duration import print_duration

from osbot_aws.AWS_Config import aws_config

from osbot_aws.aws.s3.S3 import S3

from osbot_utils.utils.Env import set_env

from osbot_local_stack.local_stack.Local_Stack__Internal import DEFAULT__LOCAL_STACK__TARGET_SERVER
from osbot_utils.utils.Objects import obj_info
from osbot_aws.deploy.Deploy_Lambda                                 import Deploy_Lambda
from osbot_local_stack.aws.lambdas.dev.hello_world                  import run
from osbot_local_stack.testing.TestCase__Local_Stack__Temp_Lambda   import TestCase__Local_Stack__Temp_Lambda
from osbot_utils.utils.Dev                                          import pprint
from osbot_aws.aws.lambda_.Lambda                                   import Lambda


class test_TestCase__Local_Stack__Temp_Lambda(TestCase__Local_Stack__Temp_Lambda):

    def test__setUpClass(self):
        lambda_name = 'an-test-lambda'
        #with Lambda() as _:
        set_env('OSBOT_LAMBDA_S3_BUCKET', self.s3_bucket)

    def test_create__temp_lambda(self):
        with S3() as _:
            bucket_name = self.s3_bucket
            #region_name = 'eu-west-1'
            #_.bucket_create(bucket_name, region_name)
            set_env('OSBOT_LAMBDA_S3_BUCKET', bucket_name)
            #set_env('AWS_DEFAULT_REGION'    , region_name)
            assert _.bucket_exists(bucket_name) is True


        deploy_lambda = Deploy_Lambda(handler=run)
        #pprint(deploy_lambda.obj())
        assert deploy_lambda.osbot_setup.s3.client().meta.endpoint_url == DEFAULT__LOCAL_STACK__TARGET_SERVER
        # print("-------------")
        # with deploy_lambda as _:
        #     _.add_function_source_code()
        #     update_result = _.package.update()
        #     pprint(update_result)
        #     update_status = _.lambda_function().wait_for_function_update_to_complete(wait_time=0.5)
        #     print("------------- CONFIGURATION (after update_status)")
        #     pprint(_.lambda_function().configuration())
        #     print("-------------")
        #     print("UPDATE STATUS: ", update_status)
        #
        # #for i in range(1,10):
        #
        #     # print("-------------")
        #     # print(f"Deploying lambda #{i}" )
        #     # result = deploy_lambda.update()
        #     # if result == 'Successful':
        #     #     break
        #     # else:
        #     #     pprint(f"got result: {result}")
        #     #     package_update_result = deploy_lambda.package.update()
        #     #     pprint(package_update_result)
        update_status = deploy_lambda.update()
        if update_status == "Pending":
            print("*********************************************")
            print("Waiting for update to complete")
            update_status = deploy_lambda.lambda_function().wait_for_function_update_to_complete(wait_time=0.5)
            print("*********************************************")
            pprint("update_status", update_status)
        assert update_status                                 == 'Successful'

        with Lambda() as _:
           assert 'osbot_local_stack_aws_lambdas_dev_hello_world' in _.functions_names()

        with S3() as _:
             assert 'lambdas/osbot_local_stack.aws.lambdas.dev.hello_world.zip'  in _.find_files(bucket_name)

        with print_duration() as duration_1:
            assert deploy_lambda.invoke() == 'Hello "World"'
        with print_duration() as duration_2:
            assert deploy_lambda.invoke(dict(name='OSBot')) == 'Hello "OSBot"'

        assert duration_1.seconds < 5           # 1st execution is slower due to the need to setup the funciton
        assert duration_2.seconds < 0.1         # 2nd execution should be much faster
